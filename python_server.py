from flask import Flask
import csv
import config
import numpy as np
from flask import jsonify
import math
import requests
import googlemaps
from heapq import nsmallest
import itertools
import time
import pandas as pd
from sklearn.cluster import KMeans
from collections import deque, namedtuple
import json
import more_itertools as mit
import fileinput
from sets import Set
import sys
import os
cwd = os.getcwd()
dir = cwd+'/Christofides/Christofides'
if dir not in sys.path:
    sys.path.append(dir)
import christofides as christofides
app = Flask(__name__)

def ordered_insert(element, lista):
	i = 0;
	# print element
	while i < len(lista) and lista[i][2] <= element[2]:
		i += 1		
	lista.insert(i, element)
	# lista.append(element)
	# return lista  
def add_node(graph, node_f, node_t):
	# print "-" * 5, "detect_cicles", "-" * 5
	# print node_f, "=>", node_t
	# for n in graph:
	# 	print n, ":", graph[n]
	if node_f in graph and node_t in graph:
		if graph[node_t] == graph[node_f]:
			return True
		else:
			for n in graph:
				if graph[n] == graph[node_f]:
					graph[n] = graph[node_t]
	elif node_f in graph and not node_t in graph:
		graph[node_t] = graph[node_f]
	elif not node_f in graph and node_t in graph :
		graph[node_f] = graph[node_t]
	else:
		aux_num = len(graph)
		graph[node_t] = aux_num
		graph[node_f] = aux_num
	# print "-" * 5, "END detect", "-" * 5
	return False

def kruskal(lista):
	connected_1 = Set()
	connected_2 = Set()
	ids = []
	graph = {}
	l_from = []
	l_to = []
	for e in lista:
		e0_c1 = e[0] in connected_1
		e1_c1 = e[1] in connected_1
		e0_c2 = e[0] in connected_2
		e1_c2 = e[1] in connected_2
		cycle = False
		if e[0] in graph and e[1] in graph:
			cycle = graph[e[0]] == graph[e[1]]
		# print int(e0_c1), int(e1_c1), int(e0_c2), int(e1_c2), cycle, " | ",
		if not e0_c1 and not e1_c1 and not e0_c2 and not e1_c2 and not cycle:
			add_node(graph, e[0], e[1])
			l_from.append(e[0])
			l_to.append(e[1])
			connected_1.add(e[0])
			connected_1.add(e[1])
			# print "1"
		elif not e0_c1 and e1_c1 and not e0_c2 and not e1_c2 and not cycle:
			add_node(graph, e[0], e[1])
			l_from.append(e[0])
			l_to.append(e[1])
			connected_1.add(e[0])
			connected_2.add(e[1])
			# print "2"
		elif e0_c1 and not e1_c1 and not e0_c2 and not e1_c2 and not cycle:
			add_node(graph, e[0], e[1])
			l_from.append(e[0])
			l_to.append(e[1])
			connected_1.add(e[1])
			connected_2.add(e[0])
			# print "3"
		elif e0_c1 and e1_c1 and not e0_c2 and not e1_c2 and not cycle:
			add_node(graph, e[0], e[1])
		 	l_from.append(e[0])
			l_to.append(e[1])
			connected_2.add(e[0])
			connected_2.add(e[1])
			# print "4"

	return l_from, l_to

@app.route("/addresses")
def data_complete():
	# return "Hello World!"
	with open('./simulation/data.csv', 'rb') as csvfile:
		item_reader = csv.reader(csvfile, delimiter='|')
		rows = [row for row in item_reader]
	return jsonify(rows)

@app.route("/latlongs")
def latlongs():
	# return "Hello World!"
	with open('./simulation/locations.csv', 'rb') as csvfile:
		item_reader = csv.reader(csvfile, delimiter='|')
		rows = [row for row in item_reader]
	return jsonify(rows)

def group(lst, n):
	return zip(*[lst[i::n] for i in range(n)]) 

def divideByN(data, n):
	return [data[i*n : (i+1)*n] for i in range(len(data)//n)]

def getCombinations(seq):
	combinations = list()
	for i in range(0,len(seq)):
		for j in range(i+1,len(seq)):
			combinations.append([seq[i],seq[j]])
	return combinations 

def chunked(iterable, n):
    chunksize = int(math.ceil(len(iterable) / n))
    return (iterable[i * chunksize:i * chunksize + chunksize]
            for i in range(n))

def csv_to_distance_matrix(csv_file, length):
	with open(csv_file, 'rb') as csvfile:
		item_reader = csv.reader(csvfile, delimiter='|')
		rows = [row for row in item_reader]
		rows = np.array([str(row).split(',') for row in rows[1:]])
		distance_rows = [int(rows[i][-1].replace("'",'').replace("]",'')) for i in range(len(rows))]
		counter = 0
		len_rows = len(rows)
		A = [[0 for x in range(length)] for y in range(length)]
		 # Aqui estoy volviendo a combinar todos, hay un error 
		for i in range(length):
			temp_index = i*length
  			for j in range(temp_index):
  				A[i][j] = distance_rows[counter]
    			A[j][i] = A[i][j]
    			counter = counter + 1
    	df = pd.DataFrame(A)
    	df.to_csv('matrix.csv')
	print(len(A),len(A[0]), A)

@app.route("/alldistances")
def distances():
	gmaps = googlemaps.Client(key=config.api_key_distance_matrix)
	r = requests.get('http://localhost:3004/trucks/companies/:FirstTruckCompany')
	number_transports = len(r.json())
	# if working with locations, delimiter equals
	with open('./simulation/locations.csv', 'rb') as csvfile:
		item_reader = csv.reader(csvfile, delimiter='|')
		rows = [row for row in item_reader]
		rows = np.array([[float(row[0]), float(row[1])] for row in rows[1:]])
		distances = []
		kmeans = KMeans(n_clusters=number_transports)
		kmeans = kmeans.fit(rows)
		labels = kmeans.predict(rows)
		centroids = kmeans.cluster_centers_
		labels = np.array(labels)
		final_array = []
		final_distance = []
		for cluster in range(number_transports):
			row_to_write = ''
			document_name = 'cluster_' + str(cluster)+'.csv'
			#archivo de nodos conectados o resultado
			results_document_name = 'cluster_result' + str(cluster)+'.csv'
			with open(document_name,'a') as fd:
				fd.write(row_to_write)
			temp_indices = np.where(labels == cluster)[0].tolist()
			print(len(temp_indices), 'cluster length')

			previous_rows = rows[temp_indices].tolist()
			previous_rows.insert(0,[19.434940, -99.195697])

			temp_array = list(itertools.combinations(previous_rows,2))
			print(len(temp_array), 'combinations length')
			print(rows[temp_indices])
			times_array = []
			origins = list()
			for element in temp_array: 
				origins.append(element[0])
			destinations = list()
			for element in temp_array: 
				destinations.append(element[1])
			origins_divided = [list(c) for c in mit.divide(len(origins)/5, origins)]
			destinations_divided = [list(c) for c in mit.divide(len(origins)/5, destinations)]
			distance_matrix = []
			for i in range(len(origins_divided)):
				d_mat = gmaps.distance_matrix(origins_divided[i], destinations_divided[i], mode='driving')
				for row in d_mat['rows'][0]['elements']:
					distance_matrix.append(row['duration']['value'])
			final_temp_array = [[temp_array[i][0], temp_array[i][1], distance_matrix[i]] for i in range(len(temp_array))]
			df = pd.DataFrame(final_temp_array)
			df.to_csv(document_name)
			#Algoritmo de Gary
			distances = {}
			points = {}
			skip = True
			mat = []
			i = 0
			j = 0
			ordered_list = []
			# hay un bug aqui
			# with open(document_name) as csv_file:
			# 	csv_reader = csv.reader(document_name, quotechar='"', delimiter=',',
   			#quoting=csv.QUOTE_ALL, skipinitialspace=True)
			for l in final_temp_array:
				if skip:
					skip = False
				else:
					aux = str(l[0]) + str(l[1])
					distances[aux] = str(l[2]) 
					# print aux
					ordered_insert((str(l[0]), str(l[1]), int(str(l[2]))), ordered_list)
					# ordered_list = ordered_insert((l[1], l[2], int(l[3])), ordered_list)
					if not str(l[0]) in points:
						points[str(l[0])] = len(points)
					if not str(l[1]) in points:
						points[str(l[1])] = len(points)
			# for e in ordered_list:
			# 	print e
			# print len(ordered_list)
			# christophides
			l1, l2 = kruskal(ordered_list)
			route_array = zip(l1, l2)
			print "=" * 10
			tot_dist = 0
			for l, t in zip(l1, l2):
				tot_dist += int(distances[l + t])
				print l, "->", t, ":", distances[l + t]
			print "Total distance:", tot_dist, "\tTotal trips:", len(l1)
			print "=" * 10
			final_array.append(route_array)
			final_distance.append(str(tot_dist))
			#pendiente escribir a un csv el resultado
		final_array = zip(final_array, final_distance)
		final_array = jsonify(pd.Series(final_array).to_json(orient='values'))
	return(final_array)


@app.route("/alldistances_christophides")
def distances_chris():
	gmaps = googlemaps.Client(key=config.api_key_distance_matrix)
	r = requests.get('http://localhost:3004/trucks/companies/:FirstTruckCompany')
	number_transports = 40
	# if working with locations, delimiter equals ','
	with open('./simulation/locations1.csv', 'rb') as csvfile:
		item_reader = csv.reader(csvfile, delimiter='|')
		rows = [row for row in item_reader]
		rows = np.array([[float(row[0]), float(row[1])] for row in rows[1:]])
		distances = []

		start_kmeans_time = time.time()
		kmeans = KMeans(n_clusters=number_transports)
		kmeans = kmeans.fit(rows)
		labels = kmeans.predict(rows)
		centroids = kmeans.cluster_centers_
		end_kmeans_time = time.time()

		total_execution_time = end_kmeans_time - start_kmeans_time;

		labels = np.array(labels)
		final_array = []
		final_distance = []
		for cluster in range(number_transports):
			row_to_write = ''
			document_name = 'cluster_second' + str(cluster)+'.csv'
			#archivo de nodos conectados o resultado
			results_document_name = 'cluster_result_second' + str(cluster)+'.csv'
			with open(document_name,'a') as fd:
				fd.write(row_to_write)
			temp_indices = np.where(labels == cluster)[0].tolist()
			previous_rows = rows[temp_indices].tolist()
			previous_rows.insert(0,[19.434940, -99.195697])
			dm = np.asarray([[{'origin':np.array(x1).flatten(), 'destination':np.array(x2).flatten()} for x2 in previous_rows] for x1 in previous_rows]).flatten()
			times_array = []
			origins = list()
			destinations = list()
			for element in dm: 
				origins.append(element['origin'])
				destinations.append(element['destination'])
			origins_divided = [list(c) for c in mit.divide(len(origins)/5, origins)]
			destinations_divided = [list(c) for c in mit.divide(len(origins)/5, destinations)]
			distance_matrix = []
			for i in range(len(origins_divided)):
				d_mat = gmaps.distance_matrix(origins_divided[i], destinations_divided[i], mode='driving')
				for row in d_mat['rows'][0]['elements']:
					if(row['duration']['value'] != 0):
						distance_matrix.append(row['duration']['value'])
					else:
						distance_matrix.append(1000000)
			distance_matrix = np.array(distance_matrix).reshape(math.sqrt(len(distance_matrix)), math.sqrt(len(distance_matrix))).tolist()
			for i in range(len(distance_matrix[0])):
				for j in range(len(distance_matrix)):
					if(i>=j):
						distance_matrix[i][j]=0
			
			start_christofides_time = time.time()
			tsp = christofides.compute(distance_matrix)
			end_christofides_time = time.time()

			total_execution_time = total_execution_time + (end_christofides_time - start_christofides_time)

			final_array.append(tsp['Christofides_Solution'])
			final_distance.append(tsp['Travel_Cost'])
		final_array = zip(final_array, final_distance)
		print(total_execution_time)
		final_array = jsonify(pd.Series(final_array).to_json(orient='values'))
	return(final_array)

# para correr simulacion con 90 datos cambiar nombre de archivos, quitar el 1
@app.route("/alldistances1")
def distances1():
	gmaps = googlemaps.Client(key=config.api_key_distance_matrix)
	number_transports = 1
	with open('./simulation/locations1.csv', 'rb') as csvfile:
		item_reader = csv.reader(csvfile, delimiter='|')
		rows = [row for row in item_reader]
		rows = np.array([[float(row[0]), float(row[1])] for row in rows[1:]]).tolist()
		distances = []
		final_array = []
		final_distance = []
		row_to_write = ''
		document_name = 'matlab1.csv'
		#archivo de nodos conectados o resultado
		rows.insert(0,[19.434940, -99.195697])
		temp_array = list(itertools.combinations(rows,2))
		origins = list()
		for element in temp_array: 
			origins.append(element[0])
		destinations = list()
		for element in temp_array: 
			destinations.append(element[1])		
		print(temp_array)
		origins_divided = [list(c) for c in mit.divide(len(origins)/5, origins)]
		destinations_divided = [list(c) for c in mit.divide(len(origins)/5, destinations)]
		distance_matrix = []
		for i in range(len(origins_divided)):
			d_mat = gmaps.distance_matrix(origins_divided[i], destinations_divided[i], mode='driving')
			for row in d_mat['rows'][0]['elements']:
				distance_matrix.append(row['duration']['value'])
		final_temp_array = [[temp_array[i][0], temp_array[i][1], distance_matrix[i]] for i in range(len(temp_array))]
		df = pd.DataFrame(final_temp_array)
		df.to_csv('matlab1.csv')

@app.route("/cleandistances")
def distances2():
	with open('./matlab1.csv', 'rb') as csvfile:
		item_reader = csv.reader(csvfile, delimiter=',')
		rows = [row for row in item_reader]
		rows = list(set(np.array([row[1] for row in rows[1:]]).tolist()))
		with open('./simulation/locations1.csv','a') as fd:
				fd.write('Lat|Long|'+ '\n')
		for row in rows:
			with open('./simulation/locations1.csv','a') as fd:
				row_to_write = row.replace('[','').replace(']','').split(',')
				row_to_write = row_to_write[0] + '|' + row_to_write[1] + '\n'
				fd.write(row_to_write)
		


# [[[0,1,6,3,5,4,2,0],14638],
# [[0,2,19,1,5,15,12,13,4,17,16,6,7,3,18,8,11,21,10,20,9,14,0],14382]
# ,[[0,10,1,12,4,5,3,8,11,9,6,7,2,0],9276]
# ,[[0,8,5,6,3,2,9,7,4,1,10,0],11216]
# ,[[0,9,4,2,8,5,10,6,11,1,7,3,0],15765]
# ,[[0,2,8,9,3,6,5,1,7,4,0],16223]
# ,[[0,12,5,10,11,7,1,8,6,2,9,3,4,0],9418]
# ,[[0,18,8,3,5,10,2,20,1,6,12,16,22,13,4,11,17,7,9,14,19,15,21,0],13276]
# ,[[0,4,7,1,2,8,10,3,5,9,6,0],12615]
# ,[[0,4,3,6,1,2,9,10,8,5,12,11,7,0],14988]
# ,[[0,4,1,9,3,7,11,8,6,14,10,2,5,13,12,0],11589]
# ,[[0,8,3,5,9,10,6,2,1,4,7,0],10107]
# ,[[0,5,9,10,7,1,4,8,6,3,2,0],13743]
# ,[[0,12,11,6,9,4,13,2,10,8,3,1,5,7,0],15258]
# ,[[0,10,8,4,6,1,5,9,2,7,3,0],12673]
# ,[[0,2,9,3,4,8,11,1,10,6,5,16,17,13,7,12,15,14,0],15076]
# ,[[0,8,13,9,17,7,11,1,5,10,15,4,3,12,14,2,16,6,0],17910]
# ,[[0,4,9,3,13,11,7,12,10,1,2,8,5,6,0],10983]
# ,[[0,1,4,3,6,8,9,5,7,10,2,0],10607]
# ,[[0,2,13,4,8,10,11,1,3,12,6,9,5,7,0],10368]
# ,[[0,10,1,5,9,2,8,6,7,3,11,4,0],8778]
# ,[[0,7,10,2,3,8,4,1,9,5,6,0],13117]
# ,[[0,8,9,3,1,4,6,2,5,7,0],13357]
# ,[[0,1,2,12,4,8,11,5,9,13,6,10,7,3,14,0],17332]
# ,[[0,9,11,4,14,10,13,3,12,1,6,5,2,8,7,0],14023]
# ,[[0,5,13,8,6,10,11,15,14,1,17,2,12,4,16,18,9,3,7,0],17736]
# ,[[0,8,2,7,1,3,6,4,5,0],12136]
# ,[[0,2,15,14,17,16,6,5,3,8,13,11,1,9,10,4,7,12,0],16228]
# ,[[0,8,11,4,5,10,1,6,2,7,3,9,0],10439]
# ,[[0,9,1,4,15,5,8,2,13,16,14,6,11,10,3,17,7,12,0],11051]
# ,[[0,8,5,6,3,7,15,1,11,4,2,10,12,14,13,9,0],15747]
# ,[[0,8,9,2,14,10,13,1,16,7,12,15,11,4,5,6,3,0],12170]
# ,[[0,1,7,3,2,4,5,6,0],11557]
# ,[[0,3,9,13,4,2,1,7,8,5,10,6,11,12,0],12637]
# ,[[0,9,6,7,11,2,4,3,8,10,1,5,0],12665]
# ,[[0,3,8,6,10,1,7,9,2,5,4,0],14797]
# ,[[0,1,5,7,6,3,9,4,2,8,10,0],16696]
# ,[[0,6,5,9,3,14,2,11,8,4,7,12,10,1,13,0],14393]
# ,[[0,2,7,8,6,1,10,9,5,4,11,3,0],9335]
# ,[[0,1,10,2,12,11,4,6,7,9,8,3,5,0],14251]
# ]

# 17.5471026897

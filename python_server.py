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
import pandas as pd
from sklearn.cluster import KMeans
from collections import deque, namedtuple
import json
import more_itertools as mit
import fileinput
from sets import Set
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

@app.route("/alldistances")
def distances():
	gmaps = googlemaps.Client(key=config.api_key_distance_matrix)
	r = requests.get('http://localhost:3004/trucks/companies/:FirstTruckCompany')
	number_transports = len(r.json())
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
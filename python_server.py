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
app = Flask(__name__)

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
		for cluster in range(number_transports):
			row_to_write = ''
			document_name = 'cluster_' + str(cluster)+'.csv'
			with open(document_name,'a') as fd:
    				fd.write(row_to_write)
			temp_indices = np.where(labels == cluster)[0].tolist()
			print(len(temp_indices), 'cluster length')
			temp_array = list(itertools.combinations(rows[temp_indices].tolist(),2))
			print(len(temp_array), 'combinations length')
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
			final_temp_array = np.array([[temp_array[i][0], temp_array[i][1], distance_matrix[i]] for i in range(len(temp_array))])
			df = pd.DataFrame(final_temp_array)
			df.to_csv(document_name)
	return(jsonify(pd.Series(temp_array).to_json(orient='values')))
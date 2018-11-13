from flask import Flask
import csv
import numpy as np
from flask import jsonify
import math
import requests
from heapq import nsmallest
import pandas as pd
from sklearn.cluster import KMeans
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

@app.route("/alldistances")
def distances():
	r = requests.get('http://localhost:3003/trucks/companies/:FirstTruckCompany')
	number_transports = len(r.json())
    # return "Hello World!"
	with open('./simulation/locations.csv', 'rb') as csvfile:
		item_reader = csv.reader(csvfile, delimiter='|')
		rows = [row for row in item_reader]
		rows = [[float(row[0]), float(row[1])] for row in rows[1:]]
		distances = []
		kmeans = KMeans(n_clusters=number_transports)
		# Fitting the input data
		kmeans = kmeans.fit(rows)
		# Getting the cluster labels
		labels = kmeans.predict(rows)
		# Centroid values
		centroids = kmeans.cluster_centers_
	return jsonify(pd.Series(labels).to_json(orient='values'))
from flask import Flask
import csv
from flask import jsonify
app = Flask(__name__)

@app.route("/algo")
def hello():
    # return "Hello World!"
	with open('./simulation/data.csv', 'rb') as csvfile:
		item_reader = csv.reader(csvfile, delimiter='|')
		rows = [row for row in item_reader]
	return jsonify(rows)
// var address_generation = require('./../prueba_google_maps.js').lat_long_lookup
var api_key_geocoding = require('./../google_api_key.js').api_key_geocoding;
const axios = require('axios');
var fs = require('fs');
var stream = fs.createWriteStream("/home/ricardo/Desktop/listings.csv", {flags:'a'});

// a function that generates a list of items with an address each and characteristics of the item (weight and volume) 

//vamos a hardcodear las coordenadas de la Ciudad de México
const min_lat = 19.197092
const min_lng = -99.424622
const max_lat = 19.577532
const max_lng = -98.888515
var list_items = [];

//todavia esta pendiente salvar en formato csv

const simulation = (min_lat, max_lat, min_lng, max_lng, min_volume, max_volume, min_weight, max_weight, number_items) => {

  var list_of_items = [];
  var list_of_locations = [];
  fs.appendFile('locations.csv', 'Lat|' + 'Long|'+ '\r\n', function (err) {
    if (err) throw err;
    console.log('Saved!');
  });
  for (var i = 0; i < number_items; i++) {
    var lat = Math.random() * (max_lat - min_lat) + min_lat;
    var longt = Math.random() * (max_lng - min_lng) + min_lng;
    var lat_long = lat+','+longt;
    list_of_locations.push(lat_long);
    console.log(lat_long)

    fs.appendFile('locations.csv', lat+'|'+longt + '\r\n', function (err) {
        if (err) throw err;
        console.log('Saved!');
    });

    var promise = new Promise ((resolve, reject) => {
      axios.get('https://maps.googleapis.com/maps/api/geocode/json',{
    	params: {
      	'latlng':lat_long,
      	'key': api_key_geocoding
    	}})
      .then(function(response) {
        resolve(response.data.results[0]['formatted_address']);
      })
      .catch(function(err) {
        reject(err);
      })
    });
    list_of_items.push(promise);
    console.log(list_of_items)
  }
	Promise.all(list_of_items).then(function(item) {
    fs.appendFile('data.csv', 'Address|' + 'Volume|'+ 'Weight' + '\r\n', function (err) {
        if (err) throw err;
        console.log('Saved!');
    });
    item.forEach(function(item) {
      item1 = {}
      item1.address = item;
	  	var volume = Math.random() * (max_volume - min_volume) + min_volume;
	  	var weight = Math.random() * (max_weight - min_weight) + min_weight;
	  	item1.volume = volume;
	  	item1.weight = weight;
     	// list_items.push
     	fs.appendFile('data.csv', item1.address+'|'+item1.volume+'|'+ item1.weight + '\r\n', function (err) {
  			if (err) throw err;
  			console.log('Saved!');
		  });
    });
  })
}

simulation(19.197092, 19.577532, -99.424622, -98.888515, 30, 100, 50, 200, 90);

//Pendiente generar un archivo csv con los tiempos de traslado de todos los nodos.
// Posteriormente armar el grafo con las distancias


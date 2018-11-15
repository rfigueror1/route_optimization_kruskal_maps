var axios = require('axios');
var api_key_distance_matrix = require('./google_api_key.js').api_key_distance_matrix;
var api_key_geocoding = require('./google_api_key.js').api_key_geocoding;

var get_travel_distance_time = function(origin,destination,callback){
	axios.get('https://maps.googleapis.com/maps/api/distancematrix/json',{
    	params: {
      	'origins':origin,
      	'destinations':destination,
      	'key': api_key_distance_matrix
    	}})
  	.then(function (response) {
    	callback(response.data.rows[0].elements[0]['duration']);
  	})
  	.catch(function (error) {
    	console.log(error,'errorzaso');
  	});
}

//https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=YOUR_API_KEY

var address_lookup = function(latlng,callback){
	axios.get('https://maps.googleapis.com/maps/api/geocode/json',{
    	params: {
      	'latlng':latlng,
      	'key': api_key_geocoding
    	}})
  	.then(function (response) {
    	callback(response.data.results[0]);
  	})
  	.catch(function (error) {
    	console.log(error,'errorzaso');
  	});
}

//https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY
var lat_long_lookup = function(address,callback){
  axios.get('https://maps.googleapis.com/maps/api/geocode/json',{
      params: {
        'address':address,
        'key': api_key_geocoding
      }})
    .then(function (response) {
      callback(response.data.results[0]);
    })
    .catch(function (error) {
      console.log(error,'errorzaso');
    });
}

//ejemplo
// var prueba_coordenadas = '40.714224,-73.961452'

// var array = []

// var resultado_prueba = '';
// address_lookup(prueba_coordenadas, function(result){
//   array.push(result.formatted_address);
//   console.log(array)
// });


// get_travel_distance_time('40.714224,-73.961452','40.714224,-73.931452',console.log)

module.exports = {lat_long_lookup:lat_long_lookup, get_travel_distance_time:get_travel_distance_time};
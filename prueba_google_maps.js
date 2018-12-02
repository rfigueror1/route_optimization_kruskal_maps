var axios = require('axios');
var api_key_distance_matrix = require('./google_api_key.js').api_key_distance_matrix;
var api_key_geocoding = require('./google_api_key.js').api_key_geocoding;
var fs = require('fs');

var get_travel_distance_time = function(origin,destination,callback){
	axios.get('https://maps.googleapis.com/maps/api/distancematrix/json',{
    	params: {
      	'origins':origin,
      	'destinations':destination,
      	'key': api_key_distance_matrix
    	}})
  	.then(function (response) {
    	callback(response.data.rows[0].elements[0]['duration']['value']);
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
var prueba_coordenadas1 = '40.714224,-93.961452'
var prueba_coordenadas2 = '40.814224,-93.971452'
// var array = []

// get_travel_distance_time(prueba_coordenadas1, prueba_coordenadas1, console.log)

// var resultado_prueba = '';
// address_lookup(prueba_coordenadas, function(result){
//   array.push(result.formatted_address);
//   console.log(array)
// });

var all_human_array = [
[6,41,71,29,70,52,7,57,31,88,33,24], 
[61,11,78,5,16,32,27,2,67,12,26,85,66,25,10,47],
[56,35,76,17,69,19,90,81],
[30,1,49,34,28,84,39,22,38,36,54,58,62,83,63,60],
[55,73,40,79,82,21,68,51,44,37,74,50,14,80,20,9,64,8,45,43,18],
[59,65,87,89,77,23,4,46,13,15,75,3,53,48,72,86,42]
]

coordinates_depot = '19.43494, -99.195697'

var generate_human_experience = function(array, callback){
  // read file with locations
  fs.readFile('./simulation/locations.csv', (err, data) => {
      if (err) throw err;
      var array = data.toString('utf8').split('\n')
      array = array.map(function(address){
        address = address.replace('\r','').replace(' ', '').split('|')
        return address
      })
      var human_array_coordinates = all_human_array.map((element) => {
        var temp_array = element.map((location) => {
          return(array[location])
        })
        return temp_array;
      })

      var total_time_of_human_route = 0;
      var total_time_of_human_route1 = 0; 
      var counter = 0;
      for (var i = 0; i < human_array_coordinates.length; i++) {
        for (var j = 0; j< human_array_coordinates[i].length-1; j++){
          //falta agregar el depot de ida al primero y de regreso al ultimo
           var origin = human_array_coordinates[i][j][0] + ',' + human_array_coordinates[i][j][1]
           var destination = human_array_coordinates[i][j+1][0] + ',' + human_array_coordinates[i][j+1][1]
           get_travel_distance_time(origin,
           destination, (response) => {
              total_time_of_human_route = total_time_of_human_route + response;
              counter = counter + 1
              console.log(total_time_of_human_route);
              console.log(counter)
           })
           if(j === 0){
            get_travel_distance_time(
            coordinates_depot,
            origin, (response) => {
            total_time_of_human_route = total_time_of_human_route + response;
            counter = counter + 1
            })
           }

           if(j === human_array_coordinates[i].length-2){
            get_travel_distance_time(
            destination,
            coordinates_depot, (response) => {
            total_time_of_human_route = total_time_of_human_route + response;
            counter = counter + 1
            })
           }
        }
      } 
  });
}

// generate_human_experience(all_human_array, console.log);

module.exports = {lat_long_lookup:lat_long_lookup, get_travel_distance_time:get_travel_distance_time};
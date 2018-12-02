var express = require('express');
var app = express();
var db = require('./../db/db.js')
var calc_time = require('./../prueba_google_maps.js').get_travel_distance_time
var fs = require('fs');
const bodyParser = require('body-parser'); //to parse json that comes in the body of the request


app.use(express.static(__dirname + '/../dist'));

app.use(bodyParser.json());

app.get('/', function(req, res){
  res.send('hello world1');
});

app.post('/trucks', function(req, res){
  var lat = req.params.lat;
  var lng = req.params.lng;
  var text = req.params.text;
  var company = req.params.company;
  db.create_transport(lat, lng, text, company, (err,res) => {
  	if(err){
  		console.log(err)
  	}else{
  		res.status(201).send();
  	}
  })
});

app.get('/trucks/:id', function(req, res){
  var id = Number(req.params.id.replace(':',''));
  db.locate_transport(id, (err,results) => {
    if(err){
      console.log(err)
    }else{
      res.json(results);
    }
  })
});

app.get('/trucks/companies/:company', function(req, res){
  var company = req.params.company.replace(':','');
  db.show_ids_company(company, (err,results) => {
    if(err){
      console.log(err)
    }else{
      res.json(results);
    }
  })
});

app.get('/time', function(req, res){
  var lat1 = req.body.lat1;
  var lng1 = req.body.lng1;
  var lat2 = req.body.lat2;
  var lng2 = req.body.lng2;
  var origins = lat1 + ',' + lng1
  var destinations = lat2 + ',' + lng2
  // calculate time using function from pruebla google maps
  calc_time(origins, destinations, (err,results) => {
    if(err){
      console.log(err)
    }else{
      res.json(results);
    }
  })
});

app.get('/items', function(req, res){
  fs.readFile('./simulation/data.csv', (err, data) => {
      if (err) throw err;
      //pendiente transformar datos a arreglo
      var array = data.toString('utf8').split('\n')
      // split array items by address
      array = array.map(function(address){
        address = address.split('|')[0]
        return address
      })
      res.json(array);
    });
});

app.get('/locations', function(req, res){
  fs.readFile('./simulation/locations.csv', (err, data) => {
      if (err) throw err;
      //pendiente transformar datos a arreglo
      var array = data.toString('utf8').split('\n')
      // split array items by address
      array = array.map(function(location){
        location = location.split('|')
        return location
      })
      res.json(array);
    });
});

app.put('/trucks:id', function(req, res){
  var id = Number(req.params.id.replace(':',''));
  var lat = req.body.lat;
  var lng = req.body.lng;
  db.update_transport(id, lat, lng, (err,results) => {
    if(err){
      console.log(err)
    }else{
      res.status(200).send();
    }
  })
});

app.listen(3004);

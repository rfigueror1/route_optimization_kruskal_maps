var express = require('express');
var app = express();
var db = require('./../db/db.js')
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

app.listen(3003);

var express = require('express');
var app = express();

app.use(express.static(__dirname + '/../dist'));

app.get('/', function(req, res){
  res.send('hello world1');
});

app.listen(3003);

var mongoose = require('mongoose');
var AutoIncrement = require('mongoose-auto-increment')

mongoose.connect('mongodb://localhost/transportation');

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
  // we're connected!
});

var transport_schema = new mongoose.Schema({
  name: String,
  lat: Number,
  longitud: Number,
  company: String
});

AutoIncrement.initialize(db);

transport_schema.plugin(AutoIncrement.plugin, 'transport');

var Transport = mongoose.model('Camiones', transport_schema);

var locate_transport = function(id, callback){
	Transport.find({_id:id}).exec(callback);
}

var show_ids_company = function(company, callback){
	Transport.find({company:company}).exec(callback);
}

var create_transport = function(name, lat, longitud, company, callback){
	var temp = new Transport({ name:name, lat:lat, longitud:longitud, company:company});
	temp.save(function (err, temp) {
    if (err) return console.error(err);
    else return console.log('element saved')
  });
}

var update_transport = function(id, lat, longitud, callback){
	console.log(lat);
	Transport.where({_id:id}).update({$set: {lat:Number(lat),longitud:Number(longitud)}}).exec(callback)
}

module.exports = {locate_transport, create_transport, update_transport}; 

// update_transport(1, -35.871852, 153.222652, console.log);
// locate_transport(1, console.log);
show_ids_company('FirstTruckCompany', console.log);

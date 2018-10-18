var mongoose = require('mongoose');
var AutoIncrement = require('mongoose-auto-increment')

mongoose.connect('mongodb://localhost/transportation');

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
  // we're connected!
});

var transport_schema = new mongoose.Schema({
  lat: Number,
  lng: Number,
  text: String,
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

var create_transport = function(lat, lng, text, company, callback){
	var temp = new Transport({ lat:lat, lng:lng, text:text, company:company});
	temp.save(function (err, temp) {
    if (err) return console.error(err);
    else return console.log('element saved')
  });
}

var update_transport = function(id, lat, lng, callback){
	Transport.where({_id:id}).update({$set: {lat:Number(lat),lng:Number(lng)}}).exec(callback)
}

module.exports = {locate_transport, create_transport, update_transport, show_ids_company}; 

// update_transport(1, -35.871852, 153.222652, console.log);
// locate_transport(1, console.log);
//show_ids_company('FirstTruckCompany', console.log);

create_transport(19.434940, -99.195697, 'Ricardo Figueroa', 'FirstTruckCompany') 
create_transport(19.434940, -99.205697, 'Alfredo Carrillo', 'FirstTruckCompany')
create_transport(19.434940, -99.205697, 'Gary', 'FirstTruckCompany')
# Logistics planning and monitoring app

Follow these instructions to start the application:

1. Get your own API key from the following and subsitute when requested (for security reasons, be careful not to push your API keys, include the files with the keys in gitignore file):
	- Google Maps Distance Matrix (api_key_distance_matrix)
	- Google Maps Geocoding (api_key_geocoding)
	- Google Maps API (api_key_maps)
2. Run `npm install`.
3. Run `npm run compile`.
4. Run `npm run start`.
5. Visit localhost:3003 

Curl commands to test REST API

GET: `curl -d '{}' -H "Content-Type: application/json" -X GET http://localhost:3003/trucks/:1`

POST: `curl -d '{"name":"third_truck", "lat":"-33.871852", "longitud":"150.000", "company":"SecondTruckCompant"}' -H "Content-Type: application/json" -X POST http://localhost:3003/trucks`

PUT: `curl -d '{"_id":"1", "lat":"-40.871852", "longitud":"150.000"}' -H "Content-Type: application/json" -X PUT http://localhost:3003/trucks:1`


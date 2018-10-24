Logistics planning and monitoring app

Curl commands to test REST API

GET: `curl -d '{}' -H "Content-Type: application/json" -X GET http://localhost:3003/trucks/:1`

POST: `curl -d '{"name":"third_truck", "lat":"-33.871852", "longitud":"150.000", "company":"SecondTruckCompant"}' -H "Content-Type: application/json" -X POST http://localhost:3003/trucks`

PUT: `curl -d '{"_id":"1", "lat":"-40.871852", "longitud":"150.000"}' -H "Content-Type: application/json" -X PUT http://localhost:3003/trucks:1`

Follow these instructions to start the application:

1. Run `npm install`.
2. Run `npm run compile`.
3. Run `npm run start`.
4. Visit localhost:3003 
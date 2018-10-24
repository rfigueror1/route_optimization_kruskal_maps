var api_key_geocoding = require('./../prueba_google_maps.js').get_travel_distance_time;
var fs = require('fs');
var stream = fs.createWriteStream("/home/ricardo/Desktop/listings.csv");

// Instantiate a new graph
var Graph = function() {
  this.list = {};
  this.vertices = {};
}; 

// Add a node to the graph, passing in the node's value
// Time complexity is O(1)
Graph.prototype.addNode = function(node, object) {
  // create an empty node
  this.list[node] = object;
};

// Return a boolean value indicating if the value passed to contains is represented in the graph.
// Pendiente arreglar estas funciones para usar en el algoritmos
Graph.prototype.contains = function(node) {
  //console.log('node is: ', node);
  var result = false;
  for (key in this.list) {
    //console.log(key, typeof key);
    if (key === JSON.stringify(node)) {
      result = true;
    }
  }
  return result;
};
 
// Removes a node from the graph.
// Pendiente arreglar estas funciones para usar en el algoritmos
Graph.prototype.removeNode = function(node) {
  delete this.list[node];
  // nested for loops
  for (key in this.list) {
    for(var i = 0 ; i<this.list[key].length ; i++) {
      if(this.list[key][i] === node){
        this.list[key].splice(i,1);
      }
    }
  }
};

// Returns a boolean indicating whether two specified nodes are connected.  Pass in the values contained in each of the two nodes.
// Pendiente arreglar estas funciones para usar en el algoritmos
Graph.prototype.hasEdge = function(fromNode, toNode) {
  var result = false;
  for(var i = 0; i<this.list[fromNode].length; i++){
    if(this.list[fromNode][i] === toNode){
      result = true;
    }
  }
  return result;  
};

// assynchronous code connecting to nodes and assigning a time between them
// pendiente arreglar algunos bugs.
// Connects two nodes in a graph by adding an edge between them.
Graph.prototype.addEdge = function(fromNode, toNode, time) {
    this.vertices[fromNode+'-'+toNode] = time;
    this.list[fromNode]['edges'].push(toNode);
    this.list[toNode]['edges'].push(fromNode);
 };

// Remove an edge between any two specified (by value) nodes.
// Pendiente arreglar estas funciones para usar en el algoritmos
Graph.prototype.removeEdge = function(fromNode, toNode) {
  var indexOfFromNode = 0;
  var indexOfToNode = 0;
  for(var i = 0; i<this.list[fromNode].length; i++){
    if(this.list[fromNode][i] === toNode){
      indexOfFromNode = i;
    }
  }
  for(var j = 0; j<this.list[toNode].length; j++){
    if(this.list[toNode][j] === fromNode){
      indexOfToNode = j;
    }
  }
  
  this.list[fromNode].splice(indexOfFromNode,1);
  this.list[toNode].splice(indexOfToNode,1);
};

// Pass in a callback which will be executed on each node of the graph.
Graph.prototype.forEachNode = function(cb) {
  for (let key in this.list) {
    cb(this.list[key]);
  }
};
/*
 * Complexity: The time complexity associated with each function is the following:
 *  - AddNode: O(1)
 *  - Contains: O(n)
 *  - removeNode: Either O(n2) or close O(n*m), depending on the connections (m) associated with each node n. 
 *  - hasEdge: O(n)
 *  - addEdge: O(1)
 *  - removeEdge: O(n)
 *  - forEachNode: O(n)*O(cb), depending on the complexity of callback
 */
var newGraph = new Graph();
// console.log(newGraph);
// newGraph.addNode({item_id:1, address:"Av 565 145, San Juan de Aragón II Secc, 07969 Ciudad de México, CDMX, Mexico", weigth:61.56368733308043,volume: 105.5834116909949})
var a1 = {item_id:1, address:"Av 565 145, San Juan de Aragón II Secc, 07969 Ciudad de México, CDMX, Mexico", weigth:61.56368733308043,volume: 105.5834116909949, edges:[]}
newGraph.addNode("a", a1)

var a2 = {item_id:2, address:"Av. Lomas de San Juan 21, 52768 San Juan Yautepec, Méx., Mexico", weigth:43.89042755363508,volume: 123.71103296818373, edges:[]}
newGraph.addNode("b", a2)
newGraph.addEdge('a','b', 5);
console.log(newGraph, 'newGraph');

// var a3 = {item_id:3, address:"Tetetixtla 14, Tenorios, 09680 Ciudad de México, CDMX, Mexico", weigth:98.48386593022796,volume: 98.71386891202096, edges:[]}
// newGraph.addNode("c", a3)
// newGraph.addEdge('b','c');
// console.log(newGraph);
// newGraph.forEachNode(console.log);

// console.log(newGraph.list[newGraph.list['a']['edges'][0]]['address']);


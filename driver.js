const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

var MongoClient = require('mongodb').MongoClient;

MongoClient.connect("mongodb://Team11:zuqXM5saOsbd4DOr@cluster0-shard-00-00-ppp7l.mongodb.net:27017,cluster0-shard-00-01-ppp7l.mongodb.net:27017,cluster0-shard-00-02-ppp7l.mongodb.net:27017/Team11DB?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin", function(err, db) {

  if(err) { return console.dir(err); }

  console.log(db);
});

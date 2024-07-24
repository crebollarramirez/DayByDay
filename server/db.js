// server/db.js
require('dotenv').config();
const { MongoClient, ServerApiVersion } = require('mongodb');
const uri = "mongodb+srv://chris:<Avanza55>@daybydaydb.pachivt.mongodb.net/?retryWrites=true&w=majority&appName=daybydayDB";

// Create a MongoClient with a MongoClientOptions object to set the Stable API version
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});

async function connectToDatabase() {
  try {
    // Connect the client to the server
    await client.connect();
    // Send a ping to confirm a successful connection
    await client.db("admin").command({ ping: 1 });
    console.log("Pinged your deployment. You successfully connected to MongoDB!");
  } catch (error) {
    console.error("Error connecting to MongoDB:", error);
  }
}

function getClient() {
  return client;
}

module.exports = { connectToDatabase, getClient };
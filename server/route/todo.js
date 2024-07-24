// server/routes/todo.js
const express = require('express');
const { getClient } = require('../db');
const router = express.Router();

router.get('/', async (req, res) => {
  try {
    const client = getClient();
    const db = client.db('daybydayDB'); // Replace with your database name
    const todos = await db.collection('todos').find().toArray();
    res.json(todos);
  } catch (error) {
    console.error("Error fetching todos:", error);
    res.status(500).send("Error fetching todos");
  }
});

module.exports = router;
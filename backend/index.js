const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

// Example: Get all chores
app.get('/api/chores', async (req, res) => {
  const result = await pool.query('SELECT * FROM chores ORDER BY id');
  res.json(result.rows);
});

// Example: Add a chore
app.post('/api/chores', async (req, res) => {
  const { task, assignee, points } = req.body;
  const result = await pool.query(
    'INSERT INTO chores (task, assignee, points, completed) VALUES ($1, $2, $3, $4) RETURNING *',
    [task, assignee, points, false]
  );
  res.json(result.rows[0]);
});

// Add similar endpoints for meals, settings, grocery_list, etc.

app.listen(3000, () => {
  console.log('Backend listening on port 3000');
});
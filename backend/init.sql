CREATE TABLE IF NOT EXISTS chores (
  id SERIAL PRIMARY KEY,
  task TEXT NOT NULL,
  assignee TEXT,
  points INTEGER,
  completed BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS meals (
  day TEXT PRIMARY KEY,
  meal TEXT
);

CREATE TABLE IF NOT EXISTS settings (
  key TEXT PRIMARY KEY,
  value TEXT
);
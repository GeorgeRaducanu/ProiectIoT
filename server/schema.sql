DROP TABLE IF EXISTS measurements;

CREATE TABLE measurements (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  current_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  temperature REAL,
  humidity REAL
);
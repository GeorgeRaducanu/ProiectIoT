DROP TABLE IF EXISTS measurements;

CREATE TABLE measurements (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  temperature REAL,
  humidity REAL
);
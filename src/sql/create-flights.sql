CREATE SCHEMA public;

CREATE TABLE Airport
( callsign VARCHAR(3) NOT NULL,
  city VARCHAR(128) NOT NULL,
  name VARCHAR(256) NOT NULL,
  PRIMARY KEY(callsign)
);

CREATE TABLE Ticket
( to VARCHAR(3) REFERENCES callsign NOT NULL,
  from VARCHAR(3) REFERENCES callsign NOT NULL,
  booking_time TIMESTAMP REFERENCES  NOT NULL,

);
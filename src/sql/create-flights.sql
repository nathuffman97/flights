-- Database: fights

-- DROP DATABASE fights;

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE Airport
( callsign VARCHAR(3) NOT NULL,
  city VARCHAR(128) NOT NULL,
  name VARCHAR(256) NOT NULL,
  PRIMARY KEY(callsign)
);

CREATE TABLE People
( id INTEGER NOT NULL,
  username VARCHAR(128) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT positive_id CHECK (
    id > 0
  ),
  -- Don't store data that might be malicious
  CONSTRAINT second_order_injection_stopper CHECK (
    username NOT LIKE '%''%'
 )
);

CREATE TABLE Airline
( id INTEGER NOT NULL,
  name VARCHAR(64) UNIQUE NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Flight
( id NUMERIC(20) NOT NULL,
  flight_code VARCHAR(32) NOT NULL,
  depart_time TIMESTAMP NOT NULL,
  arrive VARCHAR(3) REFERENCES Airport(callsign) NOT NULL,
  depart VARCHAR(3) REFERENCES Airport(callsign) NOT NULL,
  carrier VARCHAR(64) REFERENCES Airline(name) NOT NULL,
  UNIQUE(flight_code, depart_time),
  PRIMARY KEY(id)
);


CREATE TABLE Trip
( id NUMERIC(20) NOT NULL,
  booking_date DATE NOT NULL,
  price FLOAT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT positive_id CHECK(
    id > 0
  ),
  CONSTRAINT positive_price CHECK (
    price > 0
  )
);

CREATE TABLE ConnectingFlight
( trip_id NUMERIC(20) REFERENCES Trip(id) NOT NULL,
  flight_id NUMERIC(20) REFERENCES Flight(id) NOT NULL,
  PRIMARY KEY (trip_id, flight_id)
);

CREATE TABLE TripTaker
( pid INTEGER REFERENCES People(id) NOT NULL,
  tid INTEGER REFERENCES Trip(id) NOT NULL,
  PRIMARY KEY (pid, tid)
);

INSERT INTO Airline VALUES
  (0, 'Alaskan Airlines'),
  (1, 'Allegiant Air'),
  (2, 'American Airlines'),
  (3, 'Delta Airlines'),
  (4, 'Frontier Airlines'),
  (5, 'Hawaiian Airlines'),
  (6, 'Jet Blue'),
  (7, 'Spirit Airlines'),
  (8, 'United Airlines'),
  (9, 'Virgin America');

INSERT INTO People VALUES
  (1, 'ze'),
  (2, 'ml55'),
  (3, 'hh1');

INSERT INTO Airport VALUES
  ('RDU', 'Raleigh', 'Raleigh-Durham Intl Airport'),
  ('LAX', 'Los Angeles', 'Los Angeles Intl Airport'),
  ('LGA', 'New York City', 'Laguardia Intl Airport');

INSERT INTO Trip VALUES
  (11, '2017-10-12', 200),
  (22, '2017-10-12', 400),
  (33, '2017-08-16', 300);

INSERT INTO TripTaker VALUES
  (2, 11),
  (1, 22),
  (3, 33);

INSERT  INTO  Flight VALUES
  (0, 'XX1', '2017-12-15 01:30:00', 'RDU', 'LGA', 'American Airlines'),
  (1, 'XX3', '2017-12-15 16:00:00', 'RDU', 'LGA', 'United Airlines'),
  (2, 'XX4', '2017-12-15 13:00:00', 'RDU', 'LAX', 'American Airlines');

INSERT INTO ConnectingFlight VALUES
  (11, 0),
  (22, 1),
  (33, 2);


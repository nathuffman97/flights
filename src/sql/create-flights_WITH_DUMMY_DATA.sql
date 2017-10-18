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
  tid NUMERIC(20) REFERENCES Trip(id) NOT NULL,
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

INSERT INTO Airport VALUES
  ('RDU', 'Raleigh', 'Raleigh-Durham Intl Airport'),
  ('JFK', 'New York City', 'John F. Kennedy Intl Airpot'),
  ('LGA', 'New York City', 'LaGuardia Airport'),
  ('IAD', 'Washington, DC', 'Washington Dulles Intl Airport'),
  ('LAX', 'Los Angeles', 'Los Angeles Intl Airport'),
  ('SFO', 'San Francisco', 'San Francisco Itnl Airport'),
  ('DFW', 'Dallas', 'Dallas-Fort Worth Intl Airport'),
  ('MIA', 'Miami', 'Miami Intl Airport'),
  ('LHR', 'London', 'London Heathrow Intl Airport'),
  ('PVG', 'Shanghai', 'Shanghai Pudong Intl Airport'),
  ('PEK', 'Beijing', 'Beijing Capital Intl Airport'),
  ('ORD', 'Chicago', 'Chicago O''Hare Intl Airport'),
  ('SAN', 'San Diego', 'San Diego Intl Airport');

INSERT INTO People VALUES
  (1, 'ze'),
  (2, 'ml55'),
  (3, 'hh1');

INSERT INTO Trip VALUES
  (11, '2017-10-12', 200),
  (12, '2017-10-12', 150),
  (22, '2017-10-12', 400),
  (33, '2017-08-16', 300);

INSERT INTO TripTaker VALUES
  (2, 11),
  (2, 12),
  (1, 22),
  (1, 33),
  (3, 33);

INSERT  INTO  Flight VALUES
  (0, 'XX1', '2017-12-15 01:30:00', 'LGA', 'RDU', 'American Airlines'),
  (1, 'XX3', '2017-12-15 16:00:00', 'LGA', 'RDU', 'United Airlines'),
  (2, 'XX4', '2017-12-15 13:00:00', 'LAX', 'RDU', 'American Airlines'),
  (3, 'XX5', '2017-12-16 14:00:00', 'LAX', 'RDU', 'American Airlines');

INSERT INTO ConnectingFlight VALUES
  (11, 0),
  (11, 1),
  (12, 0),
  (12, 1),
  (22, 1),
  (33, 0);


--Get flight options for the day 12/15/2017 for RDU -> LGA
SELECT * FROM Flight WHERE depart_time BETWEEN '2017-12-15 00:00:00' AND '2017-12-15 23:59:59'
  AND depart = 'RDU' AND arrive = 'LGA';

--Get flight information for a user's (ze) trips
SELECT flight_code, depart, arrive, depart_time, carrier, price FROM Flight, Trip, ConnectingFlight, People, TripTaker
  WHERE People.username = 'ze' AND People.id = TripTaker.pid AND TripTaker.tid = Trip.id AND
        Flight.id = ConnectingFlight.flight_id AND Trip.id = ConnectingFlight.trip_id;

-- Select all people for a given flight
SELECT DISTINCT username FROM People, TripTaker, Trip, ConnectingFlight, Flight WHERE
  Flight.flight_code = 'XX3' AND Flight.depart_time BETWEEN '2017-12-15 00:00:00' AND '2017-12-15 23:59:59'
  AND Flight.id = ConnectingFlight.flight_id AND ConnectingFlight.trip_id = Trip.id AND Trip.id = TripTaker.tid
  AND TripTaker.pid = People.id;






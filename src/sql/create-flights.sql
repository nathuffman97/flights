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

CREATE TABLE Flight
( flight_code VARCHAR(32) NOT NULL,
  depart_time TIMESTAMP NOT NULL,
  arrive VARCHAR(3) REFERENCES Airport(callsign) NOT NULL,
  depart VARCHAR(3) REFERENCES Airport(callsign) NOT NULL,
  carrier VARCHAR(64) REFERENCES Airline(name) NOT NULL,
  PRIMARY KEY(flight_code, depart_time)
);

CREATE TABLE ConnectingFlight
( trip_id INTEGER REFERENCES Trip(id) NOT NULL,
  flight_code VARCHAR(32) REFERENCES Flight(flight_code) NOT NULL,
  depart_time TIMESTAMP REFERENCES Flight(depart_time) NOT NULL,
  PRIMARY KEY (trip_id, flight_code, depart_time)
);

CREATE TABLE Trip
( id NUMERIC(20) NOT NULL,
  booking_date DATE NOT NULL,
  price FLOAT NOT NULL,
  occupant_age VARCHAR(6) NOT NULL,
  seat_class VARCHAR(5) NOT NULL,
  refundable BOOLEAN NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT positive_id CHECK(
    id > 0
  ),
  CONSTRAINT positive_price CHECK (
    price > 0
  ),
  CONSTRAINT seat_exists CHECK(
    seat_class IN ('first', 'coach')
  ),
  CONSTRAINT avail_ages CHECK (
    occupant_age IN ('child', 'adult', 'senior')
  )
);

CREATE TABLE TripTaker
( uid INTEGER REFERENCES People(id) NOT NULL,
  tid INTEGER REFERENCES Trip(id) NOT NULL,
  PRIMARY KEY (uid, tid)
);

CREATE TABLE Airline
( id INTEGER NOT NULL,
  name VARCHAR(64) NOT NULL,
  PRIMARY KEY (id)
);
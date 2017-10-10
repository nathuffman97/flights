CREATE SCHEMA public;

CREATE TABLE Airport
( callsign VARCHAR(3) NOT NULL,
  city VARCHAR(128) NOT NULL,
  name VARCHAR(256) NOT NULL,
  PRIMARY KEY(callsign)
);

CREATE TABLE Plane
( depart_time TIMESTAMP NOT NULL,
  arrive VARCHAR(3) REFERENCES Airport(callsign) NOT NULL,
  depart VARCHAR(3) REFERENCES Airport(callsign) NOT NULL,
  carrier VARCHAR(64) NOT NULL,
  PRIMARY KEY(depart_time, arrive, depart)
);

CREATE TABLE Ticket
( arrive VARCHAR(3) REFERENCES Plane(arrive) NOT NULL,
  depart VARCHAR(3) REFERENCES Plane(depart) NOT NULL,
  depart_time TIMESTAMP REFERENCES Plane(depart_time) NOT NULL,
  booking_date DATE NOT NULL,
  price FLOAT NOT NULL,
  occupant_age VARCHAR(6) NOT NULL,
  seat_class VARCHAR(5) NOT NULL,
  refundable BOOLEAN NOT NULL,
  PRIMARY KEY(arrive, depart, depart_time, booking_date,
              occupant_age, seat_class, refundable)
);
-- Queries from task 5, modified slightly to reflect actual data scrapped from the web.
-- @author Matt Dickson

--Get flight options for the day 12/15/2017 for RDU -> SAN
SELECT DISTINCT flight_code FROM Flight, trip, connectingflight WHERE depart_time BETWEEN '2017-12-15 00:00:00' AND '2017-12-15 23:59:59'
AND origin = 'RDU' AND destination = 'SAN' AND connectingflight.trip_id = trip.id AND flight.id = connectingflight.flight_id;

--Get all flight information for a user's (Matt) trips
SELECT flight_code, depart, arrive, depart_time, carrier, price FROM Flight, Trip, ConnectingFlight, People, TripTaker
WHERE People.username = 'Matt' AND People.id = TripTaker.pid AND TripTaker.tid = Trip.id AND
Flight.id = ConnectingFlight.flight_id AND Trip.id = ConnectingFlight.trip_id;

-- Select all people for a given flight
SELECT DISTINCT username FROM People, TripTaker, Trip, ConnectingFlight, Flight WHERE
Flight.flight_code = 'UA2381' AND Flight.depart_time BETWEEN '2017-12-15 00:00:00' AND '2017-12-15 23:59:59'
AND Flight.id = ConnectingFlight.flight_id AND ConnectingFlight.trip_id = Trip.id AND Trip.id = TripTaker.tid
AND TripTaker.pid = People.id;

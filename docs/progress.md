# Application Description
Our goal is to create an app that makes it cheaper for Duke students to book flights back home for breaks. Using the Google QPX Express API, we want to create a database of prices of flights between Raleigh and big cities in the US and Europe. We also plan to use Department of Transportation data to back-populate the database. The students would be able to query this database to find out what day of the year should they buy their ticket back home for winter break, for example. 
# Data Population Plan
The Google API can take 3 parameters (among many others): origin, destination and date. We limit our searches to one-way tickets. The response we get is a list of flights for the all days between the requested date and the current date with their historical average or minimum prices prices. For example, if a user queries the database on July 7th looking for a plane ticket on August 3rd, the database will respond with the average ticket price on each data between July 7th and August 3rd. Our goal would be to track how prices change for a single destination on a given date over several months, weeks, or days before the flight date to visually show users trends in airline ticket prices.
The full sample data can be seen in create-flights.sql, which also contains the SQL code for creating tables, constraints, etc. This file can be found in the attached .zip file. A few lines of example sample data are below.  

INSERT INTO Airline VALUES  
(0, 'Alaskan Airlines'),  
(1, 'Delta Airlines');
INSERT INTO Trip VALUES  
(11, '2017-10-12', 200);
INSERT INTO Flight VALUES  
(0, 'XX1', '2017-12-15 01:30:00', 'LGA', 'RDU', 'Delta Airlines');

Additionally, we have solidified our list of cities to consider: New York (JFK, LGA), DC, LA, San Francisco, Dallas/Fort Worth, Miami, London, Shanghai, Beijing, Chicago, and San Diego. Similarly, the dates we are checking are on either side of winter break, thanksgiving, and spring break, and after spring finals.
# Assumptions
Nothing can be null.  
For the table People, all id values must be greater than zero, and the username cannot contain quote marks to eliminate possible malicious data.  
For the table Airlines, id is the primary key but name must be unique.  
For the table Flight, arrive and depart are foreign keys both referencing Airport.callsign. carrier is similarly a foreign key referencing Airline.name. The flight_code and depart_time must form a unique pair.  
For the table Trip, id values and prices must be greater than zero.  
For the table ConnectingFlight, trip_id is a foreign key referencing Trip.id and flight_id is a foreign key referencing Flight.id.  
For the table TripTaker, pid is a foreign key referencing People.id and tid is a foreign key referencing Trip.id.  
# Database Tables
Airport (__callsign__, city, name)  
People (__id__, username)  
Airline (__id__, name)  
Flight (__id__, flight_code, depart_time, arrive, depart, carrier)  
Trip (__id__, booking_date, price)  
ConnectingFlight (__trip_id__, __flight_id__)  
TripTaker (__pid__, __tid__)  
# Interface Description
When the user opens the app, they will see a banner at the top of the page with the name of the app (to be determined) and four input fields: two string inputs and two date inputs. These inputs Are labeled as and correspond with Departure Destination, Arrival Destination, and the start and end of the date range in which the user would like to book their flight. Once the user has entered this information, the app will process the query and then display the outcome to the user. The outcome will take the form of an estimated lowest price and the flight(s) necessary for the user to reach their destination for that price. This can be one or multiple flights depending on if the user has to take a layover to pay the cheapest price for their trip.
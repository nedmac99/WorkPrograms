digraph {
	rankdir=LR size=8
	Passenger [label="Passenger
- PassengerID (PK)
- FirstName
- LastName
- Age" shape=box]
	Airline [label="Airline
- AirlineID (PK)
- Name
- Concourse" shape=box]
	Flight [label="Flight
- FlightID (PK)
- FlightNumber
- AirlineID (FK)
- DepartureAirportCode
- ArrivalAirportCode
- DepartureDateTime
- ArrivalDateTime" shape=box]
	CheckIn [label="CheckIn
- CheckInID (PK)
- PassengerID (FK)
- FlightID (FK)
- CheckInDateTime" shape=box]
	Passenger -> CheckIn [label="1 to many"]
	Flight -> CheckIn [label="1 to many"]
	Airline -> Flight [label="1 to many"]
}

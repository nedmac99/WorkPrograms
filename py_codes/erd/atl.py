import graphviz

# Define the ERD diagram
erd = graphviz.Digraph(format='png')
erd.attr(rankdir='LR', size='8')

# Entities
erd.node('Passenger', '''Passenger
- PassengerID (PK)
- FirstName
- LastName
- Age''', shape='box')

erd.node('Airline', '''Airline
- AirlineID (PK)
- Name
- Concourse''', shape='box')

erd.node('Flight', '''Flight
- FlightID (PK)
- FlightNumber
- AirlineID (FK)
- DepartureAirportCode
- ArrivalAirportCode
- DepartureDateTime
- ArrivalDateTime''', shape='box')

erd.node('CheckIn', '''CheckIn
- CheckInID (PK)
- PassengerID (FK)
- FlightID (FK)
- CheckInDateTime''', shape='box')

# Relationships
erd.edge('Passenger', 'CheckIn', label='1 to many')
erd.edge('Flight', 'CheckIn', label='1 to many')
erd.edge('Airline', 'Flight', label='1 to many')

# Render the diagram
erd.render('erd_passenger_checkin', cleanup=True)
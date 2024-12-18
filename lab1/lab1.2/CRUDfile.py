from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from ORMfile import setup_database, create_session, Flights, AircraftsData, Bookings, Tickets, AirportsData, TicketFlights

# Инициализация базы данных
engine = setup_database("sqlite:///travel.sqlite")
session = create_session(engine)

# CREATE (Создание)
def add_flight(flight_no, scheduled_departure, scheduled_arrival, departure_airport, arrival_airport, status, aircraft_code, actual_departure, actual_arrival):
    new_flight = Flights(
        flight_no=flight_no,
        scheduled_departure=scheduled_departure,
        scheduled_arrival=scheduled_arrival,
        departure_airport=departure_airport,
        arrival_airport=arrival_airport,
        status=status,
        aircraft_code=aircraft_code,
        actual_departure=actual_departure,
        actual_arrival=actual_arrival
    )
    session.add(new_flight)
    session.commit()
    print(f"Flight '{flight_no}' added with ID: {new_flight.flight_id}")
    return new_flight.flight_id

def add_aircraft(aircraft_code, model, range):
    new_aircraft = AircraftsData(aircraft_code=aircraft_code, model=model, range=range)
    session.add(new_aircraft)
    session.commit()
    print(f"Aircraft '{model}' added with code: {new_aircraft.aircraft_code}")
    return new_aircraft.aircraft_code

def add_booking(book_ref, book_date, total_amount):
    new_booking = Bookings(book_ref=book_ref, book_date=book_date, total_amount=total_amount)
    session.add(new_booking)
    session.commit()
    print(f"Booking '{book_ref}' added with total amount: {new_booking.total_amount}")
    return new_booking.book_ref

def add_ticket(ticket_no, book_ref, passenger_id):
    new_ticket = Tickets(ticket_no=ticket_no, book_ref=book_ref, passenger_id=passenger_id)
    session.add(new_ticket)
    session.commit()
    print(f"Ticket '{ticket_no}' added for passenger: {new_ticket.passenger_id}")
    return new_ticket.ticket_no

# READ (Чтение)
def get_flight_by_id(flight_id):
    flight = session.query(Flights).filter_by(flight_id=flight_id).first()
    if flight:
        print(f"Flight ID: {flight.flight_id}, Flight No: {flight.flight_no}, Status: {flight.status}")
        return flight
    else:
        print(f"Flight with ID {flight_id} not found.")
        return None

def get_tickets_by_booking(book_ref):
    tickets = session.query(Tickets).filter_by(book_ref=book_ref).all()
    print(f"Tickets for Booking Ref {book_ref}:")
    for ticket in tickets:
        print(f"- Ticket No: {ticket.ticket_no}, Passenger ID: {ticket.passenger_id}")
    return tickets

def get_aircraft_inf(aircraft_code):
    aircraft = session.query(AircraftsData).filter_by(aircraft_code=aircraft_code).first()
    if aircraft:
        print(f"Aircraft Code: {aircraft.aircraft_code}, Model: {aircraft.model}, Range: {aircraft.range}")
        return aircraft
    else:
        print(f"Aircraft with code {aircraft_code} not found.")
        return None

def get_airport_inf(airport_code):
    airport = session.query(AirportsData).filter_by(airport_code=airport_code).first()
    if airport:
        print(f"Airport Code: {airport.airport_code}, Name: {airport.airport_name}, City: {airport.city}, Coordinates: {airport.coordinates}, Timezone: {airport.timezone}")
        return airport
    else:
        print(f"Airport with code {airport_code} not found.")
        return None
    
def get_aircraft_codes_with_limit(limit):
    aircraft_codes = session.query(AircraftsData.aircraft_code).limit(limit).all()
    print(f"Aircraft Codes:")
    for code in aircraft_codes:
        print(code[0])
    return aircraft_codes

def get_airport_codes_with_limit(limit):
    airport_codes = session.query(AirportsData.airport_code).limit(limit).all()
    print(f"Airport Codes:")
    for code in airport_codes:
        print(code[0])
    return airport_codes

# Добавленные функции
def get_full_flight_info(flight_id):
    flight = session.query(Flights).filter_by(flight_id=flight_id).first()
    if flight:
        print(f"Flight ID: {flight.flight_id}")
        print(f"Flight No: {flight.flight_no}")
        print(f"Scheduled Departure: {flight.scheduled_departure}")
        print(f"Scheduled Arrival: {flight.scheduled_arrival}")
        print(f"Departure Airport: {flight.departure_airport}")
        print(f"Arrival Airport: {flight.arrival_airport}")
        print(f"Status: {flight.status}")
        print(f"Aircraft Code: {flight.aircraft_code}")
        print(f"Actual Departure: {flight.actual_departure}")
        print(f"Actual Arrival: {flight.actual_arrival}")
        return flight
    else:
        print(f"Flight with ID {flight_id} not found.")
        return None

def get_full_aircraft_info(aircraft_code):
    aircraft = session.query(AircraftsData).filter_by(aircraft_code=aircraft_code).first()
    if aircraft:
        print(f"Aircraft Code: {aircraft.aircraft_code}")
        print(f"Model: {aircraft.model}")
        print(f"Range: {aircraft.range}")
        return aircraft
    else:
        print(f"Aircraft with code {aircraft_code} not found.")
        return None

def get_full_airport_info(airport_code):
    airport = session.query(AirportsData).filter_by(airport_code=airport_code).first()
    if airport:
        print(f"Airport Code: {airport.airport_code}")
        print(f"Airport Name: {airport.airport_name}")
        print(f"City: {airport.city}")
        print(f"Coordinates: {airport.coordinates}")
        print(f"Timezone: {airport.timezone}")
        return airport
    else:
        print(f"Airport with code {airport_code} not found.")
        return None

def calculate_revenue_and_tickets_by_flight(flight_id):
    revenue = session.query(func.sum(TicketFlights.amount)).filter_by(flight_id=flight_id).scalar()
    business_tickets = session.query(func.count(TicketFlights.ticket_no)).filter_by(flight_id=flight_id, fare_conditions='Business').scalar()
    comfort_tickets = session.query(func.count(TicketFlights.ticket_no)).filter_by(flight_id=flight_id, fare_conditions='Comfort').scalar()
    economy_tickets = session.query(func.count(TicketFlights.ticket_no)).filter_by(flight_id=flight_id, fare_conditions='Economy').scalar()

    print(f"Revenue for Flight ID {flight_id}: {revenue} Rub")
    print(f"Business Tickets: {business_tickets}")
    print(f"Comfort Tickets: {comfort_tickets}")
    print(f"Economy Tickets: {economy_tickets}")
    return {
        "revenue": revenue,
        "business_tickets": business_tickets,
        "comfort_tickets": comfort_tickets,
        "economy_tickets": economy_tickets
    }

def get_flight_ids_with_limit(limit):
    flight_ids = session.query(Flights.flight_id).limit(limit).all()
    print(f"Flight IDs:")
    for flight_id in flight_ids:
        print(flight_id[0])
    return flight_ids

# UPDATE (Обновление)
def update_flight_status(flight_id, new_status):
    flight = session.query(Flights).filter_by(flight_id=flight_id).first()
    if flight:
        flight.status = new_status
        session.commit()
        print(f"Flight ID {flight_id} status updated to '{new_status}'")
        return flight
    else:
        print(f"Flight with ID {flight_id} not found.")
        return None

def update_booking_total_amount(book_ref, new_total_amount):
    booking = session.query(Bookings).filter_by(book_ref=book_ref).first()
    if booking:
        booking.total_amount = new_total_amount
        session.commit()
        print(f"Booking Ref {book_ref} total amount updated to {new_total_amount}")
        return booking
    else:
        print(f"Booking with Ref {book_ref} not found.")
        return None

# DELETE (Удаление)
def delete_flight(flight_id):
    flight = session.query(Flights).filter_by(flight_id=flight_id).first()
    if flight:
        session.delete(flight)
        session.commit()
        print(f"Flight ID {flight_id} deleted.")
    else:
        print(f"Flight with ID {flight_id} not found.")

def delete_aircraft(aircraft_code):
    aircraft = session.query(AircraftsData).filter_by(aircraft_code=aircraft_code).first()
    if aircraft:
        session.delete(aircraft)
        session.commit()
        print(f"Aircraft with code {aircraft_code} deleted.")
    else:
        print(f"Aircraft with code {aircraft_code} not found.")

def delete_booking(book_ref):
    booking = session.query(Bookings).filter_by(book_ref=book_ref).first()
    if booking:
        session.delete(booking)
        session.commit()
        print(f"Booking Ref {book_ref} deleted.")
    else:
        print(f"Booking with Ref {book_ref} not found.")

def delete_ticket(ticket_no):
    ticket = session.query(Tickets).filter_by(ticket_no=ticket_no).first()
    if ticket:
        session.delete(ticket)
        session.commit()
        print(f"Ticket No {ticket_no} deleted.")
    else:
        print(f"Ticket with No {ticket_no} not found.")

# Примеры использования
if __name__ == "__main__":
    # Создание
    flight_id = add_flight("FL123", "2023-10-01 10:00:00", "2023-10-01 12:00:00", "JFK", "LAX", "Scheduled", "B737", "2023-10-01 10:05:00", "2023-10-01 12:05:00")
    aircraft_code = add_aircraft("B737", "Boeing 737", 5000)
    book_ref = add_booking("BK123", "2023-09-25 12:00:00", 500)
    ticket_no = add_ticket(12345, book_ref, "P12345")

    # Чтение
    get_flight_by_id(1185)
    get_tickets_by_booking("000012")
    get_aircraft_inf(773)
    get_airport_inf("YKS")

    # Добавленные функции
    get_full_flight_info(1185)
    get_full_aircraft_info(773)
    get_full_airport_info("DME")
    calculate_revenue_and_tickets_by_flight(30625)
    get_flight_ids_with_limit(5)
    get_aircraft_codes_with_limit(5)
    get_airport_codes_with_limit(5)

    # Обновление
    update_flight_status(flight_id, "Delayed")
    update_booking_total_amount(book_ref, 550)

    # Удаление
    delete_flight(flight_id)
    delete_aircraft(aircraft_code)
    delete_booking(book_ref)
    delete_ticket(ticket_no)


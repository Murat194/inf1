from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Базовый класс для всех моделей
Base = declarative_base()

# Таблица flights
class Flights(Base):
    __tablename__ = 'flights'
    flight_id = Column(Integer, primary_key=True)
    flight_no = Column(String)
    scheduled_departure = Column(String)  
    scheduled_arrival = Column(String)    
    departure_airport = Column(String)
    arrival_airport = Column(String)
    status = Column(String)
    aircraft_code = Column(String, ForeignKey('aircrafts_data.aircraft_code'))
    actual_departure = Column(String)  
    actual_arrival = Column(String)    

    # Связь с таблицей aircrafts_data
    aircraft = relationship('AircraftsData', back_populates='flights')
    # Связь с таблицей ticket_flights
    ticket_flights = relationship('TicketFlights', back_populates='flight')

# Таблица aircrafts_data
class AircraftsData(Base):
    __tablename__ = 'aircrafts_data'
    aircraft_code = Column(String, primary_key=True)
    model = Column(String)
    range = Column(Integer)

    # Связь с таблицей flights
    flights = relationship('Flights', back_populates='aircraft')
    # Связь с таблицей seats
    seats = relationship('Seats', back_populates='aircraft')

# Таблица airports_data
class AirportsData(Base):
    __tablename__ = 'airports_data'
    airport_code = Column(String, primary_key=True)
    airport_name = Column(String)
    city = Column(String)
    coordinates = Column(String)
    timezone = Column(String)

# Таблица boarding_passes
class BoardingPasses(Base):
    __tablename__ = 'boarding_passes'
    ticket_no = Column(String, ForeignKey('ticket_flights.ticket_no'), primary_key=True)
    boarding_no = Column(Integer)
    seat_no = Column(String)

    # Связь с таблицей ticket_flights
    ticket_flight = relationship('TicketFlights', back_populates='boarding_passes')

# Таблица bookings
class Bookings(Base):
    __tablename__ = 'bookings'
    book_ref = Column(String, primary_key=True)
    book_date = Column(String)  
    total_amount = Column(Integer)

    # Связь с таблицей tickets
    tickets = relationship('Tickets', back_populates='booking')

# Таблица seats
class Seats(Base):
    __tablename__ = 'seats'
    aircraft_code = Column(String, ForeignKey('aircrafts_data.aircraft_code'), primary_key=True)
    seat_no = Column(String, primary_key=True)
    fare_conditions = Column(String)

    # Связь с таблицей aircrafts_data
    aircraft = relationship('AircraftsData', back_populates='seats')

# Таблица ticket_flights
class TicketFlights(Base):
    __tablename__ = 'ticket_flights'
    ticket_no = Column(String, ForeignKey('tickets.ticket_no'), primary_key=True)
    flight_id = Column(Integer, ForeignKey('flights.flight_id'), primary_key=True)
    fare_conditions = Column(String)
    amount = Column(Integer)

    # Связь с таблицей flights
    flight = relationship('Flights', back_populates='ticket_flights')
    # Связь с таблицей tickets
    ticket = relationship('Tickets', back_populates='ticket_flights')
    # Связь с таблицей boarding_passes
    boarding_passes = relationship('BoardingPasses', back_populates='ticket_flight')

# Таблица tickets
class Tickets(Base):
    __tablename__ = 'tickets'
    ticket_no = Column(Integer, primary_key=True)
    book_ref = Column(String, ForeignKey('bookings.book_ref'))
    passenger_id = Column(String)

    # Связь с таблицей bookings
    booking = relationship('Bookings', back_populates='tickets')
    # Связь с таблицей ticket_flights
    ticket_flights = relationship('TicketFlights', back_populates='ticket')

# Настройка подключения к базе данных
def setup_database(database_path="sqlite:///teavel.sqlite"):
    engine = create_engine(database_path)
    Base.metadata.create_all(engine)
    return engine

# Создание сессии
def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
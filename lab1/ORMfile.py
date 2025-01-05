from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Базовый класс для всех моделей
Base = declarative_base()

# Таблица Directors
class Directors(Base):
    __tablename__ = 'Directors'
    name = Column(String)
    id = Column(Integer, primary_key=True)
    gender = Column(Integer)
    uid = Column(Integer)
    department = Column(String)

    movies = relationship('Movies', back_populates='director')

# Таблица Movies
class Movies(Base):
    __tablename__ = 'Movies'
    id = Column(Integer, primary_key=True)
    original_title = Column(String)
    budget = Column(Integer)
    popularity = Column(Integer)
    release_date = Column(String)
    revenue = Column(Integer)
    title = Column(String)
    vote_average = Column(Float)
    vote_count = Column(Integer)
    overview = Column(String)
    director_id = Column(Integer, ForeignKey('Directors.id'))


    director = relationship('Directors', back_populates='movies')


# Настройка подключения к базе данных
def setup_database(database_path="sqlite:///movies.sqlite"):
    engine = create_engine(database_path)
    Base.metadata.create_all(engine)
    return engine

# Создание сессии
def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


engine = setup_database("sqlite:///movies.sqlite")
session = create_session(engine)
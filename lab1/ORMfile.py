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


# novi rezhisser
new_director = Directors(name="Vlad Posnov", gender=2, uid=2006, department="Directing")
session.add(new_director)
session.commit()
print("added director with id:", new_director.id)

# novi film
new_movie = Movies(original_title="new film", budget=1000000, popularity=10, release_date="2024-12-31", revenue=2000000, title="new film", vote_average=9.9, vote_count=1000, overview="otlichni film!!", director_id=new_director.id)
session.add(new_movie)
session.commit()
print("added movie with id: ", new_movie.id)

# vce filmi rezhissera
director = session.query(Directors).filter_by(name="Vlad Posnov").first()
if director:
    mt = [movie.title for movie in director.movies]
    print("movies by", director.name, ":", mt)

# delete film
movie = session.query(Movies).filter_by(title="new movie").first()
if movie:
    session.delete(movie)
    session.commit()
    print("movie deleted.")

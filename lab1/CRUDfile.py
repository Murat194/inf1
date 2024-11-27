from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ORMfile import setup_database, create_session, Directors, Movies  # Подключаем модели из ORM

# Инициализация базы данных
engine = setup_database("sqlite:///movies.sqlite")
session = create_session(engine)

# CREATE (Создание)
def add_director(name, gender, uid, department):
    new_director = Directors(name=name, gender=gender, uid=uid, department=department)
    session.add(new_director)
    session.commit()
    print("director '", name, "' added with id: ", str(new_director.id))
    return new_director.id

def add_movie(original_title, budget, popularity, release_date, revenue, title, vote_average, vote_count, overview, director_id):
    new_movie = Movies(
        original_title=original_title,
        budget=budget,
        popularity=popularity,
        release_date=release_date,
        revenue=revenue,
        title=title,
        vote_average=vote_average,
        vote_count=vote_count,
        overview=overview,
        director_id=director_id
    )
    session.add(new_movie)
    session.commit()
    print("movie '", title, "' added with id: ", str(new_movie.id))
    return new_movie.id

# READ (Чтение)
def get_director_by_id(director_id):
    director = session.query(Directors).filter_by(id=director_id).first()
    if director:
        print("director: ", director.name, ", gender: ", str(director.gender), ", uid: ", str(director.uid), ", department: ", director.department)
        return director
    else:
        print("director with id ", str(director_id), " not found.")
        return None

def get_all_directors():
    directors = session.query(Directors).all()
    for director in directors:
        print("director id: ", str(director.id), ", name: ", director.name)
    return directors

def get_movies_by_director(director_id):
    movies = session.query(Movies).filter_by(director_id=director_id).all()
    print("movies by director id ", str(director_id), ":")
    for movie in movies:
        print("- ", movie.title)
    return movies

# UPDATE (Обновление)
def update_director_name(director_id, new_name):
    director = session.query(Directors).filter_by(id=director_id).first()
    if director:
        director.name = new_name
        session.commit()
        print("director id ", str(director_id), " updated to '", new_name, "'")
        return director
    else:
        print("director with id ", str(director_id), " not found.")
        return None

def update_movie_title(movie_id, new_title):
    movie = session.query(Movies).filter_by(id=movie_id).first()
    if movie:
        movie.title = new_title
        session.commit()
        print("movie id ", str(movie_id), " updated to '", new_title, "'")
        return movie
    else:
        print("movie with id ", str(movie_id), " not found.")
        return None

# DELETE (Удаление)
def delete_director(director_id):
    director = session.query(Directors).filter_by(id=director_id).first()
    if director:
        director_name = director.name
        session.delete(director)
        session.commit()
        print("director id ", str(director_id), " (", director_name, ") deleted.")
    else:
        print("director with id ", str(director_id), " not found.")

def delete_movie(movie_id):
    movie = session.query(Movies).filter_by(id=movie_id).first()
    if movie:
        movie_title = movie.title
        session.delete(movie)
        session.commit()
        print("movie id ", str(movie_id), " (", movie_title, ") deleted.")
    else:
        print("movie with id ", str(movie_id), " not found.")

# Примеры использования
if __name__ == "__main__":
    # Создание
    director_id = add_director("Vlad Posnov", 2, 2006, "Directing")
    movie_id = add_movie("new movie", 1000000, 10, "2024-12-31", 2000000, "new movie", 9.9, 1000, "well well well", director_id)

    # Чтение
    get_director_by_id(director_id)
    get_all_directors()
    get_movies_by_director(director_id)

    # Обновление
    update_director_name(director_id, "updated director")
    update_movie_title(movie_id, "updated movie")

    # Удаление
    delete_movie(movie_id)
    delete_director(director_id)
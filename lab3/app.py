from flask import Flask, render_template, request, redirect, url_for, flash
from ORMfile import setup_database, create_session, Directors, Movies
from CRUDfile import (
    add_director, add_movie, get_all_directors, get_all_movies,
    update_director_name, update_movie_title, delete_director, delete_movie
)

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Инициализация базы данных
engine = setup_database("sqlite:///movies.sqlite")
session = create_session(engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/directors')
def show_directors():
    directors = get_all_directors()
    return render_template('directors.html', directors=directors)

@app.route('/movies')
def show_movies():
    movies = get_all_movies()
    return render_template('movies.html', movies=movies)

@app.route('/add_director', methods=['GET', 'POST'])
def add_director_route():
    if request.method == 'POST':
        name = request.form['name']
        gender = int(request.form['gender'])
        uid = int(request.form['uid'])
        department = request.form['department']

        director_id = add_director(name, gender, uid, department)
        flash(f"Director added with ID: {director_id}")
        return redirect(url_for('show_directors'))
    return render_template('add_director.html')

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie_route():
    if request.method == 'POST':
        original_title = request.form['original_title']
        budget = int(request.form['budget'])
        popularity = float(request.form['popularity'])
        release_date = request.form['release_date']
        revenue = int(request.form['revenue'])
        title = request.form['title']
        vote_average = float(request.form['vote_average'])
        vote_count = int(request.form['vote_count'])
        overview = request.form['overview']
        director_id = int(request.form['director_id'])

        movie_id = add_movie(original_title, budget, popularity, release_date, revenue, title, vote_average, vote_count, overview, director_id)
        flash(f"Movie added with ID: {movie_id}")
        return redirect(url_for('show_movies'))
    return render_template('add_movie.html')

@app.route('/update_director/<int:director_id>', methods=['GET', 'POST'])
def update_director_route(director_id):
    if request.method == 'POST':
        new_name = request.form['new_name']
        director = update_director_name(director_id, new_name)
        if director:
            flash(f"Director ID {director_id} updated to '{new_name}'")
        else:
            flash(f"Director with ID {director_id} not found.")
        return redirect(url_for('show_directors'))
    return render_template('update_director.html', director_id=director_id)

@app.route('/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie_route(movie_id):
    if request.method == 'POST':
        new_title = request.form['new_title']
        movie = update_movie_title(movie_id, new_title)
        if movie:
            flash(f"Movie ID {movie_id} updated to '{new_title}'")
        else:
            flash(f"Movie with ID {movie_id} not found.")
        return redirect(url_for('show_movies'))
    return render_template('update_movie.html', movie_id=movie_id)

@app.route('/delete_director/<string:director_name>', methods=['POST'])
def delete_director_route(director_name):
    delete_director(director_name)
    flash(f"Director '{director_name}' deleted.")
    return redirect(url_for('show_directors'))

@app.route('/delete_movie/<string:movie_title>', methods=['POST'])
def delete_movie_route(movie_title):
    delete_movie(movie_title)
    flash(f"Movie '{movie_title}' deleted.")
    return redirect(url_for('show_movies'))

@app.route('/director/<int:director_id>/movies')
def show_director_movies(director_id):
    director = session.query(Directors).filter_by(id=director_id).first()
    if director:
        movies = session.query(Movies).filter_by(director_id=director_id).all()
        return render_template('director_movies.html', director=director, movies=movies)
    else:
        flash(f"Director with ID {director_id} not found.")
        return redirect(url_for('show_directors'))

if __name__ == '__main__':
    app.run(debug=True)
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQtfile import Ui_MainWindow 
from ORMfile import setup_database, create_session, Directors, Movies  
from CRUDfile import (
    add_director, add_movie, get_all_directors, get_all_movies,
    update_director_name, update_movie_title, delete_director, delete_movie
)

# Инициализация базы данных
engine = setup_database("sqlite:///movies.sqlite")
session = create_session(engine)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Подключение кнопок к функциям
        self.ui.pushButton_add_director.clicked.connect(self.add_director)
        self.ui.pushButton_add_movie.clicked.connect(self.add_movie)
        self.ui.pushButton_get_all_directors.clicked.connect(self.show_all_directors)
        self.ui.pushButton_get_all_movies.clicked.connect(self.show_all_movies)
        self.ui.pushButton_update_director_name.clicked.connect(self.update_director_name)
        self.ui.pushButton_update_movie_title.clicked.connect(self.update_movie_title)
        self.ui.pushButton_delete_director.clicked.connect(self.delete_director)
        self.ui.pushButton_delete_movie.clicked.connect(self.delete_movie)

    def add_director(self):
        try:
            name = self.ui.lineEdit_directorName.text()
            gender = int(self.ui.lineEdit_directorGender.text())
            uid = int(self.ui.lineEdit_directorUid.text())
            department = self.ui.lineEdit_Department.text()

            director_id = add_director(name, gender, uid, department)
            QMessageBox.information(self, "Success", f"Director added with ID: {director_id}")
            self.show_all_directors()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def add_movie(self):
        try:
            original_title = self.ui.lineEdit_oridignal_title.text()
            budget = int(self.ui.lineEdit_movie_budget.text())
            popularity = float(self.ui.lineEdit_popularity.text())
            release_date = self.ui.lineEdit_release_date.text()
            revenue = int(self.ui.lineEdit_revenue.text())
            title = self.ui.lineEdit_title.text()
            vote_average = float(self.ui.lineEdit_vote_average.text())
            vote_count = int(self.ui.lineEdit_vote_count.text())
            overview = self.ui.lineEdit_overview.text()
            director_id = int(self.ui.lineEdit_director_id.text())

            movie_id = add_movie(original_title, budget, popularity, release_date, revenue, title, vote_average, vote_count, overview, director_id)
            QMessageBox.information(self, "Success", f"Movie added with ID: {movie_id}")
            self.show_all_movies()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_all_directors(self):
        directors = get_all_directors()
        self.ui.listWidget.clear()
        for director in directors:
            self.ui.listWidget.addItem(f"Director ID: {director.id}, Name: {director.name}")

    def show_all_movies(self):
        movies = get_all_movies()
        self.ui.listWidget.clear()
        for movie in movies:
            self.ui.listWidget.addItem(f"ID: {movie.id} Title: {movie.title}, Director ID: {movie.director_id}, AVG vote: {movie.vote_average}")

    def update_director_name(self):
        try:
            director_id = int(self.ui.lineEdit_director_id_for_update.text())
            new_name = self.ui.lineEdit_new_name_for_update.text()

            director = update_director_name(director_id, new_name)
            if director:
                QMessageBox.information(self, "Success", f"Director ID {director_id} updated to '{new_name}'")
                self.show_all_directors()
            else:
                QMessageBox.information(self, "Not Found", f"Director with ID {director_id} not found.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_movie_title(self):
        try:
            movie_id = int(self.ui.lineEdit_movie_id_forupdate.text())
            new_title = self.ui.lineEdit_new_title.text()

            movie = update_movie_title(movie_id, new_title)
            if movie:
                QMessageBox.information(self, "Success", f"Movie ID {movie_id} updated to '{new_title}'")
                self.show_all_movies()
            else:
                QMessageBox.information(self, "Not Found", f"Movie with ID {movie_id} not found.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete_director(self):
        try:
            director_name = self.ui.lineEdit_director_name.text()
            delete_director(director_name)
            QMessageBox.information(self, "Success", f"Director '{director_name}' deleted.")
            self.show_all_directors()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete_movie(self):
        try:
            movie_title = self.ui.lineEdit_movie_title.text()
            delete_movie(movie_title)
            QMessageBox.information(self, "Success", f"Movie '{movie_title}' deleted.")
            self.show_all_movies()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
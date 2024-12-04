import sqlite3

# Создание класса для представления альбома
class Album:
    def __init__(self, album_id, title, artist_id):
        self.album_id = album_id
        self.title = title
        self.artist_id = artist_id

    def __repr__(self):
        return f"Album(id={self.album_id}, title='{self.title}', artist_id={self.artist_id})"

# Создание класса для представления исполнителя
class Artist:
    def __init__(self, artist_id, name):
        self.artist_id = artist_id
        self.name = name

    def __repr__(self):
        return f"Artist(id={self.artist_id}, name='{self.name}')"

# Функция для подключения к базе данных
def get_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        print("Подключение к базе данных успешно.")
        return connection
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return None

# Функция для получения всех альбомов
def get_all_albums(connection):
    cursor = connection.cursor()
    cursor.execute('''
    SELECT Album.Albumid,Album.Title,Artist.ArtistId
    FROM Album     
    JOIN Artist ON Album.ArtistId = Artist.ArtistId;
    ''')
    a = cursor.fetchall()
    return [Album(album_id, title, artist_id) for album_id, title, artist_id in a]

# Функция для получения исполнителей
def get_all_artists(connection):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT *
        FROM Artist     
        ''')
    a = cursor.fetchall()
    return [Artist(artist_id,name) for artist_id, name in a]

# Функция для получения треков, выпущенных после 2010 года
def get_tracks_after_2010(connection):
    cursor = connection.cursor()
    cursor.execute('''
            SELECT Track.Name
            FROM Track     
            ''')
    a = cursor.fetchall()
    return a
if __name__ == "__main__":
    db_file = 'Chinook_Sqlite.sqlite'  # Укажи путь к базе данных
    connection = get_connection(db_file)
    if connection:
        # Получение всех альбомов
        albums = get_all_albums(connection)
        print("Альбомы:")
        for album in albums:
            print(album)
        # Получение всех исполнителей
        artists = get_all_artists(connection)
        print("\nИсполнители:")
        for artist in artists:
            print(artist)

        # Получение треков, выпущенных после 2010 года
        tracks_after_2010 = get_tracks_after_2010(connection)
        print("\nТреки, выпущенные после 2010 года:")
        for track in tracks_after_2010:
            print(track)
        # Закрытие соединения
        connection.close()
    else:
        print("Не удалось установить соединение с базой данных.")
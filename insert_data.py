import csv
import mysql.connector

class MovieDataInserter:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            port=3000,
            user="root",
            password="system",
            database="movie_recommend"
        )
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def insert_movies_data(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                try:
                   # Extract data from the CSV row
                    movie_id = int(row['id'])
                    title = row['title']
                    genres = row['genres']
                    keywords = row['keywords']
                    overview = row['overview']
                    vote_average = float(row['vote_average'])
                    vote_count = int(row['vote_count'])
                    year = int(row['year'])
                    language = row['language']

                    # Prepare and execute the SQL query to insert data (without IGNORE to detect errors)
                    query = "INSERT INTO recomm_movies (id, title, genres, keywords, overview, vote_average, vote_count, year, language) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    values = (movie_id, title, genres, keywords, overview, vote_average, vote_count, year, language)
                    self.cursor.execute(query, values)

                    # Commit changes
                    self.connection.commit()
                except mysql.connector.Error as err:
                    # Handle errors (skip duplicate, mismatch, or weakly referencing errors)
                    if err.errno == 1062:
                        print(f"Skipping duplicate entry: {row['id']}")
                    elif err.errno == 1452:
                        print(f"Skipping weakly referencing error: {row['id']}")
                    else:
                        print(f"Skipping row due to unexpected error: {err}")
                    self.connection.rollback()
        self.stdout.write(self.style.SUCCESS('Movies table inserted successfully.'))
                

    def insert_credits_data(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                try:
                    # Extract data from the CSV row
                    movie_id = int(row['movie_id'])
                    cast = row['cast']
                    director = row['director']

                    # Prepare and execute the SQL query to insert data (without IGNORE to detect errors)
                    query = "INSERT INTO recomm_credits (movie_id, cast, director) VALUES (%s, %s, %s)"
                    values = (movie_id, cast, director)
                    self.cursor.execute(query, values)

                    # Commit changes
                    self.connection.commit()
                except mysql.connector.Error as err:
                    # Handle errors (skip duplicate, mismatch, or weakly referencing errors)
                    if err.errno == 1062:
                        print(f"Skipping duplicate entry: {row['movie_id']}")
                    elif err.errno == 1452:
                        print(f"Skipping weakly referencing error: {row['movie_id']}")
                    else:
                        print(f"Skipping row due to unexpected error: {err}")
                    self.connection.rollback()
        self.stdout.write(self.style.SUCCESS('Movies table inserted successfully.'))

    def cleanup(self):
        self.close_connection()

# Specify the file paths
movies_data_file = r'C:\Users\Medha Trust\Desktop\django-pro\movie_recomendations\preprocessing\tmdb_data\processed_movies_data.csv'
credits_data_file = r'C:\Users\Medha Trust\Desktop\django-pro\movie_recomendations\preprocessing\tmdb_data\processed_credits_data.csv'

# Create an instance of MovieDataInserter
data_inserter = MovieDataInserter()

# Insert movies data into the database
data_inserter.insert_movies_data(movies_data_file)

# Insert credits data into the database
data_inserter.insert_credits_data(credits_data_file)

# Clean up resources
data_inserter.cleanup()

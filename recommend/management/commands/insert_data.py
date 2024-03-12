import csv
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from recommend.models import Movies
import requests
import logging


class Command(BaseCommand):
    help = 'Insert data into Django database from CSV files'

    def handle(self, *args, **options):
        movies_data_file = r'preprocessing\tmdb_data\movies_data.csv'

        self.insert_movies_data(movies_data_file)

    def insert_movies_data(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            count = 0

            for row in csvreader:
                try:
                    # Extract data from the CSV row
                    movie_id = int(row['movie_id'])
                    title = row['title']
                    poster_path = self.fetch_poster(movie_id)
                    genres = row['genres']
                    keywords = row['keywords']
                    overview = row['overview']
                    vote_average = float(row['vote_average'])
                    vote_count = int(row['vote_count'])
                    year = int(row['year'])
                    language = row['language']
                    cast = row['cast']
                    director = row['director']
                    


                    # Use Django ORM to insert data into the Movies table
                    movie_instance = Movies.objects.create(
                        id=movie_id,
                        title=title,
                        poster_path = poster_path,
                        genres=genres,
                        keywords=keywords,
                        overview=overview,
                        vote_average=vote_average,
                        vote_count=vote_count,
                        year=year,
                        language=language,
                        cast = cast,
                        director = director
                    )
                    movie_instance.save()
                    self.stdout.write(self.style.SUCCESS(f"{count +1}) Inserted Movie: {movie_id}"))
                except IntegrityError:
                    self.stdout.write(self.style.WARNING(f"Movie with ID {movie_id} already exists. Skipping."))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error inserting movie: {e}"))

    def fetch_poster(self,movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=c5593d7e3a6a6f8e2278388ae57498b7&language=en-US".format(movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        try:
            if poster_path:
                full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
                return full_path
            else:
                return None  # No poster path available for the movie
        except requests.RequestException as e:
            logging.error(f"Error fetching poster for movie {movie_id}: {e}")
            return None
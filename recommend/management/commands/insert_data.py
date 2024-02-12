import csv
import os
from django.core.management.base import BaseCommand
from recomm.models import Movies, Credits  # Import your Django models

class Command(BaseCommand):
    help = 'Insert data into Django database from CSV files'

    def handle(self, *args, **options):
        # # Specify the file paths relative to your Django app
        # base_path = os.path.dirname(os.path.abspath(__file__))
        # movies_data_file = os.path.join(base_path, 'path', 'to', 'your', 'processed_movies_data.csv')
        # credits_data_file = os.path.join(base_path, 'path', 'to', 'your', 'processed_credits_data.csv')

        movies_data_file = r'C:\Users\Medha Trust\Desktop\django-pro\movie_recomendations\preprocessing\tmdb_data\processed_movies_data.csv'
        credits_data_file = r'C:\Users\Medha Trust\Desktop\django-pro\movie_recomendations\preprocessing\tmdb_data\processed_credits_data.csv'


        self.insert_movies_data(movies_data_file)
        self.insert_credits_data(credits_data_file)

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
                    # watched = int(value())

                    # Use Django ORM to insert data into the Movies table
                    movie_instance = Movies.objects.create(
                        id=movie_id,
                        title=title,
                        genres=genres,
                        keywords=keywords,
                        overview=overview,
                        vote_average=vote_average,
                        vote_count=vote_count,
                        year=year,
                        language=language
                    )
                    movie_instance.save()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Skipping row due to unexpected error: {e}"))

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

                    # Use Django ORM to insert data into the Credits table
                    credit_instance = Credits.objects.create(
                        movie_id=movie_id,
                        cast=cast,
                        director=director
                    )
                    credit_instance.save()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Skipping row due to unexpected error: {e}"))
        self.stdout.write(self.style.SUCCESS('Credits table inserted successfully.'))
        

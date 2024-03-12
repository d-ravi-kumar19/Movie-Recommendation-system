# recommend/management/commands/populate_metadata.py

from django.core.management.base import BaseCommand
from recommend.models import Metadata, Movies, Credits
from ast import literal_eval

class Command(BaseCommand):
    help = 'Populate metadata table with combined information'
    print("Populating metadata...")
    def handle(self, *args, **options):
        # Clear existing data in the metadata table
        Metadata.objects.all().delete()

        # Fetch data from recomm_movies and recomm_credits
        movies_data = Movies.objects.values('movie_id','title', 'overview', 'genres', 'keywords','cast', 'director').all()
        # credits_data = Credits.objects.values('movie_id', 'cast', 'director').all()

        # Create a dictionary to store combined information
        metadata_dict = {}

        # Populate the dictionary with combined information
        for movie in movies_data:
            movie_id = movie['movie_id']
            
            genres_list = literal_eval(movie['genres'])
            keywords_list = literal_eval(movie['keywords'])
            cast_list = literal_eval(movie['cast'])

            metadata_dict[movie_id] = {
                'genres': genres_list,
                'keywords': keywords_list,
                'overview': movie['overview'],
                'cast': cast_list,
                'director': movie['director']
            }

        # for credit in credits_data:
        #     movie_id = credit['movie_id']

        #     cast_list = literal_eval(credit['cast'])

        #     if movie_id in metadata_dict:
        #         metadata_dict[movie_id]['cast'] = cast_list
        #         metadata_dict[movie_id]['director'] = credit['director']

        # Populate the Metadata table
        for movie_id, metadata_info in metadata_dict.items():
            # Combine lists into space-separated strings
            genres_combined = ' '.join(metadata_info['genres'])
            keywords_combined = ' '.join(metadata_info['keywords'])
            cast_combined = ' '.join(metadata_info['cast'])

            description = f"{metadata_info['overview']} {genres_combined} {keywords_combined} {cast_combined} {metadata_info['director']}"
            Metadata.objects.create(movie_id=movie_id, description=description)

        self.stdout.write(self.style.SUCCESS('Metadata table populated successfully.'))

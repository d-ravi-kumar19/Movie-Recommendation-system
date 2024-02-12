import pickle
from django.core.management.base import BaseCommand
from recomm.models import Metadata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

class Command(BaseCommand):
    help = 'Dump DataFrame and similarity matrix into pickle files'

    def handle(self, *args, **options):
        # Get data from the database
        moviemeta_data = Metadata.objects.values('movie', 'description').all()

        # Create a DataFrame from the retrieved data
        df = pd.DataFrame.from_records(moviemeta_data)

        # Fill missing values with empty string
        # df = df.fillna('')

        # TF-IDF Vectorization
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(df['description'])

        # Calculate cosine similarity for content-based filtering
        content_similarity = linear_kernel(tfidf_matrix, tfidf_matrix)

        # Dump DataFrame and similarity matrix into pickle files
        with open('movie_dataframe.pkl', 'wb') as df_file:
            pickle.dump(df, df_file)

        with open('similarity_matrix.pkl', 'wb') as similarity_file:
            pickle.dump(content_similarity, similarity_file)

        self.stdout.write(self.style.SUCCESS('DataFrame and similarity matrix dumped successfully.'))
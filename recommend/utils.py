# utils.py
import logging
import pickle
import requests
from django.db.models import Avg, ExpressionWrapper, F, FloatField, Value
from .models import *

def fetch_poster(movie_id):
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

def fetch_posters(movies):
    movies_with_posters = []

    for movie in movies:
        poster_path = fetch_poster(movie.id)
        movies_with_posters.append({
            'movie': movie,
            'poster_path': poster_path,
        })

    return movies_with_posters


# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=c5593d7e3a6a6f8e2278388ae57498b7&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

# def get_all_movies():
#     try:
#         m = 1000
#         all_movies = Movies.objects.annotate(
#             C=Avg('vote_average'),
#             m=Value(m, output_field=FloatField())
#         ).exclude(vote_count=0, vote_average=0)

#         all_movies = all_movies.annotate(
#             weighted_rating=ExpressionWrapper(
#                 (F('vote_count') / (F('vote_count') + F('m'))) * F('vote_average') +
#                 (F('m') / (F('vote_count') + F('m'))) * F('C'),
#                 output_field=FloatField()
#             )
#         ).order_by('-weighted_rating')

#         return all_movies
#     except Exception as e:
#         logging.error(f"Error retrieving all movies: {e}")
#         return None

def get_top_10_movies():
    m = 1000
    top_movies = Movies.objects.annotate(
        C=Avg('vote_average'),
        m=Value(m, output_field=FloatField())
    ).exclude(vote_count=0, vote_average=0)

    top_movies = top_movies.annotate(
        weighted_rating=ExpressionWrapper(
            (F('vote_count') / (F('vote_count') + F('m'))) * F('vote_average') +
            (F('m') / (F('vote_count') + F('m'))) * F('C'),
            output_field=FloatField()
        )
    ).order_by('-weighted_rating')[:10]

    return top_movies


def get_movies_by_language(language):
    return _get_movies_by_filter('language', language)

def get_movies_by_genre(genre):
    return _get_movies_by_filter('genres__icontains', genre)

def get_movies_by_director(director):
    return _get_movies_by_filter('director__icontains', director)


# def get_movies_by_director(director):
#     m = 1000
#     movies = Movies.objects.filter(**{filter_field: filter_value}).order_by('-vote_average')

#     movies_with_ratings = movies.annotate(
#         C=Avg('vote_average'),
#         m=Value(m, output_field=FloatField())
#     ).exclude(vote_count=0, vote_average=0)

#     movies_with_ratings = movies_with_ratings.annotate(
#         weighted_rating=ExpressionWrapper(
#             (F('vote_count') / (F('vote_count') + F('m'))) * F('vote_average') +
#             (F('m') / (F('vote_count') + F('m'))) * F('C'),
#             output_field=FloatField()
#         )
#     ).order_by('-weighted_rating')[:10]

#     return movies_with_ratings

    # return _get_movies_by_filter('director', director)

def _get_movies_by_filter(filter_field, filter_value):
    m = 1000
    movies = Movies.objects.filter(**{filter_field: filter_value}).order_by('-vote_average')

    movies_with_ratings = movies.annotate(
        C=Avg('vote_average'),
        m=Value(m, output_field=FloatField())
    ).exclude(vote_count=0, vote_average=0)

    movies_with_ratings = movies_with_ratings.annotate(
        weighted_rating=ExpressionWrapper(
            (F('vote_count') / (F('vote_count') + F('m'))) * F('vote_average') +
            (F('m') / (F('vote_count') + F('m'))) * F('C'),
            output_field=FloatField()
        )
    ).order_by('-weighted_rating')[:10]

    return movies_with_ratings


def get_content_based_recommendations(movie_id, num_recommendations=10):
    with open('models/movie_dataframe.pkl', 'rb') as df_file:
        df = pickle.load(df_file)

    with open('models/similarity_matrix.pkl', 'rb') as similarity_file:
        similarity = pickle.load(similarity_file)

    movie_index = df[df['movie'] == movie_id].index

    if not movie_index.empty:
        movie_index = movie_index[0]
    else:
        logging.error(f"Movie ID {movie_id} not found in the DataFrame.")
        return None

    movie_similarity_scores = similarity[movie_index]
    if not any(movie_similarity_scores):
        logging.warning(f"No recommendations found for movie ID {movie_id}.")
        return None

    similar_movie_indices = movie_similarity_scores.argsort()[::-1][1:num_recommendations + 1]
    recommended_movie_ids = df.iloc[similar_movie_indices]['movie'].tolist()

    return recommended_movie_ids



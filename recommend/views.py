# recommend/views.py
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render,get_object_or_404
import requests
# from django.http import HttpResponse
from django.db.models import *
from .models import Movies, Credits,Metadata
import pickle
import logging

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Redirect to a success page.
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # You can change 'login' to the actual login URL
    else:
        form = UserRegistrationForm()

    return render(request, 'signup.html', {'form': form})

def logout(request):
    return render(request,'logout.html')

def mylist(request):
    return render(request,'mylist.html')


# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path


def fetch_poster(movie_id):
    url = "https://imdb146.p.rapidapi.com/v1/find/"

    querystring = {"id":"tt0087884"}

    headers = {
            "X-RapidAPI-Key": "713d419c2emsh6fc87fe03c25287p1b0b45jsn5a38fc312049",
            "X-RapidAPI-Host": "imdb146.p.rapidapi.com"
            }
    # api_key = "713d419c2emsh6fc87fe03c25287p1b0b45jsn5a38fc312049"
    # url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
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
    # Fetch movies based on language
    m =1000
    movies = Movies.objects.filter(language=language).order_by('-vote_average')

    # Apply recommendations to the fetched movies
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

def get_content_based_recommendations(movie_id, num_recommendations=5):
    with open('movie_dataframe.pkl', 'rb') as df_file:
        df = pickle.load(df_file)

    with open('similarity_matrix.pkl', 'rb') as similarity_file:
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

    similar_movie_indices = movie_similarity_scores.argsort()[::-1][1:num_recommendations+1]
    recommended_movie_ids = df.iloc[similar_movie_indices]['movie'].tolist()

    return recommended_movie_ids

######################## Routers #######################


def home(request):
    featured_movies = [
        {'title': 'Movie 1', 'image_path': '/media/movie1.jpg'},
        {'title': 'Movie 2', 'image_path': '/media/movie2.jpg'},
        {'title': 'Movie 3', 'image_path': '/media/batman_begins.jpeg'},
        {'title': 'Movie 4', 'image_path': '/media/dark_knight.jpeg'},
        {'title': 'Movie 5', 'image_path': '/media/inception.jpeg'},
        {'title': 'Movie 6', 'image_path': '/media/avengers.jpeg'},


        # Add more movies as needed
    ]
    context = {
        'featured_movies': featured_movies,
    }
    return render(request,'home.html',context)

def search(request):
    return render(request,'search.html')


def movies(request):

    top_10_movies = get_top_10_movies()
    english_movies = get_movies_by_language('English')
    hindi_movies = get_movies_by_language('Hindi')

    # top_movies_with_posters = fetch_posters(top_10_movies)
    # english_movies_with_posters = fetch_posters(english_movies)
    # hindi_movies_with_posters = fetch_posters(hindi_movies)

    # context = {
    #     'top_movies_with_posters': top_movies_with_posters,
    #     'english_movies_with_posters': english_movies_with_posters,
    #     'hindi_movies_with_posters': hindi_movies_with_posters,
    # }
    context ={
        'top_movies': top_10_movies,
        'top_englishmovies': english_movies,
        'top_hindimovies': hindi_movies
    } 

    return render(request, 'movies.html', context)

# def get_movies_by_director(director_name):

#     movies = Movies.objects.filter(directors__name=director_name).order_by('-vote_average')[:10]
#     return movies



# def movie_detail(request, movie_id=None):
#     movie = None
#     recommended_movies = None
#     recommended_movie_ids = None
#     no_recommendations = False

#     if movie_id is not None:
#         movie_id = int(movie_id)
#         movie = get_object_or_404(Movies, pk=movie_id)
#         recommended_movie_ids = get_content_based_recommendations(movie_id)

#     if recommended_movie_ids:
#         recommended_movies = Movies.objects.filter(id__in=recommended_movie_ids)
#     else:
#         no_recommendations = True
    
#     if no_recommendations:
#         return render(request, 'no_recommendations.html', {'movie': movie})
#     else:
#         context = {
#             'movie': movie,
#             'recommended_movies': recommended_movies,
#         }
#         return render(request, 'movie_details.html', context)

def movie_search(request):
    movie = None
    recommended_movies = None
    error_message = None

    if request.method == 'GET':
        movie_id = request.GET.get('movie_id')

        if movie_id:
            movie_id = int(movie_id)
            movie = get_object_or_404(Movies, pk=movie_id)
            recommended_movie_ids = get_content_based_recommendations(movie_id)

            if recommended_movie_ids:
                recommended_movies = Movies.objects.filter(id__in=recommended_movie_ids)
            else:
                error_message = "No recommendations found for the provided movie."

    context = {
        'movie': movie,
        'recommended_movies': recommended_movies,
        'error_message': error_message,
    }
    return render(request, 'movie_search.html', context)

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Add your registration logic here
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # Add your login logic here
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def dashboard(request):
    return render(request, 'dashboard.html')
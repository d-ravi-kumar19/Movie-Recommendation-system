# recommend/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('movies',movies,name='movies'),
    path('see-more-movies/', see_more_movies, name='see_more_movies'),
    path('see-more-movies/<str:category>/', see_more_movies, name='see_more_movies'),
    path('load-more-movies/', load_more_movies, name='load_more_movies'),
    path('search/', search_results, name='search_results'),
    path('moviesearch', movie_search, name='moviesearch'),
    path('moviesearch/', movie_search, name='moviesearch_no_id'),
    path('moviesearch/<int:movie_id>/', movie_search, name='moviesearch_with_id'),
    path('signup/', user_signup, name='signup'),
    path('signin/', user_signin, name='signin'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('update_status', update_status, name='update_status'),
]

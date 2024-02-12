# recomm/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup',signup,name='signup'),
    path('movies',movies,name='movies'),
    path('mylist',mylist,name='mylist'),
    path('search',search,name='search'),
    path('movie/', movie_detail, name='movie_detail'),
]

# recommend/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('movies',movies,name='movies'),
    # path('mylist',mylist,name='mylist'),
    # path('search',search,name='search'),
    path('moviedetails', movie_search, name='movie_detail'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
]

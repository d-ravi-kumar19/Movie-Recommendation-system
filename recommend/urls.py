# recommend/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('movies',movies,name='movies'),
    # path('mylist',mylist,name='mylist'),
    # path('search',search,name='search'),
    path('moviesearch', movie_search, name='moviesearch'),
    path('signup/', user_signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('dashboard/', dashboard, name='dashboard'),
]

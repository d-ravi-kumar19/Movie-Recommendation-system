# recommend/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('movies',movies,name='movies'),
    # path('mylist',mylist,name='mylist'),
    # path('search',search,name='search'),
    path('moviesearch', movie_search, name='moviesearch'),
    path('moviesearch/<int:movie_id>/', movie_search, name='moviesearch_with_id'),
    path('signup/', user_signup, name='signup'),
    path('signin/', user_signin, name='signin'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('update_status/', update_status, name='update_status'),
]

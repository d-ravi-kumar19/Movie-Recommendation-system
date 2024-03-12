# recommend/views.py
from django.shortcuts import render, redirect, get_object_or_404
from recommend.models import Movies,UserCredentials,UserTracking
from django.http import JsonResponse
from django.contrib.auth import logout

from .utils import *
from django.contrib import messages
# ================= user_signup ===================

def user_signup(request):
    if request.method=='POST':
        username=request.POST.get("username")
        email=request.POST.get("email")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        if password1 is not None and password2 is not None and password1 == password2: 
            data = UserCredentials.objects.create( username= username,email=email,password=password1)
            data.save()

            return redirect('signin')
    return render(request,"recommend/signup.html")

# ================= user_signin ===================

def user_signin(request):
    authenticated = False

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = UserCredentials.objects.filter(username=username, password=password).first()
        print(user)
        if user is not None:
            messages.success(request, 'Login successful!')
            request.session['userid'] = user.id
            request.session['username'] = user.username
            authenticated = True
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, "recommend/signin.html", {'authenticated': authenticated})


# ================= user_logout ===================

def user_logout(request):
    # Use Django's logout function to log out the user
    logout(request)
    return redirect('home')  # Redirect to the home page after logout


# ================= dashboard ===================

def dashboard(request):
    # Retrieve user tracking information
    if 'username' in request.session:
        user_tracking = UserTracking.objects.get(user=request.session['userid'])
        watched_movies = [movie for movie in user_tracking.watched_movies.all()]
        favorite_movies = [favorite for favorite in user_tracking.favorite_movies.all()]
        # print(watched_movies)
        # print(favorite_movies)
        

        context = {
            'user_tracking':  user_tracking,
            'watched_movies': watched_movies,
            'favorite_movies': favorite_movies,
        }
        return render(request, 'recommend/dashboard.html', context=context)
    else:
        return redirect('signin')
# ================= home ===================

def home(request):

    featured_movies = [
        {'title': 'Movie 1', 'image_path': '/media/movie1.jpg'},
        {'title': 'Movie 2', 'image_path': '/media/movie2.jpg'},
        {'title': 'Movie 3', 'image_path': '/media/batman_begins.jpeg'},
        {'title': 'Movie 4', 'image_path': '/media/dark_knight.jpeg'},
        {'title': 'Movie 5', 'image_path': '/media/inception.jpeg'},
        {'title': 'Movie 6', 'image_path': '/media/avengers.jpeg'},
    ]
    top_10_movies = get_top_10_movies()
    english_movies = get_movies_by_language('English')
    hindi_movies = get_movies_by_language('Hindi')

    context = {
        'featured_movies': featured_movies,
        'top_movies': top_10_movies,
        'top_englishmovies': english_movies,
        'top_hindimovies': hindi_movies,
        'authenticated': True,
    }

    return render(request,'home.html',context)
    

def search(request):
    return render(request,'search.html')

# ================= movies ===================
def movies(request):
    # movie_posters =[]
    top_10_movies = get_top_10_movies()
    english_movies = get_movies_by_language('English')
    hindi_movies = get_movies_by_language('Hindi')
    romance_movies = get_movies_by_genre('Romance')
    science_fiction = get_movies_by_genre('ScienceFiction')
    thiller_movies = get_movies_by_genre('Thriller')

    # nolan_movies = get_movies_by_director('ChristopherNolan')
    

    context = {
        'top_movies': top_10_movies,
        'top_englishmovies': english_movies,
        'top_hindimovies': hindi_movies,
        'top_romancemovies':romance_movies,
        'top_scifimovies': science_fiction,
        'top_thillermovies':thiller_movies,
        # 'nolan_movies': nolan_movies,
        'authenticated': True,
    }

    return render(request, 'movies.html', context)

# ================= see more movies ===================


def see_more_movies(request, category=None):
    valid_categories = ['english', 'hindi', 'action', 'romance', 'dir-nolan','scifi']
    
    if category not in valid_categories:
        # Handle invalid category (optional)
        return render(request, 'error.html', {'message': 'Invalid category'})
    
    # Filter movies based on the selected category
    if category == 'english':
        more_movies = Movies.objects.filter(language='English')
    elif category == 'hindi':
        more_movies = Movies.objects.filter(language='Hindi')
    elif category == 'action-movies':
        more_movies = Movies.objects.filter(genres__icontains='Action')
    elif category == 'romance':
        more_movies = Movies.objects.filter(genres__icontains='Romance')
    elif category == 'scifi':
        more_movies = Movies.objects.filter(genres__icontains='ScienceFiction')
    # elif category == 'dir-nolan':
        # more_movies = Movies.objects.filter(director='ChristopherNolan')
    
    context = {
        'more_movies': more_movies,
    }
    
    return render(request, 'see_more_movies.html', context)


# ================= load more movies ===================

def load_more_movies(request):
    page = request.GET.get('page', 1)
    per_page = 20
    start = (int(page) - 1) * per_page
    end = start + per_page

    # Retrieve the next set of movies
    more_movies = Movies.objects.all()[start:end]

    context = {
        'movies_html': render_to_string('movie_list.html', {'more_movies': more_movies}),
        'has_next': len(more_movies) == per_page,
    }

    return JsonResponse(context)
# # ================= update movie to database ===================
def update_status(request):
    if request.method == 'POST':
        if 'username' in request.session:
            user = UserCredentials.objects.get(username=request.session['username'])
            user_tracking = UserTracking.objects.get_or_create(user=user)[0]
            movie_id = request.POST.get('movie_id')
            movie = get_object_or_404(Movies, id=movie_id)
            print(movie_id)
            print(request.POST.getlist('statusCheckbox'))
            statuses = request.POST.getlist('statusCheckbox')
            if 'watched' in statuses:
                if movie not in user_tracking.watched_movies.all():
                    user_tracking.watched_movies.add(movie)
            else:
                if movie in user_tracking.watched_movies.all():
                    user_tracking.watched_movies.remove(movie)
            if 'favorite' in statuses:
                if movie not in user_tracking.favorite_movies.all():
                    user_tracking.favorite_movies.add(movie)
            else:
                if movie in user_tracking.favorite_movies.all():
                    user_tracking.favorite_movies.remove(movie)
            user_tracking.save()
            response_data = {'message': 'Status updated successfully'}
            return JsonResponse(response_data)
        else:
            response_data = {'message': 'You must be logged in to update the movie status.'}
            return JsonResponse(response_data, status=401)

# # ================= search_results ===================





def search_results(request):
    if request.method == 'GET':
        # Retrieve the search query from the submitted form
        search_query = request.GET.get('search', '')
        search_query = search_query.lower().replace(' ', '').strip()

        # Fetch movies that match the search query (case-insensitive)
        movies = Movies.objects.filter(title__icontains=search_query)

        # Redirect to the movie_search page with the first movie's ID if found
        if movies.exists():
            first_movie_id = movies.first().id
            return redirect('moviesearch_with_id', movie_id=first_movie_id)

        # Pass the search results to the template
        context = {
            'search_query': search_query,
            'movies': movies,
        }

        # Render the movie_search template with the search results
        return render(request, 'movie_search.html', context=context)

# # ================= movie_search ===================

def movie_search(request):
    if 'username' in request.session:
        username = request.session['username']
        try:
            user = UserCredentials.objects.get(username=username)
        except UserCredentials.DoesNotExist:
            print("User not found.")
            return redirect('signin')

        user = get_object_or_404(UserCredentials, username=username)

        user_tracking, created = UserTracking.objects.get_or_create(user=user)

        movie_id = request.GET.get('movie_id')
        movie = None
        recommended_movies = None
        error_message = None

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
            'authenticated': True,
            'user_tracking': user_tracking,
        }

        return render(request, 'movie_search.html', context)
    else:
        return redirect('signin')

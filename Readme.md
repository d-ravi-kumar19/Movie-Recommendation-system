# Django Movie Recommendation Project

Welcome to the Django Movie Recommendation project! This web application uses Django to recommend movies dynamically.
The backend is powered by Django's default SQLite3 database, and it offers a range of views, including top movies by various criteria.
Users can receive personalized recommendations, mark movies as watched, and build a watchlist.
The project showcases the power of Django for creating interactive and data-driven web applications.

## Features
- Dynamic movie recommendations
- Top movies by language, director, genre, etc.
- Personalized user interactions
- Watched movies tracking and watchlist functionality

## Setup and Running the Code

### Prerequisites
- Python installed
- pip (Python package installer) installed

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/django-movie-recommendation.git

2. **Install dependencies:**
    ```bash 
    pip install -r requirements.txt
3. **Databse setup:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py insert_data
    python manage.py populate_metadata
    python manage.py dump_data
4. **Run Server:**
    ```bash 
    python manage.py runserver






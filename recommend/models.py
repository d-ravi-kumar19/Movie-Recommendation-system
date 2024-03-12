from django.db import models
import uuid

class Movies(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    poster_path = models.URLField(blank=True, null=True)  # Add a field for poster URL

    genres = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    
    # Credits
    cast = models.TextField(blank=True, null=True)
    director = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.title}"

class Metadata(models.Model):
    movie = models.OneToOneField(Movies, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()

    def __str__(self):
        return f'Metadata for Movie ID {self.movie.id}'

class UserCredentials(models.Model):
    userid = models.CharField(max_length=10, default=None, editable=False, unique=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed password

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.userid:
            self.userid = f'user{UserCredentials.objects.count() + 1}'
        super().save(*args, **kwargs)

class UserTracking(models.Model):
    user = models.ForeignKey(UserCredentials, on_delete=models.CASCADE)
    watched_movies = models.ManyToManyField(Movies, related_name='watched_by_users', blank=True)
    favorite_movies = models.ManyToManyField(Movies, related_name='favorited_by_users', blank=True)

    def __str__(self):
        return f'Tracking info for {self.user.username}'

from django.db import models


class Credits(models.Model):
    movie = models.OneToOneField('Movies', on_delete=models.CASCADE, primary_key=True)
    cast = models.TextField(blank=True, null=True)
    director = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.movie.id} - {self.cast}"

class Movies(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    genres = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    watched = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.title}"

class Metadata(models.Model):
    movie  = models.OneToOneField('Movies', on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()

    def __str__(self):
        return f'Metadata for Movie ID {self.movie.id}'

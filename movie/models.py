from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    year = models.IntegerField()
    image = models.ImageField(upload_to='movie/images/', blank=True, null=True)
    url = models.URLField(blank=True)
    genre = models.CharField(max_length=250, blank=True)
    year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

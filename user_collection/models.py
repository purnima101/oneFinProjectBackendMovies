from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import uuid

class Movie(models.Model):
    uuid = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.CharField(max_length=255)

class Collection(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

class CollectionMap(models.Model):
    collection_key = models.ForeignKey(Collection, on_delete=models.CASCADE)
    movie_key = models.ForeignKey(Movie, on_delete=models.CASCADE)
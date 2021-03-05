from django.db import models
from django.contrib.postgres.fields import JSONField
# django.db.models.JSONField
from django.utils import timezone

# Create your models here.
class Picture(models.Model):
    name = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    genre = models.TextField(blank=True,null=True)
    imdb_score = models.CharField( max_length=6, blank=True, null=True)
    dire99popularity = models.CharField(max_length=6, blank=True, null=True)
    pub_date =  models.DateTimeField(default=timezone.now)

# class User(models.User):

    
 

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Leaderboard(models.Model):

    gameName = models.CharField(max_length=100) # PK
    
    date_added = models.DateTimeField(auto_now_add=True) # when this leaderboard was added

    def __str__(self):
        return self.gameName

class Entry(models.Model):

    # id is PK

    LB = models.ForeignKey(Leaderboard, on_delete=models.CASCADE) # FK - gameName
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #username = models.CharField(max_length=20) #the same as owner
    score = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True) # when an entry to the leaderboard was added

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        return self.username


class Game(models.Model):
    title = models.CharField(max_length=100) #game name??
    # file = models.FileField(upload_to='media', max_length=1000)
    icon = models.ImageField(upload_to = 'media/', default = None)

    def __str__(self):
        return self.title

    
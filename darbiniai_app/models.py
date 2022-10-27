from django.db import models

# Create your models here.

class Leaderboard(models.Model):

    gameName = models.CharField(max_length=100) # PK
    
    date_added = models.DateTimeField(auto_now_add=True) # when this leaderboard was added

    def __str__(self):
        return self.gameName

class Entry(models.Model):

    LB = models.ForeignKey(Leaderboard, on_delete=models.CASCADE) # FK - gameName
    
    username = models.CharField(max_length=20) # PK
    score = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True) # when an entry to the leaderboard was added

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        return self.username
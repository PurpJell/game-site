from socket import fromshare
from django import forms

from .models import Leaderboard

class LeaderboardForm(forms.ModelForm):
        class Meta:
            model = Leaderboard
            fields = [
                'gameName',
            ]
            labels = {'gameName': 'Game'}
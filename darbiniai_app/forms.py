from socket import fromshare
from django import forms

from .models import Leaderboard, Entry

class LeaderboardForm(forms.ModelForm):
        class Meta:
            model = Leaderboard
            fields = [
                'gameName',
            ]
            labels = {'gameName': 'Game'}


class EntryForm(forms.ModelForm):
        class Meta:
            model = Entry
            fields = [
                'username',
                'score',
            ]
            labels = {'username': 'Username','score':'Score'}
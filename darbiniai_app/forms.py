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


class LBEntryForm(forms.ModelForm):
        class Meta:
            model = Entry
            fields = [
                'score',
            ]
            labels = {'username': 'Username','score':'Score'}

class MEEntryForm(forms.ModelForm):
        class Meta:
            model = Entry
            fields = [
                'LB',
                'score',
            ]
            labels = {'username': 'Username','score':'Score'}
# from socket import fromshare
from django import forms

from .models import Leaderboard, Entry, Game
from django.contrib.auth.models import User


# formos, kurias pateikia site'ai, norint prideti arba editinti tam tikrus modelius 
class LeaderboardForm(forms.ModelForm):
        class Meta:
            model = Leaderboard
            fields = [
                'gameName',
            ]
            labels = {'gameName': 'Game'}


# pridedant entry per /leaderboards/
class LBEntryForm(forms.ModelForm):
        class Meta:
            model = Entry
            fields = [
                'score',
            ]
            labels = {'score':'Score'}

# pridedant entry per /my_entries/
class MEEntryForm(forms.ModelForm):
        class Meta:
            model = Entry
            fields = [
                'LB',
                'score',
            ]
            labels = {'LB':'Leaderboard', 'score':'Score'}

class changeUsernameForm(forms.ModelForm):
        class Meta:
            model = User
            fields = [
                'username',
            ]
            labels = {'username':'Username'}

class GameForm (forms.ModelForm):

    class Meta:
        model = Game
        fields = [
            'title',
            'icon',
            'file',
        ]
        # labels = {'title':'Game title'}
        labels = {'title':'Game title', 'icon':'Game icon', 'file':'Game file'}
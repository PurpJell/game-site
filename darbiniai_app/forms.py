# from socket import fromshare
from django import forms

from .models import Leaderboard, Entry, Game
from django.contrib.auth.models import User

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
            labels = {'score':'Score'}

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
                'username'
            ]
            labels = {'username':'Username'}

class GameForm (forms.ModelForm):

    class Meta:
        model = Game
        fields = [
            'icon'
        ]
        labels = {'icon':'Game icon'}
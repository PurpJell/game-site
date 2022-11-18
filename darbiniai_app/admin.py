from django.contrib import admin
from .models import Leaderboard, Entry, Game

# Register your models here.

admin.site.register(Leaderboard)
admin.site.register(Entry)
admin.site.register(Game)
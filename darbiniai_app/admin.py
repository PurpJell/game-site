from django.contrib import admin
from .models import Leaderboard, Entry, Game

# Register your models here.

# uzregistruoja modelius /admin/ site, kad butu galima juos matyti ir modifikuoti
admin.site.register(Leaderboard)
admin.site.register(Entry)
admin.site.register(Game)
"""Defines URL patterns for darbiniai_app"""

from django.urls import path, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.generic.base import RedirectView


from django.contrib import admin

app_name = 'darbiniai_app'

# prie url patternu reikia prideti visus norimus tureti url path'us, pvz darbiniai.herokuapp.com/leaderboards/, kuri accessinant kreipiamasi i views.py -> leaderboards()
urlpatterns = [
    # Home page
    path('', views.index, name = 'index'),

    # admin
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    path('admin/', admin.site.urls),

    # leaderboards (by django book)
    path('leaderboards/', views.leaderboards, name='leaderboards'),
    path('entries/<str:gameName>/', views.entries, name='entries'),
    path('my_entries/', views.my_entries, name='my_entries'),

    path('new_leaderboard/', views.new_leaderboard, name='new_leaderboard'),
    path('LBnew_entry/<str:gameName>/', views.LBnew_entry, name='LBnew_entry'),
    path('MEnew_entry/', views.MEnew_entry, name='MEnew_entry'),
    path('edit_leaderboard/<str:gameName>/', views.edit_leaderboard, name='edit_leaderboard'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('edit_game/<str:title>/', views.edit_game, name='edit_game'),
    path('delete_leaderboard/<str:gameName>/', views.delete_leaderboard, name='delete_leaderboard'),
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('submit_score/<str:gameName>/<int:score>', views.submit_score, name='submit_score'),

    path('account/', views.account, name='account'),
    path('account/change_username/', views.change_username, name='change_username'),
    path('account/change_password/', views.change_password, name='change_password'),
    path('account/delete_account/', views.delete_account, name='delete_account'),
    path('account_deleted/', views.account_deleted, name='account_deleted'),

    # (by internet, with an API)
    path('api/leaderboards/', views.leaderboard_list),
    #path('api/leaderboard/<str:gameName>/', views.leaderboard_detail), # useless

    path('api/entries/', views.entry_list),
    #path('api/entry/<str:gameName>/', views.leaderboard_detail), # useless

    #Files 
    path ('library/', views.library, name = 'library'),
    path ('add_game/', views.add_game, name = 'add_game'),
    path('game/<str:title>/',views.goto_game, name='goto_game'),
    path('delete_game/<str:title>', views.delete_game, name = 'delete_game'),

] + static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
"""Defines URL patterns for darbiniai_app"""

from django.urls import path

from . import views

app_name = 'darbiniai_app'
urlpatterns = [
    # Home page
    path('', views.index, name = 'index'),

    # leaderboards (by django book)
    path('leaderboards/', views.leaderboards, name='leaderboards'),
    path('entries/<str:gameName>/', views.entries, name='entries'),
    path('my_entries/', views.my_entries, name='my_entries'),

    path('new_leaderboard/', views.new_leaderboard, name='new_leaderboard'),
    path('LBnew_entry/<str:gameName>/', views.LBnew_entry, name='LBnew_entry'),
    path('MEnew_entry/', views.MEnew_entry, name='MEnew_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),

    # (by internet, with an API)
    path('api/leaderboards/', views.leaderboard_list),
    #path('api/leaderboard/<str:gameName>/', views.leaderboard_detail), # useless

    path('api/entries/', views.entry_list),
    #path('api/entry/<str:gameName>/', views.leaderboard_detail), # useless

]
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

    path('new_leaderboard/', views.new_leaderboard, name='new_leaderboard'),
    path('new_entry/<str:gameName>/', views.new_entry, name='new_entry'),

    # (by internet, with an API)
    path('api/leaderboards/', views.leaderboard_list),
    #path('api/leaderboard/<str:gameName>/', views.leaderboard_detail), # useless

    path('api/entries/', views.entry_list),
    #path('api/entry/<str:gameName>/', views.leaderboard_detail), # useless

]
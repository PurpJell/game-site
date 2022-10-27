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

    # (by internet, with an API)
    path('api/leaderboards/', views.leaderboard_list),
    path('api/leaderboards/<str:gameName>/', views.leaderboard_detail),

]
# urls.py
from django.urls import path
from . import views

app_name = 'projectile'

urlpatterns = [
    path('', views.index, name='index'), # Changed from 'simultion' to root for the menu
    path('simulation/', views.projectile_simulation, name='simulation'),
    path('practice/', views.practice, name='practice'),
    path('reset-progress/', views.reset_progress, name='reset_progress'), # Utility to restart game
    path('reload-question/', views.reload_question, name='reload_question'), # Reload current question
    path('reload-last-level/', views.reload_last_level, name='reload_last_level'), # Reload previous level
]
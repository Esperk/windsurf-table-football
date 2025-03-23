from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('match/<int:pk>/', views.MatchDetailView.as_view(), name='match-detail'),
    path('match/new/', views.create_match, name='match-create'),
    path('match/<int:pk>/update/', views.MatchUpdateView.as_view(), name='match-update'),
    path('match/<int:pk>/delete/', views.MatchDeleteView.as_view(), name='match-delete'),
    path('players/', views.PlayerListView.as_view(), name='player-list'),
    path('player/<int:pk>/', views.PlayerDetailView.as_view(), name='player-detail'),
    path('profile/update/', views.update_profile, name='profile-update'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
]

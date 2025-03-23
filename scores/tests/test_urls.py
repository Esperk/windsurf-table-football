import pytest
from django.urls import reverse, resolve
from scores.views import (
    HomeView, MatchDetailView, create_match, MatchUpdateView, 
    MatchDeleteView, PlayerListView, PlayerDetailView, 
    update_profile, LeaderboardView
)


class TestUrls:
    def test_home_url_resolves(self):
        url = reverse('home')
        assert resolve(url).func.view_class == HomeView
        
    def test_match_detail_url_resolves(self):
        url = reverse('match-detail', kwargs={'pk': 1})
        assert resolve(url).func.view_class == MatchDetailView
        
    def test_match_create_url_resolves(self):
        url = reverse('match-create')
        assert resolve(url).func == create_match
        
    def test_match_update_url_resolves(self):
        url = reverse('match-update', kwargs={'pk': 1})
        assert resolve(url).func.view_class == MatchUpdateView
        
    def test_match_delete_url_resolves(self):
        url = reverse('match-delete', kwargs={'pk': 1})
        assert resolve(url).func.view_class == MatchDeleteView
        
    def test_player_list_url_resolves(self):
        url = reverse('player-list')
        assert resolve(url).func.view_class == PlayerListView
        
    def test_player_detail_url_resolves(self):
        url = reverse('player-detail', kwargs={'pk': 1})
        assert resolve(url).func.view_class == PlayerDetailView
        
    def test_profile_update_url_resolves(self):
        url = reverse('profile-update')
        assert resolve(url).func == update_profile
        
    def test_leaderboard_url_resolves(self):
        url = reverse('leaderboard')
        assert resolve(url).func.view_class == LeaderboardView

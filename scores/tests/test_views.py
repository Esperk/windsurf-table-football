import pytest
import uuid
from django.urls import reverse
from django.contrib.auth.models import User
from scores.models import Player, Match, PlayerStats


@pytest.mark.django_db
class TestHomeView:
    def test_home_view_get(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert 'matches' in response.context
        assert 'top_players' in response.context
        assert 'is_paginated' in response.context


@pytest.mark.django_db
class TestLeaderboardView:
    def test_leaderboard_view_get(self, client):
        response = client.get(reverse('leaderboard'))
        assert response.status_code == 200
        assert 'stats' in response.context


@pytest.mark.django_db
class TestPlayerListView:
    def test_player_list_view_get(self, client):
        response = client.get(reverse('player-list'))
        assert response.status_code == 200
        assert 'players' in response.context


@pytest.mark.django_db
class TestPlayerDetailView:
    def test_player_detail_view_get(self, client):
        # Create a unique user
        username = f"testuser_detail_{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(username=username, password='password123')
        player = Player.objects.create(user=user, nickname='TestNick')
        
        response = client.get(reverse('player-detail', kwargs={'pk': player.pk}))
        assert response.status_code == 200
        assert response.context['player'] == player
        assert 'matches' in response.context


@pytest.mark.django_db
class TestMatchDetailView:
    def test_match_detail_view_get(self, client):
        # Create unique users
        user1 = User.objects.create_user(username=f"player1_detail_{uuid.uuid4().hex[:8]}", password='password123')
        user2 = User.objects.create_user(username=f"player2_detail_{uuid.uuid4().hex[:8]}", password='password123')
        player1 = Player.objects.create(user=user1, nickname='Player1')
        player2 = Player.objects.create(user=user2, nickname='Player2')
        
        # Create a match
        match = Match.objects.create(
            match_type='1v1',
            team1_player1=player1,
            team2_player1=player2,
            team1_score=5,
            team2_score=3
        )
        
        response = client.get(reverse('match-detail', kwargs={'pk': match.pk}))
        assert response.status_code == 200
        assert response.context['match'] == match


@pytest.mark.django_db
class TestMatchCreateView:
    def test_match_create_view_get_requires_login(self, client):
        response = client.get(reverse('match-create'))
        assert response.status_code == 302  # Redirects to login
        
    def test_match_create_view_get(self, client):
        # Create a unique user
        username = f"testuser_create_{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(username=username, password='password123')
        client.login(username=username, password='password123')
        
        response = client.get(reverse('match-create'))
        assert response.status_code == 200
        assert 'form' in response.context
        
    def test_match_create_view_post(self, client):
        # Create unique users
        username1 = f"player1_create_{uuid.uuid4().hex[:8]}"
        username2 = f"player2_create_{uuid.uuid4().hex[:8]}"
        user1 = User.objects.create_user(username=username1, password='password123')
        user2 = User.objects.create_user(username=username2, password='password123')
        
        player1 = Player.objects.create(user=user1, nickname='Player1')
        player2 = Player.objects.create(user=user2, nickname='Player2')
        
        # Create player stats
        PlayerStats.objects.create(player=player1)
        PlayerStats.objects.create(player=player2)
        
        # Login
        client.login(username=username1, password='password123')
        
        # Post data
        data = {
            'match_type': '1v1',
            'team1_player1': player1.id,
            'team2_player1': player2.id,
            'team1_score': 5,
            'team2_score': 3
        }
        
        response = client.post(reverse('match-create'), data=data)
        
        # Should create a new match and redirect to match detail
        assert Match.objects.count() == 1
        match = Match.objects.first()
        assert match.team1_player1 == player1
        assert match.team2_player1 == player2
        assert match.team1_score == 5
        assert match.team2_score == 3


@pytest.mark.django_db
class TestProfileUpdateView:
    def test_profile_update_view_get_requires_login(self, client):
        response = client.get(reverse('profile-update'))
        assert response.status_code == 302  # Redirects to login
        
    def test_profile_update_view_get(self, client):
        # Create a unique user
        username = f"testuser_profile_{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(username=username, password='password123')
        player = Player.objects.create(user=user, nickname='TestNick')
        
        # Login
        client.login(username=username, password='password123')
        
        response = client.get(reverse('profile-update'))
        assert response.status_code == 200
        assert 'form' in response.context
        
    def test_profile_update_view_post(self, client):
        # Create a unique user
        username = f"testuser_profile2_{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(username=username, password='password123')
        player = Player.objects.create(user=user, nickname='TestNick')
        
        # Login
        client.login(username=username, password='password123')
        
        # Post data
        data = {
            'nickname': 'NewNick',
            'profile_color': '#00FF00'
        }
        
        response = client.post(reverse('profile-update'), data=data)
        
        # Should update the player and redirect
        player.refresh_from_db()
        assert player.nickname == 'NewNick'
        assert player.profile_color == '#00FF00'

import pytest
from django.contrib.auth.models import User
from scores.models import Player, PlayerStats

@pytest.fixture
def create_user():
    """Factory fixture to create users with unique usernames"""
    users = {}
    
    def _create_user(username='testuser', password='password123'):
        if username in users:
            return users[username]
        
        user = User.objects.create_user(username=username, password=password)
        users[username] = user
        return user
    
    return _create_user

@pytest.fixture
def create_player():
    """Factory fixture to create players"""
    players = {}
    
    def _create_player(user, nickname=None, profile_color='#FF5733'):
        if user.username in players:
            return players[user.username]
        
        if nickname is None:
            nickname = f"Player_{user.username}"
            
        player = Player.objects.create(
            user=user,
            nickname=nickname,
            profile_color=profile_color
        )
        
        # Create stats for the player
        PlayerStats.objects.create(player=player)
        
        players[user.username] = player
        return player
    
    return _create_player

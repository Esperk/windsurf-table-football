import pytest
import uuid
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from scores.models import Player, Match, PlayerStats


@pytest.mark.django_db
class TestPlayerModel:
    def test_player_creation(self):
        # Create a unique username
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(username=username, password='password123')
        player = Player.objects.create(user=user, nickname='TestNick', profile_color='#FF5733')
        
        assert player.user == user
        assert player.nickname == 'TestNick'
        assert player.profile_color == '#FF5733'
        
    def test_player_str_with_nickname(self):
        # Create a unique username
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(username=username, password='password123')
        player = Player.objects.create(user=user, nickname='TestNick')
        
        assert str(player) == 'TestNick'
        
    def test_player_str_without_nickname(self):
        # Create a unique username
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(username=username, password='password123')
        player = Player.objects.create(user=user, nickname='')
        
        assert str(player) == username


@pytest.mark.django_db
class TestMatchModel:
    @pytest.fixture
    def setup_players(self):
        # Create unique usernames
        user1 = User.objects.create_user(username=f"player1_{uuid.uuid4().hex[:8]}", password='password123')
        user2 = User.objects.create_user(username=f"player2_{uuid.uuid4().hex[:8]}", password='password123')
        user3 = User.objects.create_user(username=f"player3_{uuid.uuid4().hex[:8]}", password='password123')
        user4 = User.objects.create_user(username=f"player4_{uuid.uuid4().hex[:8]}", password='password123')
        
        player1 = Player.objects.create(user=user1, nickname='Player1')
        player2 = Player.objects.create(user=user2, nickname='Player2')
        player3 = Player.objects.create(user=user3, nickname='Player3')
        player4 = Player.objects.create(user=user4, nickname='Player4')
        
        return player1, player2, player3, player4
    
    def test_1v1_match_creation(self, setup_players):
        player1, player2, _, _ = setup_players
        
        match = Match.objects.create(
            match_type='1v1',
            team1_player1=player1,
            team2_player1=player2,
            team1_score=5,
            team2_score=3
        )
        
        assert match.match_type == '1v1'
        assert match.team1_player1 == player1
        assert match.team2_player1 == player2
        assert match.team1_score == 5
        assert match.team2_score == 3
        assert match.team1_player2 is None
        assert match.team2_player2 is None
        
    def test_2v2_match_creation(self, setup_players):
        player1, player2, player3, player4 = setup_players
        
        match = Match.objects.create(
            match_type='2v2',
            team1_player1=player1,
            team1_player2=player2,
            team2_player1=player3,
            team2_player2=player4,
            team1_score=5,
            team2_score=3
        )
        
        assert match.match_type == '2v2'
        assert match.team1_player1 == player1
        assert match.team1_player2 == player2
        assert match.team2_player1 == player3
        assert match.team2_player2 == player4
        assert match.team1_score == 5
        assert match.team2_score == 3
        
    def test_match_winner_team1(self, setup_players):
        player1, player2, _, _ = setup_players
        
        match = Match.objects.create(
            match_type='1v1',
            team1_player1=player1,
            team2_player1=player2,
            team1_score=5,
            team2_score=3
        )
        
        assert match.winner == "Team 1"
        
    def test_match_winner_team2(self, setup_players):
        player1, player2, _, _ = setup_players
        
        match = Match.objects.create(
            match_type='1v1',
            team1_player1=player1,
            team2_player1=player2,
            team1_score=3,
            team2_score=5
        )
        
        assert match.winner == "Team 2"
        
    def test_match_winner_draw(self, setup_players):
        player1, player2, _, _ = setup_players
        
        match = Match.objects.create(
            match_type='1v1',
            team1_player1=player1,
            team2_player1=player2,
            team1_score=3,
            team2_score=3
        )
        
        assert match.winner == "Draw"
        
    def test_match_str_representation_1v1(self, setup_players):
        player1, player2, _, _ = setup_players
        
        match = Match.objects.create(
            match_type='1v1',
            team1_player1=player1,
            team2_player1=player2,
            team1_score=5,
            team2_score=3
        )
        
        expected_str = "Player1 vs Player2 - 5:3"
        assert str(match) == expected_str
        
    def test_match_str_representation_2v2(self, setup_players):
        player1, player2, player3, player4 = setup_players
        
        match = Match.objects.create(
            match_type='2v2',
            team1_player1=player1,
            team1_player2=player2,
            team2_player1=player3,
            team2_player2=player4,
            team1_score=5,
            team2_score=3
        )
        
        expected_str = "Player1 & Player2 vs Player3 & Player4 - 5:3"
        assert str(match) == expected_str


@pytest.mark.django_db
class TestPlayerStatsModel:
    def test_player_stats_creation(self):
        # Create a unique username
        username = f"testuser_stats_{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(username=username, password='password123')
        player = Player.objects.create(user=user, nickname='TestNick')
        
        stats = PlayerStats.objects.create(
            player=player,
            matches_played=10,
            matches_won=5,
            matches_lost=3,
            matches_drawn=2,
            goals_scored=20,
            goals_conceded=15
        )
        
        assert stats.player == player
        assert stats.matches_played == 10
        assert stats.matches_won == 5
        assert stats.matches_lost == 3
        assert stats.matches_drawn == 2
        assert stats.goals_scored == 20
        assert stats.goals_conceded == 15
        
    def test_win_percentage_calculation(self):
        # Create a unique username
        username = f"testuser_stats_{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(username=username, password='password123')
        player = Player.objects.create(user=user, nickname='TestNick')
        
        stats = PlayerStats.objects.create(
            player=player,
            matches_played=10,
            matches_won=5
        )
        
        assert stats.win_percentage == 50.0
        
    def test_win_percentage_zero_matches(self):
        # Create a unique username
        username = f"testuser_stats_{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(username=username, password='password123')
        player = Player.objects.create(user=user, nickname='TestNick')
        
        stats = PlayerStats.objects.create(
            player=player,
            matches_played=0,
            matches_won=0
        )
        
        assert stats.win_percentage == 0
        
    def test_player_stats_str(self):
        # Create a unique username
        username = f"testuser_stats_{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(username=username, password='password123')
        player = Player.objects.create(user=user, nickname='TestNick')
        
        stats = PlayerStats.objects.create(player=player)
        
        assert str(stats) == "Stats for TestNick"

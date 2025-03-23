from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from colorfield.fields import ColorField

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=True)
    profile_color = ColorField(default='#FF5733')
    
    def __str__(self):
        return self.nickname if self.nickname else self.user.username

class Match(models.Model):
    MATCH_TYPES = (
        ('1v1', '1 vs 1'),
        ('2v1', '2 vs 1'),
        ('2v2', '2 vs 2'),
    )
    
    match_type = models.CharField(max_length=3, choices=MATCH_TYPES)
    date_played = models.DateTimeField(auto_now_add=True)
    
    # Team 1
    team1_player1 = models.ForeignKey(Player, related_name='team1_player1_matches', on_delete=models.CASCADE)
    team1_player2 = models.ForeignKey(Player, related_name='team1_player2_matches', on_delete=models.CASCADE, null=True, blank=True)
    team1_score = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    
    # Team 2
    team2_player1 = models.ForeignKey(Player, related_name='team2_player1_matches', on_delete=models.CASCADE)
    team2_player2 = models.ForeignKey(Player, related_name='team2_player2_matches', on_delete=models.CASCADE, null=True, blank=True)
    team2_score = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    
    # Additional info
    notes = models.TextField(blank=True)
    
    def __str__(self):
        team1 = f"{self.team1_player1}"
        if self.team1_player2:
            team1 += f" & {self.team1_player2}"
            
        team2 = f"{self.team2_player1}"
        if self.team2_player2:
            team2 += f" & {self.team2_player2}"
            
        return f"{team1} vs {team2} - {self.team1_score}:{self.team2_score}"
    
    @property
    def winner(self):
        if self.team1_score > self.team2_score:
            return "Team 1"
        elif self.team2_score > self.team1_score:
            return "Team 2"
        else:
            return "Draw"
            
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validate match type and players
        if self.match_type == '1v1':
            if self.team1_player2 or self.team2_player2:
                raise ValidationError("1v1 matches should have only one player per team")
        elif self.match_type == '2v1':
            if not self.team1_player2 and not self.team2_player2:
                raise ValidationError("2v1 matches should have at least one team with two players")
            if self.team1_player2 and self.team2_player2:
                raise ValidationError("2v1 matches should have only one team with two players")
        elif self.match_type == '2v2':
            if not self.team1_player2 or not self.team2_player2:
                raise ValidationError("2v2 matches should have two players per team")

class PlayerStats(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='stats')
    matches_played = models.PositiveIntegerField(default=0)
    matches_won = models.PositiveIntegerField(default=0)
    matches_lost = models.PositiveIntegerField(default=0)
    matches_drawn = models.PositiveIntegerField(default=0)
    goals_scored = models.PositiveIntegerField(default=0)
    goals_conceded = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Stats for {self.player}"
    
    @property
    def win_percentage(self):
        if self.matches_played == 0:
            return 0
        return round((self.matches_won / self.matches_played) * 100, 2)

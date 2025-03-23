from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from .models import Player, Match, PlayerStats

@receiver(post_save, sender=User)
def create_player(sender, instance, created, **kwargs):
    # Skip signal during testing to avoid conflicts
    if getattr(settings, 'TESTING', False):
        return
        
    if created:
        Player.objects.get_or_create(user=instance)

@receiver(post_save, sender=Player)
def create_player_stats(sender, instance, created, **kwargs):
    # Skip signal during testing to avoid conflicts
    if getattr(settings, 'TESTING', False):
        return
        
    if created:
        PlayerStats.objects.get_or_create(player=instance)

@receiver(post_save, sender=Match)
def update_player_stats(sender, instance, created, **kwargs):
    # Skip signal during testing to avoid conflicts
    if getattr(settings, 'TESTING', False):
        return
        
    if created:
        # Update stats for all players involved in the match
        players = [instance.team1_player1, instance.team2_player1]
        if instance.team1_player2:
            players.append(instance.team1_player2)
        if instance.team2_player2:
            players.append(instance.team2_player2)
            
        for player in players:
            stats, _ = PlayerStats.objects.get_or_create(player=player)
            
            # Update matches played
            stats.matches_played += 1
            
            # Update wins, losses, draws
            if instance.winner == "Team 1" and (player == instance.team1_player1 or player == instance.team1_player2):
                stats.matches_won += 1
            elif instance.winner == "Team 2" and (player == instance.team2_player1 or player == instance.team2_player2):
                stats.matches_won += 1
            elif instance.winner == "Draw":
                stats.matches_drawn += 1
            else:
                stats.matches_lost += 1
                
            # Update goals
            if player == instance.team1_player1 or player == instance.team1_player2:
                stats.goals_scored += instance.team1_score
                stats.goals_conceded += instance.team2_score
            else:
                stats.goals_scored += instance.team2_score
                stats.goals_conceded += instance.team1_score
                
            stats.save()

from django.contrib import admin
from .models import Player, Match, PlayerStats

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'profile_color')
    search_fields = ('user__username', 'nickname')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'match_type', 'date_played', 'team1_score', 'team2_score', 'winner')
    list_filter = ('match_type', 'date_played')
    search_fields = ('team1_player1__nickname', 'team1_player2__nickname', 
                     'team2_player1__nickname', 'team2_player2__nickname')
    date_hierarchy = 'date_played'

@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ('player', 'matches_played', 'matches_won', 'matches_lost', 
                   'matches_drawn', 'goals_scored', 'goals_conceded', 'win_percentage')
    search_fields = ('player__nickname', 'player__user__username')
    readonly_fields = ('win_percentage',)

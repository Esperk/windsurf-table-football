from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Sum, F, Case, When, Value, IntegerField
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Match, Player, PlayerStats
from .forms import MatchForm, PlayerForm
from django.db import models

class HomeView(ListView):
    model = Match
    template_name = 'scores/home.html'
    context_object_name = 'matches'
    ordering = ['-date_played']
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_players'] = PlayerStats.objects.order_by('-matches_won')[:5]
        return context

class MatchDetailView(DetailView):
    model = Match
    template_name = 'scores/match_detail.html'

@login_required
def create_match(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save()
            
            # Update player stats
            players = [
                match.team1_player1,
                match.team2_player1
            ]
            
            if match.team1_player2:
                players.append(match.team1_player2)
            if match.team2_player2:
                players.append(match.team2_player2)
            
            for player in players:
                stats, created = PlayerStats.objects.get_or_create(player=player)
                stats.matches_played += 1
                
                # Determine if player is on team 1 or team 2
                on_team1 = player in [match.team1_player1, match.team1_player2]
                
                if on_team1:
                    stats.goals_scored += match.team1_score
                    stats.goals_conceded += match.team2_score
                    if match.team1_score > match.team2_score:
                        stats.matches_won += 1
                    elif match.team1_score < match.team2_score:
                        stats.matches_lost += 1
                    else:
                        stats.matches_drawn += 1
                else:
                    stats.goals_scored += match.team2_score
                    stats.goals_conceded += match.team1_score
                    if match.team2_score > match.team1_score:
                        stats.matches_won += 1
                    elif match.team2_score < match.team1_score:
                        stats.matches_lost += 1
                    else:
                        stats.matches_drawn += 1
                
                stats.save()
            
            messages.success(request, 'Match recorded successfully!')
            return redirect('match-detail', pk=match.pk)
    else:
        form = MatchForm()
    
    return render(request, 'scores/match_form.html', {'form': form})

class MatchUpdateView(LoginRequiredMixin, UpdateView):
    model = Match
    form_class = MatchForm
    template_name = 'scores/match_form.html'
    
    def get_success_url(self):
        return reverse_lazy('match-detail', kwargs={'pk': self.object.pk})

class MatchDeleteView(LoginRequiredMixin, DeleteView):
    model = Match
    template_name = 'scores/match_confirm_delete.html'
    success_url = reverse_lazy('home')

class PlayerListView(ListView):
    model = Player
    template_name = 'scores/player_list.html'
    context_object_name = 'players'
    
    def get_queryset(self):
        return Player.objects.annotate(
            total_matches=Count('team1_player1_matches') + 
                          Count('team1_player2_matches') + 
                          Count('team2_player1_matches') + 
                          Count('team2_player2_matches')
        ).order_by('-total_matches')

class PlayerDetailView(DetailView):
    model = Player
    template_name = 'scores/player_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = self.object
        
        # Get all matches involving this player
        context['matches'] = Match.objects.filter(
            Q(team1_player1=player) | 
            Q(team1_player2=player) | 
            Q(team2_player1=player) | 
            Q(team2_player2=player)
        ).order_by('-date_played')
        
        return context

@login_required
def update_profile(request):
    try:
        player = request.user.player
    except Player.DoesNotExist:
        player = Player(user=request.user)
    
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('player-detail', pk=player.pk)
    else:
        form = PlayerForm(instance=player)
    
    return render(request, 'scores/profile_form.html', {'form': form})

class LeaderboardView(ListView):
    model = PlayerStats
    template_name = 'scores/leaderboard.html'
    context_object_name = 'stats'
    
    def get_queryset(self):
        return PlayerStats.objects.filter(matches_played__gt=0).annotate(
            win_percentage_calc=Case(
                When(matches_played=0, then=Value(0)),
                default=F('matches_won') * 100.0 / F('matches_played'),
                output_field=models.FloatField()
            )
        ).order_by('-win_percentage_calc', '-matches_won')

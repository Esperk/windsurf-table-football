from django import forms
from django.core.exceptions import ValidationError
from .models import Match, Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['nickname', 'profile_color']
        widgets = {
            'profile_color': forms.TextInput(attrs={'type': 'color'}),
        }

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = [
            'match_type', 
            'team1_player1', 'team1_player2', 'team1_score',
            'team2_player1', 'team2_player2', 'team2_score',
            'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team1_player2'].required = False
        self.fields['team2_player2'].required = False
        
        # Add CSS classes for styling
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control animate__animated animate__fadeIn'})
    
    def clean(self):
        cleaned_data = super().clean()
        match_type = cleaned_data.get('match_type')
        team1_player1 = cleaned_data.get('team1_player1')
        team1_player2 = cleaned_data.get('team1_player2')
        team2_player1 = cleaned_data.get('team2_player1')
        team2_player2 = cleaned_data.get('team2_player2')
        
        # Validate match type and players
        if match_type == '1v1':
            if team1_player2 or team2_player2:
                raise ValidationError("1v1 matches should have only one player per team")
        elif match_type == '2v1':
            if not (team1_player2 or team2_player2):
                raise ValidationError("2v1 matches should have at least one team with two players")
            if team1_player2 and team2_player2:
                raise ValidationError("2v1 matches should have only one team with two players")
        elif match_type == '2v2':
            if not team1_player2 or not team2_player2:
                raise ValidationError("2v2 matches should have two players per team")
        
        # Validate that a player is not playing against themselves
        all_players = [p for p in [team1_player1, team1_player2, team2_player1, team2_player2] if p]
        if len(all_players) != len(set(all_players)):
            raise ValidationError("A player cannot play against themselves")
        
        return cleaned_data

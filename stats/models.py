from django.db import models

class Game(models.Model):
    game_id = models.CharField(max_length=20, unique=True)
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

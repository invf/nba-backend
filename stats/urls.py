from django.urls import path
from .views import todays_games, game_details

urlpatterns = [
    path("todays_games/", todays_games, name="todays_games"),
    path("game/<str:game_id>/", game_details, name="game_details"),  # Додає ендпоінт для деталей матчу
]

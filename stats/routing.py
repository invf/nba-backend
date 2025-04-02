from django.urls import re_path
from .consumers import (NBAStatsConsumer,  # 🏀 Додаємо окремий клас для Today's Games
)

websocket_urlpatterns = [
    re_path(r"^ws/game/(?P<game_id>\d+)/$", NBAStatsConsumer.as_asgi()),
    re_path(r"^ws/todays_games/$", NBAStatsConsumer.as_asgi()),  # ✅ Використовуємо окремий клас
    re_path(r"^ws/quarter_stats/$", NBAStatsConsumer.as_asgi()),  # ✅ Окремий клас
    re_path(r"^ws/player_stats/$", NBAStatsConsumer.as_asgi()),  # ✅ Окремий клас
]

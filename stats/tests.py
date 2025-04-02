from nba_api.live.nba.endpoints import boxscore

game_id = "0022400920"  # Твій реальний gameId
box = boxscore.BoxScore(game_id)

# Вивід даних
game_details = box.game_details.get_dict()
print("🔍 gameStatusText:", game_details.get("gameStatusText", "❌ Немає даних"))

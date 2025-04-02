import requests
from django.http import JsonResponse

NBA_SCOREBOARD_URL = "https://nba-prod-us-east-1-mediaops-stats.s3.amazonaws.com/NBA/liveData/scoreboard/todaysScoreboard_00.json"

def todays_games(request):
    """Повертає всі матчі, що відбуваються сьогодні"""
    response = requests.get(NBA_SCOREBOARD_URL)

    if response.status_code == 200:
        data = response.json()
        games = data.get("scoreboard", {}).get("games", [])

        game_list = []
        for game in games:
            game_list.append({
                "game_id": game["gameId"],
                "home_team": game["homeTeam"]["teamName"],
                "away_team": game["awayTeam"]["teamName"],
                "home_score": game["homeTeam"]["score"],
                "away_score": game["awayTeam"]["score"],
                "game_time": game["gameTimeUTC"],
                "arena": game.get("arenaName", "Невідома арена"),
                "status": game["gameStatusText"],
                "home_leader": game.get("gameLeaders", {}).get("homeLeaders", {}),
                "away_leader": game.get("gameLeaders", {}).get("awayLeaders", {}),
                "home_periods": game["homeTeam"].get("periods", []),
                "away_periods": game["awayTeam"].get("periods", [])
            })

        return JsonResponse({"games": game_list}, safe=False)
    return JsonResponse({"error": "API недоступне"}, status=500)


def game_details(request, game_id):
    response = requests.get(NBA_SCOREBOARD_URL)

    if response.status_code == 200:
        data = response.json()
        games = data.get("scoreboard", {}).get("games", [])

        # Знайти потрібний матч по його ID
        game_data = next((game for game in games if game["gameId"] == game_id), None)

        if game_data:
            return JsonResponse(game_data, safe=False)
        else:
            return JsonResponse({"error": "Game not found"}, status=404)

    return JsonResponse({"error": "API unavailable"}, status=500)

import json
import requests
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from nba_api.live.nba.endpoints import boxscore

NBA_SCOREBOARD_URL = "https://nba-prod-us-east-1-mediaops-stats.s3.amazonaws.com/NBA/liveData/scoreboard/todaysScoreboard_00.json"


class NBAStatsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.keep_running = True
        asyncio.create_task(self.send_nba_stats())

    async def disconnect(self, close_code):
        self.keep_running = False

    async def send_nba_stats(self):
        while self.keep_running:
            try:
                # Отримуємо список матчів
                response = requests.get(
                    NBA_SCOREBOARD_URL,
                    timeout=30,
                    headers={"Cache-Control": "no-cache", "Pragma": "no-cache"}
                )
                response.raise_for_status()
                data = response.json()

                games = data.get("scoreboard", {}).get("games", [])

                game_list = []
                detailed_stats = {}

                for game in games:
                    game_id = game.get("gameId", "N/A")
                    home_team = game.get("homeTeam", {})
                    away_team = game.get("awayTeam", {})
                    game_leaders = game.get("gameLeaders", {})

                    home_leader = game_leaders.get("homeLeaders", {})
                    away_leader = game_leaders.get("awayLeaders", {})

                    # Основна інформація про матч
                    game_info = {
                        "game_id": game_id,
                        "home_team": home_team.get("teamName", "Unknown"),
                        "away_team": away_team.get("teamName", "Unknown"),
                        "home_score": home_team.get("score", 0),
                        "away_score": away_team.get("score", 0),
                        "game_time": game.get("gameTimeUTC", "N/A"),
                        "status": game.get("gameStatusText", "Unknown"),
                        "home_wins": home_team.get("wins", 0),
                        "home_losses": home_team.get("losses", 0),
                        "away_wins": away_team.get("wins", 0),
                        "away_losses": away_team.get("losses", 0),
                        "home_periods": home_team.get("periods", []),
                        "away_periods": away_team.get("periods", []),
                        "home_leader": {
                            "name": home_leader.get("name", "N/A"),
                            "points": home_leader.get("points", 0),
                            "rebounds": home_leader.get("rebounds", 0),
                            "assists": home_leader.get("assists", 0),
                        },
                        "away_leader": {
                            "name": away_leader.get("name", "N/A"),
                            "points": away_leader.get("points", 0),
                            "rebounds": away_leader.get("rebounds", 0),
                            "assists": away_leader.get("assists", 0),
                        }
                    }

                    game_list.append(game_info)

                    # Детальна статистика для кожної гри
                    try:
                        box = boxscore.BoxScore(game_id)
                        game_data = box.get_dict()

                        if "game" in game_data:
                            home_team_data = game_data["game"].get("homeTeam", {})
                            away_team_data = game_data["game"].get("awayTeam", {})

                            detailed_stats[game_id] = {
                                "home_team": {
                                    "name": home_team_data.get("teamName", "Unknown"),
                                    "score": home_team_data.get("score", 0),
                                    "rebounds": home_team_data.get("statistics", {}).get("reboundsTotal", 0),
                                    "assists": home_team_data.get("statistics", {}).get("assists", 0),
                                    "turnovers": home_team_data.get("statistics", {}).get("turnoversTotal", 0),
                                    "steals": home_team_data.get("statistics", {}).get("steals", 0),
                                    "blocks": home_team_data.get("statistics", {}).get("blocks", 0),
                                    "fgp": round(home_team_data.get("statistics", {}).get("fieldGoalsPercentage", 0) * 100, 1),
                                    "3pp": round(home_team_data.get("statistics", {}).get("threePointersPercentage", 0) * 100, 1),
                                    "ftp": round(home_team_data.get("statistics", {}).get("freeThrowsPercentage", 0) * 100, 1),
                                },
                                "away_team": {
                                    "name": away_team_data.get("teamName", "Unknown"),
                                    "score": away_team_data.get("score", 0),
                                    "rebounds": away_team_data.get("statistics", {}).get("reboundsTotal", 0),
                                    "assists": away_team_data.get("statistics", {}).get("assists", 0),
                                    "turnovers": away_team_data.get("statistics", {}).get("turnoversTotal", 0),
                                    "steals": away_team_data.get("statistics", {}).get("steals", 0),
                                    "blocks": away_team_data.get("statistics", {}).get("blocks", 0),
                                    "fgp": round(away_team_data.get("statistics", {}).get("fieldGoalsPercentage", 0) * 100, 1),
                                    "3pp": round(away_team_data.get("statistics", {}).get("threePointersPercentage", 0) * 100, 1),
                                    "ftp": round(away_team_data.get("statistics", {}).get("freeThrowsPercentage", 0) * 100, 1),
                                },
                            }
                        else:
                            print(f"❌ Детальна статистика не знайдена для game_id: {game_id}")

                    except Exception as e:
                        print(f"⚠️ Помилка отримання детальної статистики для game_id {game_id}: {e}")

                # Відправлення даних
                await self.send(text_data=json.dumps({
                    "games": game_list,
                    "detailed_stats": detailed_stats
                }))

            except requests.exceptions.RequestException as e:
                print(f"❌ Помилка отримання матчів: {e}")
            except json.JSONDecodeError as e:
                print(f"❌ Помилка розбору JSON: {e}")
            except Exception as e:
                print(f"❌ Несподівана помилка: {e}")

            await asyncio.sleep(10)  # Оновлення кожні 10 секунд

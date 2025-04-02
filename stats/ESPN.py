import openai

# 🔑 Введіть ваш OpenAI API ключ
OPENAI_API_KEY = "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"

# 🔹 Функція для обробки тексту через OpenAI API
def generate_match_summary(match_text):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional sports journalist."},
            {"role": "user", "content": f"Rewrite the following NBA match preview in a more engaging and professional way:\n\n{match_text}"}
        ],
        max_tokens=500
    )

    return response.choices[0].message.content

# 🔹 Тестовий текст матчу
match_text = """
Portland Trail Blazers (28-37, 12th in the Western Conference) vs. Golden State Warriors (36-28, sixth in the Western Conference)San Francisco; Monday, 10 p.m. EDTWarriors -11.5; over/under is 231BOTTOM LINE: Portland looks to end its three-game skid with a win over Golden State.The Warriors are 20-19 in Western Conference games. Golden State ranks third in the NBA with 29.1 assists per game led by Stephen Curry averaging 6.2.The Trail Blazers are 15-29 in Western Conference play. Portland is ninth in the Western Conference with 44.0 rebounds per game led by Donovan Clingan averaging 7.1.The Warriors average 15.2 made 3-pointers per game this season, 2.3 more made shots on average than the 12.9 per game the Trail Blazers allow. The Trail Blazers average 12.5 made 3-pointers per game this season, 0.6 fewer makes per game than the Warriors give up.TOP PERFORMERS: Curry is scoring 24.5 points per game with 4.4 rebounds and 6.2 assists for the Warriors. Jimmy Butler is averaging 14.8 points and 4.4 rebounds while shooting 45.9% over the last 10 games.Anfernee Simons is averaging 19.3 points and 4.9 assists for the Trail Blazers. Shaedon Sharpe is averaging 19.8 points over the last 10 games.LAST 10 GAMES: Warriors: 9-1, averaging 120.0 points, 45.8 rebounds, 31.5 assists, 9.9 steals and 5.0 blocks per game while shooting 46.4% from the field. Their opponents have averaged 107.3 points per game.Trail Blazers: 5-5, averaging 117.4 points, 46.3 rebounds, 25.0 assists, 8.7 steals and 4.6 blocks per game while shooting 45.9% from the field. Their opponents have averaged 112.2 points.INJURIES: Warriors: Brandin Podziemski: day to day (back), Jonathan Kuminga: day to day (ankle).Trail Blazers: Deandre Ayton: out (calf), Matisse Thybulle: out (ankle), Dalano Banton: day to day (personal), Deni Avdija: out (quad), Robert Williams III: out (knee).
"""

# 🔥 Виклик API для генерації покращеного тексту
summary = generate_match_summary(match_text)
print(summary)

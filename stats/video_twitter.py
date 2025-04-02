import os
import json
import datetime
import subprocess
import snscrape.modules.twitter as sntwitter

# 🔹 Налаштування
USERNAME = "NBA"  # Замініть на ім'я акаунту (без @)
DOWNLOAD_DIR = "twitter_videos"
HOURS_BACK = 12  # Період, за який потрібно знайти відео

# 🔹 Функція для пошуку твітів з відео
def get_recent_tweets_with_videos(username, hours=12):
    """Отримує список твітів із відео за останні X годин"""
    since_time = (datetime.datetime.utcnow() - datetime.timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S UTC")
    query = f"from:{username} filter:videos since:{since_time}"

    video_urls = []
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if "video" in tweet.media:
            video_urls.append(tweet.media[0].variants[-1]["url"])  # Найкраща якість

    return video_urls

# 🔹 Функція для завантаження відео
def download_videos(video_urls):
    """Завантажує відео зі списку URL"""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    for idx, url in enumerate(video_urls):
        output_file = os.path.join(DOWNLOAD_DIR, f"video_{idx+1}.mp4")
        print(f"⬇️ Завантаження відео: {url}")

        # Використовуємо yt-dlp для скачування
        command = ["yt-dlp", "-o", output_file, url]
        subprocess.run(command, check=True)

    print("✅ Завантаження завершено!")

# 🔹 Виконання скрипту
if __name__ == "__main__":
    print(f"🔎 Пошук відео на {USERNAME} за останні {HOURS_BACK} годин...")
    video_links = get_recent_tweets_with_videos(USERNAME, HOURS_BACK)

    if video_links:
        print(f"✅ Знайдено {len(video_links)} відео! Починаємо завантаження...")
        download_videos(video_links)
    else:
        print("❌ Відео не знайдено!")

from news_find import google_news
from twitter import create_tweet_with_image, create_reply
from datetime import datetime, timedelta
import csv
import schedule
import time

CSV_FILE = "shared_news.csv"

def save_shared_news(url):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([url, timestamp])

# Eski haberleri temizle (7 günden eski olanları sil)
def clean_old_news():
    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)
    rows_to_keep = []

    try:
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                timestamp = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
                if timestamp >= seven_days_ago:
                    rows_to_keep.append(row)

        # Dosyayı yeniden yaz
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["url", "timestamp"])
            writer.writeheader()
            writer.writerows(rows_to_keep)
    except FileNotFoundError:
        pass  # Dosya yoksa hiçbir şey yapma

def start():
    news = google_news()
    try:
        tweet_text = news["title"]
        image_url = news["image"]

        # Resimli tweet paylaş
        tweet_id = create_tweet_with_image(tweet_text, image_url)
        if tweet_id:
            reply_text = f"{news['summary']}"
            create_reply(reply_text, tweet_id)
            save_shared_news(news["url"])  # Yeni haber URL'sini ve tarihini kaydet

    except Exception as e:
        print(f"Beklenmedik hata: {e}")
        pass


# Zamanlama
schedule.every().day.at("12:00").do(start)
schedule.every().day.at("13:30").do(start)
schedule.every().day.at("15:00").do(start)
schedule.every().day.at("16:30").do(start)
schedule.every().day.at("18:00").do(start)
schedule.every().day.at("19:30").do(start)
schedule.every().day.at("21:00").do(start)
schedule.every().day.at("22:30").do(start)

# # # Her gün eski haberleri temizle
schedule.every().day.at("00:00").do(clean_old_news)

while True:
    schedule.run_pending()
    time.sleep(1)

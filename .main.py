import time
import schedule
import csv
from datetime import datetime, timedelta
from trend_news import get_trending_news
from summary import summarize_article
from twitter import create_tweet_with_image, create_reply

from newspaper.article import ArticleException

# CSV dosyası adı
CSV_FILE = "shared_news.csv"

# CSV dosyasından paylaşılan haberleri oku
def load_shared_news():
    shared_news = set()
    try:
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                shared_news.add(row["url"])  # URL'leri bir küme olarak döndür
                
    except FileNotFoundError:
        pass  # Dosya yoksa boş küme döndür
    return shared_news

# Yeni haber URL'sini ve tarihini CSV dosyasına ekle
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

def post_trending_news():
    trending_news = get_trending_news()
    shared_news = load_shared_news()  # Paylaşılan haberleri yükle
    for news in trending_news:
        if news["url"] not in shared_news:
            try:
                article = summarize_article(news["url"])
                tweet_text = article["title"]
                image_url = article["image"]

                # Resimli tweet paylaş
                tweet_id = create_tweet_with_image(tweet_text, image_url)
                if tweet_id:
                    reply_text = f"{article['summary']}"
                    create_reply(reply_text, tweet_id)
                    save_shared_news(news["url"])  # Yeni haber URL'sini ve tarihini kaydet
                    break  # Her seferinde sadece bir haber paylaş
            except ArticleException as e:
                print(f"Haber indirme hatası (403): {e}")
                continue  # Bir sonraki habere geç
            except Exception as e:
                print(f"Beklenmedik hata: {e}")
                continue  # Bir sonraki habere geç

# Zamanlama
schedule.every(1).minutes.do(post_trending_news)
# # schedule.every().day.at("23:52").do(post_trending_news)
# # schedule.every().day.at("14:00").do(post_trending_news)
# # schedule.every().day.at("16:00").do(post_trending_news)
# # schedule.every().day.at("18:00").do(post_trending_news)
# # schedule.every().day.at("20:00").do(post_trending_news)
# # schedule.every().day.at("22:00").do(post_trending_news)
# # schedule.every().day.at("24:00").do(post_trending_news)

# # Her gün eski haberleri temizle
# schedule.every().day.at("00:00").do(clean_old_news)

while True:
    schedule.run_pending()
    time.sleep(1)


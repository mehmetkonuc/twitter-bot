import tweepy
import requests

API_KEY = "EJK7W9IYumPR2lvH15tpWpBue"
API_SECRET = "uRSG3rRnAqhJRtlOVkOkVyAwoqQ8ZfY5TvhVFvseAUT8umr8bo"
ACCESS_TOKEN = "1894693466883416064-aETtrEdbyD2cYicLocD3ATehPNe5yr"
ACCESS_TOKEN_SECRET = "qaaIAhdIVPQl4ug6ns9BFvGYQqiCB0nnEpVYS2t9HuHQ0"

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Resmi indir ve Twitter'a yükle
def upload_media(image_url):
    try:
        # Resmi indir
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open("temp_image.jpg", "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            # Resmi Twitter'a yükle
            media = api.media_upload("temp_image.jpg")
            return media.media_id_string  # Medya ID'sini döndür
    except Exception as e:
        print(f"Resim yükleme hatası: {e}")
    return None

# Tweet paylaşımı (resimli)
def create_tweet_with_image(text, image_url):
    media_id = upload_media(image_url)
    if media_id:
        try:
            response = client.create_tweet(text=text, media_ids=[media_id])
            print("Resimli tweet başarıyla paylaşıldı!")
            return response.data["id"]  # Paylaşılan tweet'in ID'sini döndür
        except tweepy.TweepyException as e:
            print(f"Hata oluştu: {e}")
    return None

def create_reply(text, tweet_id):
    try:
        tweet_text = f"📰 {text}"

        response = client.create_tweet(text=tweet_text, in_reply_to_tweet_id=tweet_id)
        print("Yanıt tweet'i başarıyla paylaşıldı!")
        return response.data["id"]
    except tweepy.TweepyException as e:
        print(f"Hata oluştu: {e}")
        return None
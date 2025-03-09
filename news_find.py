from gnews import GNews
import random
import csv
from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from newspaper import Article
from googlenewsdecoder import gnewsdecoder


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

def original_url(url):
    interval_time = 1  # interval is optional, default is None
    source_url = url
    try:
        decoded_url = gnewsdecoder(source_url, interval=interval_time)
        if decoded_url.get("status"):
            return decoded_url["decoded_url"]
        else:
            print("Error:", decoded_url["message"])
    except Exception as e:
        print(f"Error occurred: {e}")

def format_summary_for_premium(summary):
    # Her cümleyi yeni bir satıra yerleştir ve paragraf gibi boşluk bırak
    formatted_summary = "\n\n".join(str(sentence) for sentence in summary)
    return formatted_summary


def google_news():
    # GNews nesnesi oluştur
    google_news = GNews(language='tr', country='TR', period='7d', max_results=10)

    # İlgilendiğiniz kategoriler
    kategoriler = ['ENTERTAINMENT', 'HEALTH', 'CELEBRITIES', 'TV', 'MUSIC', 'MOVIES', 'THEATER', 'MENTAL HEALTH', 'ARTS-DESIGN', 'BEAUTY', 'TRAVEL', 'SHOPPING', 'FASHION']

    # Kategorileri karıştır (random.shuffle kullanarak)
    random.shuffle(kategoriler)

    # Haber bulunana kadar kategorileri dene
    haberler = []
    for kategori in kategoriler:
        print(f"{kategori} kategorisindeki haberler çekiliyor...")
        haberler = google_news.get_news_by_topic(kategori)
        if haberler:  # Eğer haber varsa döngüyü kır
            shared_news = load_shared_news()
            for haber in haberler:
                google_news_url = haber['url']  # Google News yönlendirme linki
                url = original_url(google_news_url)
                if url not in shared_news:
                    try:
                        # Newspaper3k ile haber içeriğini çek
                        article = Article(url)
                        article.download()
                        article.parse()
                        article.nlp()  # Doğal dil işleme ile özetleme yapar
                        
                        parser = PlaintextParser.from_string(article.text, Tokenizer("turkish"))
                        summarizer = LsaSummarizer()
                        summary = summarizer(parser.document, 10)  # 3 cümlelik özet
                        formatted_summary = format_summary_for_premium(summary)

                        haber = {
                            "title": article.title,
                            "image": article.top_image,
                            "summary": formatted_summary,
                            'url' : article.url,
                        }
                        return haber

                    except Exception as e:
                        print(f"Hata oluştu: {e}")
                        continue
            break
            
        else:
            print(f"{kategori} kategorisinde haber bulunamadı. Başka bir kategori deneniyor...")
            continue
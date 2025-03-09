from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from langdetect import detect

def is_turkish(text):
    try:
        return detect(text) == 'tr'
    except:
        return False

def summarize_article(url):
    article = Article(url)
    article.download()
    article.parse()

    if not is_turkish(article.text):
        return None  # Eğer haber Türkçe değilse None döndür

    parser = PlaintextParser.from_string(article.text, Tokenizer("turkish"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 10)  # 3 cümlelik özet

    return {
        "title": article.title,
        "image": article.top_image,
        "summary": " ".join(str(sentence) for sentence in summary)
    }

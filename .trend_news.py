import feedparser

def contains_excluded_words(title, excluded_words):
    """
    Başlıkta belirtilen yasaklı kelimelerin olup olmadığını kontrol eder.
    Kelimeler bitişik olsa bile algılar.
    """
    title_lower = title.lower()
    for word in excluded_words:
        if word.lower() in title_lower:
            return True
    return False

def get_trending_news():
    rss_url = "https://trends.google.com/trending/rss?geo=TR"
    feed = feedparser.parse(rss_url)
    trending_news = []

    # Yasaklı kelimeler listesi
    excluded_words = ["spor", "ezan", "iftar"]

    for entry in feed.entries:
        try:
            title = entry.title
            link = entry.ht_news_item_url

            # Eğer başlıkta yasaklı kelimeler yoksa listeye ekle
            if not contains_excluded_words(title, excluded_words):
                trending_news.append({"title": title, "url": link})
        except:
            pass

    return trending_news
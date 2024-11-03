import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd

def fetch_articles(keyword, start_date, end_date):
    articles = []
    current_date = start_date
    while current_date <= end_date:
        url = f"https://tw.yahoo.com/news/search?q={keyword}&date={current_date.strftime('%Y-%m-%d')}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for item in soup.find_all('a', href=True):
            title = item.get_text()
            link = item['href']
            # 設置過濾文章標題或內容關鍵字
            if "劉德華" in title:
                articles.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'title': title,
                    'link': link
                })
        
        current_date += timedelta(days=1)
    return articles

# 定義日期區間
start_date = datetime(2024, 10, 1)
end_date = datetime(2024, 10, 31)
articles = fetch_articles("劉德華", start_date, end_date)
df = pd.DataFrame(articles)

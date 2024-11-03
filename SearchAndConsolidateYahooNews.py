import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_yahoo_news_articles(keyword, start_date, end_date):
    base_url = "https://tw.news.yahoo.com"
    search_url = f"{base_url}/search?p={keyword}"
    articles = []

    # 模擬頁面請求與解析
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        news_list = soup.select('.StreamContainer a', href=True)  # 根據Yahoo的HTML結構，獲取所有新聞連結
        
        for news in news_list:
            article_url = news['href']
            if article_url.startswith("/"):
                article_url = base_url + article_url
            
            # 抓取文章詳細內容
            article_response = requests.get(article_url)
            if article_response.status_code == 200:
                article_soup = BeautifulSoup(article_response.text, "lxml")
                # 取得文章的日期
                date_str = article_soup.find("time")["datetime"]
                article_date = datetime.fromisoformat(date_str.split("T")[0])

                # 檢查日期是否符合範圍
                if start_date <= article_date <= end_date:
                    # 獲取文章標題和內容
                    title = article_soup.find("h1").get_text()
                    paragraphs = article_soup.find_all("p")
                    content = " ".join([p.get_text() for p in paragraphs])
                    
                    # 萃取出新聞重點
                    summary = summarize_content(content)
                    
                    # 儲存至文章列表
                    articles.append({
                        "title": title,
                        "url": article_url,
                        "date": article_date.strftime("%Y-%m-%d"),
                        "summary": summary
                    })
    return articles

def summarize_content(content):
    # 簡易摘要方法：取前200字為重點
    return content[:200] + "..."

# 指定搜尋條件
keyword = "劉德華"
start_date = datetime(2024, 11, 1)
end_date = datetime(2024, 11, 3)
articles = fetch_yahoo_news_articles(keyword, start_date, end_date)




def generate_html(articles):
    html_content = "<html><head><title>Yahoo 新聞 - 劉德華 11月新聞重點</title></head><body>"
    html_content += "<h1>Yahoo 新聞 - 劉德華 10月新聞重點</h1>"

    for article in articles:
        html_content += f"<h2>{article['title']}</h2>"
        html_content += f"<p><a href='{article['url']}'>查看完整文章</a></p>"
        html_content += f"<p><strong>日期：</strong> {article['date']}</p>"
        html_content += f"<p><strong>重點：</strong> {article['summary']}</p><hr>"

    html_content += "</body></html>"
    return html_content

# 儲存為HTML檔案
html_output = generate_html(articles)
with open("yahoo_news_summary.html", "w", encoding="utf-8") as file:
    file.write(html_output)

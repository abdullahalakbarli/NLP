import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import pandas as pd

base_url = "https://anspress.com"
category_url = "https://anspress.com/xeberler/ekologiya"

news_data = []

response = requests.get(category_url)
if response.status_code != 200:
    print(f"Failed to retrieve the page, status code: {response.status_code}")
    exit()

soup = BeautifulSoup(response.content, "html.parser")

articles = soup.select("div.post-item-horizontal a")

news_links = []
for article in articles:
    if "href" in article.attrs:
        full_link = urljoin(base_url, article["href"])
        if full_link not in news_links:
            news_links.append(full_link)
    if len(news_links) >= 100:
        break  

for index, link in enumerate(news_links):
    try:
        article_response = requests.get(link)
        if article_response.status_code != 200:
            print(f"Failed to access news page {link}")
            continue

        article_soup = BeautifulSoup(article_response.content, "html.parser")
        title_tag = article_soup.select_one("h1")
        title = title_tag.get_text(strip=True) if title_tag else "No Title"

        content_tag = article_soup.select_one("div.post-content")
        content = content_tag.get_text("\n", strip=True) if content_tag else "No Content"

        news_data.append({"Başlıq": title, "Link": link, "Məqalə": content})

        print(f"{index + 1}. Başlıq: {title}")
        print(f"Link: {link}")
        print(f"Məqalə (ilk 300 simvol):\n{content[:300]}...")
        print("-" * 80)

        time.sleep(1)

    except Exception as e:
        print(f"Error processing {link}: {e}")

df = pd.DataFrame(news_data)
df.to_csv("anspress_ekologiya_news.csv", index=False, encoding="utf-8")

print(f"\nToplam {len(news_data)} xəbər toplandı! Məlumatlar 'anspress_ekologiya_news.csv' faylında saxlanıldı.")

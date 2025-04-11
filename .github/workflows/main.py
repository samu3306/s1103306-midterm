import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.billboard.com/charts/hot-100/"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

#儲存結果
results = []

#先抓第一名資料
first_item = soup.select_one("div.o-chart-results-list-row-container")
items = first_item.find_all("li")

if first_item:
    #抓歌名
    rank_tag = first_item.find("span", class_="c-label a-font-primary-bold-l")
    rank = rank_tag.get_text(strip=True) if rank_tag else "" 
    title_tag = first_item.select_one("h3#title-of-a-story")
    title = title_tag.get_text(strip=True) if title_tag else ""
    text_items = [li.get_text(strip=True) for li in items if li.get_text(strip=True)]
    # 抓歌手
    artist_tag = first_item.select_one("span.c-label.a-no-trucate") or first_item.select_one("span.c-label.a-truncate-ellipsis")
    artist = artist_tag.get_text(strip=True) if artist_tag else ""
    # 抓統計數字
    number_tags = first_item.select("li span.c-label.a-font-primary-m")
    numbers = [tag.get_text(strip=True) for tag in number_tags if tag.get_text(strip=True)]
    rank = "1"
    last_week = text_items[3] if len(text_items) > 2 else ""  #上週排名
    peak = text_items[4] if len(text_items) > 3 else ""     #最高排名）
    weeks = text_items[5] if len(text_items) > 4 else ""    #總周數

    results.append([rank, title, artist, last_week, peak, weeks])

# 接下來處理其他排名
rows = soup.select("div.o-chart-results-list-row-container")

for row in rows[1:]:  # 跳過第一名
    rank_tag = row.select_one("span.c-label.a-font-primary-bold-l")
    title_tag = row.select_one("h3#title-of-a-story")
    artist_tag = row.select_one("span.c-label.a-no-trucate") or row.select_one("span.c-label.a-truncate-ellipsis")

    number_tags = row.select("li span.c-label.a-font-primary-m")
    numbers = [tag.get_text(strip=True) for tag in number_tags if tag.get_text(strip=True)]

    rank = rank_tag.get_text(strip=True) if rank_tag else ""
    title = title_tag.get_text(strip=True) if title_tag else ""
    artist = artist_tag.get_text(strip=True) if artist_tag else ""
    last_week = numbers[0] if len(numbers) > 0 else ""
    peak = numbers[1] if len(numbers) > 1 else ""
    weeks = numbers[2] if len(numbers) > 2 else ""

    results.append([rank, title, artist, last_week, peak, weeks])


# 轉換成 DataFrame
df = pd.DataFrame(results, columns=["Rank", "Title", "Artist", "Last Week", "Peak Position", "Weeks on Chart"])

# 儲存成 CSV
df.to_csv("billboard_hot_100.csv", index=False, encoding="utf-8-sig")

print("Data has been saved to 'billboard_hot_100.csv'.")


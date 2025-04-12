import requests
import pandas as pd
from datetime import datetime
from datetime import timezone, timedelta
import os

API_KEY = '94faece3b1289de731ec94cbc6553680'
url = f'https://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key={API_KEY}&format=json&limit=100'

res = requests.get(url)
data = res.json()

tracks = data['tracks']['track']

results = []
for t in tracks:
    name = t['name']
    artist = t['artist']['name']
    playcount = t['playcount']
    url = t['url']
    results.append([name, artist, playcount, url])
# 建立資料夾（例如存放在 data/）
os.makedirs("data", exist_ok=True)

taiwan_time = datetime.now(timezone(timedelta(hours=8)))
timestamp = taiwan_time.strftime("%Y%m%d_%H%M")
filename = f"data/API_last_fm{timestamp}.csv"

df = pd.DataFrame(results, columns=['Title', 'Artist', 'Playcount', 'URL'])
# 儲存成 CSV
df.to_csv(filename, index=False, encoding="utf-8-sig")

print(f"Data has been saved to '{filename}'.")

import requests
import pandas as pd

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

df = pd.DataFrame(results, columns=['Title', 'Artist', 'Playcount', 'URL'])
df.to_csv('lastfm_top_tracks.csv', index=False, encoding='utf-8-sig')

print("✅ 抓取成功，儲存為 lastfm_top_tracks.csv")

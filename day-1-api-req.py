import requests
import json


url='https://api.worldnewsapi.com/top-news'
params={
   "source-country":"us",
   "language":"en",
   "date":"2025-12-01",
   "api-key":"16939e9a16d848c7ae63126454fbe7dc" 
    }


response=requests.get(url,params=params)
if response.status_code==200:
    news=response.json()
    if "top_news" in news:
        print(f"Title:{news['top_news'][0]['title']}")
        print(f"Description:{news['top_news'][0]['text']}")
    else:
        print("No top news found in the response.")
            
else:
    print(f"Failed to fetch news. Status code:{response.status_code}")
            
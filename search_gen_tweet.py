# search_gen_tweet.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import csv
from typing import List, Dict

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.kenkensz9.com"],  # すべてのオリジンを許可する（セキュリティ上、特定のオリジンを指定するのが良い）
    allow_credentials=True,
    allow_methods=["GET"]  # すべてのHTTPメソッドを許可する
   # allow_headers=["*"],  # すべてのヘッダーを許可する
)
# 仮のツイートデータ
tweets = [
    {"id": 1, "content": "これはテストツイートです。"},
    {"id": 2, "content": "FastAPIは素晴らしいです！"},
    {"id": 3, "content": "ツイート検索のサンプルです。"}
]

def load_tweets(file_path: str) -> List[Dict[str, str]]:
    tweets = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:  # Assuming the format is id,text
                tweet_id, tweet_text = row
                tweets.append({"id": tweet_id, "text": tweet_text})
                #print({"id": tweet_id, "text": tweet_text})
    return tweets

# データのロード
tweets = load_tweets("./全ツイート一覧.txt")

#tweets=open("/root/webfile/全ツイート一覧.txt","r",encoding="utf-8")
#tw=tweets.read()
#tw=tw.split("\n")

class Tweet(BaseModel):
    id: str
    text: str

@app.get("/tweets", response_model=List[Tweet])
async def search_tweets(query: str = Query(..., description="Search query")):
    # クエリに基づいてツイートをフィルタリング
    result = [tweet for tweet in tweets if query.lower() in tweet["text"].lower()]
    return result

app.mount("/", StaticFiles(directory="/var/www/html", html=True), name="static")

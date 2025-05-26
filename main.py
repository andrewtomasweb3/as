import tweepy
import time
import os
import json
from dotenv import load_dotenv
from datetime import datetime
import random

# Load API keys
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Auth
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Track engagement history
HISTORY_FILE = "history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {"tweet_ids": [], "user_ids": []}
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

# Define crypto-related search queries
SEARCH_TERMS = [
    "#pinksale",
    "#CryptoPresale",
    "#launchpad",
    "#Web3",
    "#DeFi",
    "site:pinksale.finance"
]

def engage():
    history = load_history()
    print(f"[{datetime.now()}] Starting engagement cycle...")

    for query in SEARCH_TERMS:
        try:
            tweets = api.search_tweets(q=query + " -filter:retweets", lang="en", count=10, tweet_mode="extended")
            for tweet in tweets:
                tweet_id = tweet.id
                user_id = tweet.user.id
                screen_name = tweet.user.screen_name

                # Skip if already engaged
                if tweet_id in history["tweet_ids"] or user_id in history["user_ids"]:
                    continue

                try:
                    api.create_favorite(tweet_id)
                    api.create_friendship(user_id)
                    print(f"✅ Engaged with @{screen_name} | Tweet: {tweet_id}")
                    history["tweet_ids"].append(tweet_id)
                    history["user_ids"].append(user_id)
                    save_history(history)
                    time.sleep(random.randint(10, 20))  # vary delay
                except Exception as e:
                    print(f"❌ Failed with @{screen_name}: {e}")
        except Exception as e:
            print(f"Search error for query '{query}': {e}")

    print("🟢 Engagement cycle complete.\n")

# Loop it 24/7 with delay between cycles
if __name__ == "__main__":
    while True:
        engage()
        time.sleep(60 * 60)  # run every hour

# scripts/post_tweet.py
import os, sys

REQUIRED = ["TWITTER_API_KEY","TWITTER_API_SECRET","TWITTER_ACCESS_TOKEN","TWITTER_ACCESS_TOKEN_SECRET"]
missing = [k for k in REQUIRED if not os.getenv(k)]

# ツイート本文を取得（STEP1で作るtweet.txt）
tweet_text = ""
if os.path.exists("tweet.txt"):
    tweet_text = open("tweet.txt", "r", encoding="utf-8").read().strip()
if not tweet_text:
    tweet_text = "自動テスト投稿：tweet.txt が見つからなかったためデフォルト文を投稿（またはスキップ）。"

# Secrets が無いときは“スキップして成功終了”
if missing:
    print("⚠️ Twitter Secrets が未設定のため投稿をスキップします。")
    print("必要なSecrets:", ", ".join(REQUIRED))
    print("ツイート候補:\n", tweet_text)
    sys.exit(0)

# ここから実投稿
import tweepy
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
api = tweepy.API(auth)

resp = api.update_status(status=tweet_text)
print("✅ 投稿完了:", resp.id)

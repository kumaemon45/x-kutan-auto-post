# scripts/generate_tweet.py
from datetime import datetime

def build_tweet():
    base = "くーたん博士のAIメモ：今日の学び。生成AIを“目的”ではなく“手段”にする。まず顧客価値→ワークフロー→最後にモデル最適化。#生成AI #X自動投稿"
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    tweet = f"{base}\n{now}"
    return tweet[:280]  # 280文字に収める

if __name__ == "__main__":
    text = build_tweet()
    print(text)  # ログ確認用
    with open("tweet.txt", "w", encoding="utf-8") as f:
        f.write(text)  # 後続が読むファイル

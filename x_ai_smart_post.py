#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X (Twitter) 生成AI情報自動投稿スクリプト (GitHub Actions版)
くーたん博士風の親しみやすい口調で投稿
"""

import os
import logging
import sys
from datetime import datetime

try:
    import tweepy
except ImportError:
    print("エラー: tweepyライブラリがインストールされていません")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("エラー: openaiライブラリがインストールされていません")
    sys.exit(1)


# ログ設定
LOG_FILE = "x_ai_smart_post.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# 文字数制限
MAX_TWEET_LENGTH = 280


def load_config_from_env() -> dict:
    """環境変数から認証情報を読み込む"""
    config = {
        'api_key': os.getenv('X_API_KEY'),
        'api_secret': os.getenv('X_API_SECRET'),
        'access_token': os.getenv('X_ACCESS_TOKEN'),
        'access_token_secret': os.getenv('X_ACCESS_TOKEN_SECRET')
    }
    
    # 必須項目のチェック
    missing_keys = [key for key, value in config.items() if not value]
    
    if missing_keys:
        raise ValueError(f"環境変数が設定されていません: {', '.join(missing_keys)}")
    
    return config


def create_api_client(config: dict) -> tweepy.Client:
    """X API v2クライアントを作成"""
    client = tweepy.Client(
        consumer_key=config['api_key'],
        consumer_secret=config['api_secret'],
        access_token=config['access_token'],
        access_token_secret=config['access_token_secret']
    )
    return client


def research_ai_trends() -> str:
    """
    LLMを使用して生成AI最新トレンドをリサーチ
    
    Returns:
        str: リサーチ結果のサマリー
    """
    logger.info("生成AI最新トレンドをリサーチ中...")
    
    # OpenAI APIキーを環境変数から取得
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY環境変数が設定されていません")
    
    client = OpenAI(api_key=api_key)
    
    # 現在の日付を取得
    current_date = datetime.now().strftime('%Y年%m月%d日')
    
    prompt = f"""今日は{current_date}です。

生成AI分野の最新トレンドや注目ニュースについて、以下の観点から簡潔にまとめてください：

1. 最近の重要な技術発表やアップデート
2. 注目されている新しいAIモデルやサービス
3. 業界で話題になっているトピック
4. 今後の展望や期待されている動向

300文字程度で、ポイントを絞って説明してください。"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "あなたは生成AI技術の最新動向に詳しい専門家です。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        research_result = response.choices[0].message.content.strip()
        logger.info(f"リサーチ完了: {len(research_result)}文字")
        return research_result
        
    except Exception as e:
        logger.error(f"リサーチエラー: {e}")
        return "生成AI分野は日々進化しており、ChatGPT、Claude、Geminiなどの大規模言語モデルが注目を集めています。"


def generate_tweet_with_insight(research_data: str) -> str:
    """
    リサーチ結果から所感付きツイートを生成（くーたん博士風）
    
    Args:
        research_data: リサーチ結果
        
    Returns:
        str: 生成されたツイート本文
    """
    logger.info("所感付きツイートを生成中（くーたん博士風）...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    
    prompt = f"""以下の生成AI最新トレンド情報をもとに、魅力的なツイートを作成してください。

【最新トレンド情報】
{research_data}

【要件】
- 280文字以内の日本語で作成
- 「くーたん博士」というキャラクターとして投稿
- 親しみやすく、かわいい口調を使用（「〜だよ」「〜なの」「〜だね」「わくわく」「すごい」「びっくり」など）
- 最新トレンドのポイントを簡潔に紹介
- くーたん博士としての所感や考察を必ず含める
- 読者に語りかけるような親しみやすい表現
- ハッシュタグを1〜2個含める（#生成AI #AI #ChatGPT #Claude など）
- かわいい絵文字を2〜3個使用（🤖✨💡🎨🌟😊🚀など）
- ポジティブで前向きなトーン
- 専門的な内容も分かりやすく説明

【くーたん博士の口調例】
- 「〜だよ！」「〜なんだよね」「〜だと思うの」
- 「すごいね！」「わくわくするね！」「びっくりだよ！」
- 「みんなも〜してみてね」「一緒に〜しよう」

ツイート本文のみを出力してください。説明や前置きは不要です。"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "あなたは『くーたん博士』という生成AI技術に詳しいキャラクターです。親しみやすく、かわいい口調で、専門的な内容を分かりやすく楽しく伝えるのが得意です。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.9
        )
        
        tweet_text = response.choices[0].message.content.strip()
        
        # 引用符を削除（もしあれば）
        tweet_text = tweet_text.strip('"').strip("'")
        
        # 文字数チェック
        if len(tweet_text) > MAX_TWEET_LENGTH:
            logger.warning(f"生成されたツイートが長すぎます（{len(tweet_text)}文字）。切り詰めます。")
            tweet_text = tweet_text[:MAX_TWEET_LENGTH-3] + "..."
        
        logger.info(f"ツイート生成完了: {len(tweet_text)}文字")
        logger.info(f"生成内容: {tweet_text}")
        return tweet_text
        
    except Exception as e:
        logger.error(f"ツイート生成エラー: {e}")
        return "生成AIの世界、今日もすごい進化してるよ🤖✨ 新しい技術がどんどん出てきてワクワクが止まらないの！みんなも一緒に楽しもうね💡 #生成AI #AI"


def post_tweet(client: tweepy.Client, text: str) -> bool:
    """ツイートを投稿"""
    try:
        if len(text) > MAX_TWEET_LENGTH:
            logger.error(f"ツイートが長すぎます（{len(text)}文字 > {MAX_TWEET_LENGTH}文字）")
            return False
        
        response = client.create_tweet(text=text)
        
        if response.data:
            tweet_id = response.data['id']
            logger.info(f"ツイート投稿成功: ID={tweet_id}")
            logger.info(f"投稿内容: {text}")
            return True
        else:
            logger.error("ツイート投稿失敗: レスポンスが空です")
            return False
            
    except tweepy.TweepyException as e:
        logger.error(f"ツイート投稿失敗: {e}")
        return False
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        return False


def main():
    """メイン処理"""
    logger.info("=" * 60)
    logger.info("X 生成AI情報自動投稿スクリプト開始（くーたん博士モード）")
    logger.info("=" * 60)
    
    try:
        # 環境変数から認証情報を読み込み
        logger.info("環境変数から認証情報を読み込み中...")
        config = load_config_from_env()
        logger.info("認証情報読み込み完了")
        
        # APIクライアント作成
        logger.info("APIクライアント作成中...")
        client = create_api_client(config)
        logger.info("APIクライアント作成完了")
        
        # 生成AI最新トレンドをリサーチ
        research_data = research_ai_trends()
        
        # 所感付きツイートを生成（くーたん博士風）
        tweet_text = generate_tweet_with_insight(research_data)
        
        # ツイート投稿
        logger.info("ツイート投稿中...")
        if post_tweet(client, tweet_text):
            logger.info("✓ ツイート投稿が正常に完了しました")
            sys.exit(0)
        else:
            logger.error("✗ ツイート投稿に失敗しました")
            sys.exit(1)
            
    except ValueError as e:
        logger.error(f"設定エラー: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)
    finally:
        logger.info("=" * 60)
        logger.info("X 生成AI情報自動投稿スクリプト終了")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()


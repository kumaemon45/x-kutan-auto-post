#!/usr/bin/env python3
"""
X AI Auto Tweet Generator
生成AIトレンドをリサーチし、くーたん博士風のツイートを生成してGitHub Issueに投稿
"""

import os
import sys
import logging
from datetime import datetime
from openai import OpenAI

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tweet_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def research_ai_trends() -> str:
    """
    LLMを使用して生成AI最新トレンドをリサーチ
    
    Returns:
        str: リサーチ結果のサマリー
    """
    logger.info("生成AI最新トレンドをリサーチ中...")
    
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "あなたは生成AI分野の専門家です。最新のトレンドや技術動向について、正確で分かりやすい情報を提供します。"
                },
                {
                    "role": "user",
                    "content": f"""
現在の日付: {datetime.now().strftime('%Y年%m月')}

生成AI分野の最新トレンドについて、以下の観点でサマリーを作成してください：
1. 最新の技術動向（新しいモデル、機能など）
2. 産業界での活用事例
3. 今後の展望や注目ポイント

300文字程度で簡潔にまとめてください。
"""
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        research_result = response.choices[0].message.content.strip()
        logger.info(f"リサーチ完了: {len(research_result)}文字")
        return research_result
        
    except Exception as e:
        logger.error(f"リサーチエラー: {e}")
        # フォールバック: デフォルトのトレンド情報
        return "2025年、生成AIは大きく進化しています。マルチモーダルAIが注目され、テキスト・画像・音声を統合した新しいサービスが次々と登場しています。企業での活用も加速し、カスタマイズされたAIソリューションが普及しています。"


def generate_kutan_tweet(research_summary: str) -> str:
    """
    リサーチ結果をもとに、くーたん博士風のツイートを生成
    
    Args:
        research_summary: リサーチ結果のサマリー
        
    Returns:
        str: 生成されたツイート内容（280文字以内）
    """
    logger.info("所感付きツイートを生成中（くーたん博士風）...")
    
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """あなたは「くーたん博士」という親しみやすいAI専門家のキャラクターです。

キャラクター設定：
- 語尾: 「〜だよ」「〜だね」「〜なんだ」
- 口調: 親しみやすく、かわいらしい
- 絵文字: 適度に使用（✨🤖💡🌟🎨など）
- 特徴: 最新AI技術に詳しく、分かりやすく説明するのが得意

ツイートの要件：
- 280文字以内（厳守）
- 生成AIの最新トレンドを分かりやすく紹介
- 個人的な所感や感想を含める
- ポジティブで前向きなトーン
- ハッシュタグ: #生成AI #AI を含める
"""
                },
                {
                    "role": "user",
                    "content": f"""
以下のリサーチ結果をもとに、くーたん博士としてツイートを作成してください：

{research_summary}

要件：
- 280文字以内
- くーたん博士の口調で
- 所感や感想を含める
- ハッシュタグ #生成AI #AI を含める
"""
                }
            ],
            temperature=0.8,
            max_tokens=300
        )
        
        tweet = response.choices[0].message.content.strip()
        
        # 280文字制限チェック
        if len(tweet) > 280:
            logger.warning(f"ツイートが長すぎます（{len(tweet)}文字）。短縮します...")
            # 280文字に切り詰め
            tweet = tweet[:277] + "..."
        
        logger.info(f"ツイート生成完了: {len(tweet)}文字")
        logger.info(f"生成内容: {tweet}")
        
        return tweet
        
    except Exception as e:
        logger.error(f"ツイート生成エラー: {e}")
        # フォールバック
        return "みんな、こんにちは！くーたん博士だよ😊✨ 生成AIの世界は毎日進化していて、わくわくが止まらないね！新しい技術がどんどん出てきて、未来が楽しみだよ🚀 一緒にAIの可能性を探求しようね💡 #生成AI #AI"


def main():
    """メイン処理"""
    logger.info("=" * 60)
    logger.info("X AI Tweet Generator 開始（くーたん博士モード）")
    logger.info("=" * 60)
    
    try:
        # 1. 生成AIトレンドをリサーチ
        research_summary = research_ai_trends()
        
        # 2. くーたん博士風のツイートを生成
        tweet = generate_kutan_tweet(research_summary)
        
        # 3. 結果を出力（GitHub Actionsで使用）
        print("\n" + "=" * 60)
        print("📝 生成されたツイート")
        print("=" * 60)
        print(tweet)
        print("=" * 60)
        print(f"\n文字数: {len(tweet)}/280")
        print("\n✅ ツイート生成完了！")
        
        # GitHub Actionsの環境変数に出力
        if os.getenv('GITHUB_OUTPUT'):
            with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
                # 改行を含む値を正しく出力
                f.write(f"tweet<<EOF\n{tweet}\nEOF\n")
                f.write(f"char_count={len(tweet)}\n")
        
        logger.info("=" * 60)
        logger.info("X AI Tweet Generator 終了")
        logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())


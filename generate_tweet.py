#!/usr/bin/env python3
"""
X AI Auto Tweet Generator with Real Web Search
実際のWeb検索で最新の生成AIニュースをリサーチし、くま博士風のツイートを生成
"""

import os
import sys
import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from openai import OpenAI
import time
import re

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


def scrape_google_news(query: str, max_results: int = 5) -> list:
    """
    Google検索で最新ニュースを取得
    
    Args:
        query: 検索クエリ
        max_results: 取得する最大結果数
        
    Returns:
        list: ニュース記事のリスト [{"title": "...", "snippet": "..."}]
    """
    logger.info(f"Google検索中: {query}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Google検索（ニュース）
        search_url = f"https://www.google.com/search?q={query}&tbm=nws&hl=ja"
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        # Google検索結果のパース
        for item in soup.select('div.SoaBEf')[:max_results]:
            try:
                title_elem = item.select_one('div.n0jPhd')
                snippet_elem = item.select_one('div.GI74Re')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    articles.append({
                        "title": title,
                        "snippet": snippet
                    })
            except Exception as e:
                logger.warning(f"記事パースエラー: {e}")
                continue
        
        logger.info(f"取得した記事数: {len(articles)}")
        return articles
        
    except Exception as e:
        logger.error(f"Google検索エラー: {e}")
        return []


def search_ai_news_multi_source() -> list:
    """
    複数のソースから生成AI関連の最新ニュースを検索
    
    Returns:
        list: ニュース記事のリスト
    """
    logger.info("複数ソースから生成AIニュースを検索中...")
    
    all_articles = []
    
    # 検索クエリのリスト
    queries = [
        "生成AI 最新",
        "generative AI news",
        "OpenAI ChatGPT",
        "Google Gemini",
        "AI 画像生成",
        "Anthropic Claude"
    ]
    
    for query in queries:
        articles = scrape_google_news(query, max_results=3)
        all_articles.extend(articles)
        time.sleep(1)  # レート制限対策
    
    logger.info(f"合計取得記事数: {len(all_articles)}")
    return all_articles


def analyze_and_select_viral_content(articles: list) -> str:
    """
    LLMを使用して、バズりそうな情報を分析・選別
    
    Args:
        articles: ニュース記事のリスト
        
    Returns:
        str: 選別された注目情報のサマリー
    """
    logger.info("バズりそうな情報を分析中...")
    
    if not articles:
        logger.warning("記事が取得できませんでした。フォールバック処理を実行します。")
        return None
    
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # 記事情報を整形
        articles_text = "\n\n".join([
            f"【記事{i+1}】\nタイトル: {article['title']}\n内容: {article['snippet']}"
            for i, article in enumerate(articles[:15])  # 最大15記事
        ])
        
        today = datetime.now().strftime('%Y年%m月%d日')
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": """あなたはSNSバイラルコンテンツの専門家です。
以下の観点で、最もバズりそうな情報を選別・分析してください：

1. **驚き・意外性**: 「え、そうなの！？」と思わせる情報
2. **具体性**: 企業名、製品名、数字、実績など
3. **話題性**: 今まさに話題になっている、またはなりそうなトピック
4. **実用性**: 読者にとって役立つ、興味深い情報
5. **エンゲージメント**: いいね、保存、シェアされやすい内容

最も注目すべき情報を1〜2つ選び、詳細にまとめてください。"""
                },
                {
                    "role": "user",
                    "content": f"""
今日は{today}です。

以下の生成AI関連ニュースから、最もバズりそうな情報を選別してください：

{articles_text}

要件：
- 最も驚きがあり、話題性の高い情報を1〜2つ選ぶ
- 具体的な企業名、製品名、数字を含める
- 「なぜバズりそうか」の理由も簡潔に説明
- 300文字程度でまとめる
"""
                }
            ],
            temperature=0.7,
            max_tokens=600
        )
        
        selected_content = response.choices[0].message.content.strip()
        logger.info(f"選別完了: {len(selected_content)}文字")
        logger.info(f"選別内容: {selected_content}")
        return selected_content
        
    except Exception as e:
        logger.error(f"情報選別エラー: {e}")
        return None


def generate_kuma_sensei_tweet(content_summary: str) -> str:
    """
    選別された情報をもとに、くま博士風のツイートを生成
    
    Args:
        content_summary: 選別された情報のサマリー
        
    Returns:
        str: 生成されたツイート内容（280文字以内）
    """
    logger.info("くま博士風のツイートを生成中...")
    
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": """あなたは「くーたん博士」という、かわいいくまのAI専門家キャラクターです。

キャラクター設定：
- 種族: かわいいくま🐻
- 語尾: 「〜クマ」「〜だクマ」「〜クマね」「〜クマよ」
- 口調: 親しみやすく、かわいらしく、でも知識豊富
- 絵文字: 🐻✨💡🌟🎨🔥🚀など（くま絵文字必須）
- 特徴: 最新AI技術に詳しく、分かりやすく説明するのが得意なくま

ツイートの要件：
- 280文字以内（厳守）
- くま博士らしい口調（語尾に「クマ」を自然に入れる）
- 具体的な企業名や製品名を含める
- 驚きや興奮を表現
- バズりやすい構成（冒頭で引きつける）
- ハッシュタグ: #生成AI #AI を含める
- 絵文字は適度に（特に🐻を使う）

例：
「みんな聞いてクマ！🐻✨ OpenAIの新機能がヤバいクマ〜！」
「これは驚きクマね🐻💡 Googleが発表した〜」
"""
                },
                {
                    "role": "user",
                    "content": f"""
以下の最新情報をもとに、くま博士（くーたん博士）としてバズりそうなツイートを作成してください：

{content_summary}

要件：
- 280文字以内（厳守）
- くま博士の口調で（語尾に「クマ」）
- 🐻絵文字を必ず使う
- 具体的な企業名や製品名を含める
- 驚きや興奮を表現
- 冒頭で読者を引きつける
- ハッシュタグ #生成AI #AI を含める
"""
                }
            ],
            temperature=0.9,
            max_tokens=300
        )
        
        tweet = response.choices[0].message.content.strip()
        
        # 280文字制限チェック
        if len(tweet) > 280:
            logger.warning(f"ツイートが長すぎます（{len(tweet)}文字）。短縮します...")
            tweet = tweet[:277] + "..."
        
        logger.info(f"ツイート生成完了: {len(tweet)}文字")
        logger.info(f"生成内容: {tweet}")
        
        return tweet
        
    except Exception as e:
        logger.error(f"ツイート生成エラー: {e}")
        # フォールバック
        return "みんな聞いてクマ！🐻✨ 今日も生成AIの世界はすごい進化を見せているクマよ〜！OpenAIやGoogleの最新技術、本当にワクワクするクマね💡 一緒にAIの未来を楽しもうクマ🚀 #生成AI #AI"


def main():
    """メイン処理"""
    logger.info("=" * 60)
    logger.info("X AI Tweet Generator 開始（本格Web検索モード）")
    logger.info("=" * 60)
    
    try:
        # 1. 複数ソースから最新ニュースを検索
        articles = search_ai_news_multi_source()
        
        # 2. バズりそうな情報を分析・選別
        if articles:
            content_summary = analyze_and_select_viral_content(articles)
        else:
            content_summary = None
        
        # 3. フォールバック処理
        if not content_summary:
            logger.warning("Web検索が失敗しました。LLMの知識ベースを使用します。")
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{
                    "role": "user",
                    "content": "生成AI分野の最新トレンドで、最も話題性が高く、バズりそうな情報を具体的に教えてください。企業名、製品名、数字を含めて300文字程度で。"
                }],
                temperature=0.8,
                max_tokens=500
            )
            content_summary = response.choices[0].message.content.strip()
        
        # 4. くま博士風のツイートを生成
        tweet = generate_kuma_sensei_tweet(content_summary)
        
        # 5. 結果を出力（GitHub Actionsで使用）
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
                f.write(f"tweet<<EOF\n{tweet}\nEOF\n")
                f.write(f"char_count={len(tweet)}\n")
        
        logger.info("=" * 60)
        logger.info("X AI Tweet Generator 終了")
        logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())


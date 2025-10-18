# 🤖 X AI Tweet Generator - くーたん博士

GitHub Actionsで生成AI最新トレンドを自動リサーチし、くーたん博士風のツイートを自動生成するシステムです。

## ✨ 特徴

- 🔍 **自動リサーチ**: OpenAI APIで生成AI分野の最新トレンドを調査
- 💬 **くーたん博士風**: 親しみやすくかわいい口調でツイート生成
- ⏰ **定期実行**: 毎日9時、12時、18時に自動生成
- 📋 **GitHub Issue通知**: 生成されたツイートをIssueで通知
- 🆓 **完全無料**: GitHub ActionsとOpenAI APIのみ使用

## 🚀 使い方

### 1. 自動生成されたツイートを確認

毎日9時、12時、18時に、GitHub Issuesに新しいツイート案が投稿されます。

### 2. ツイートを投稿

1. Issueに記載されたツイート内容をコピー
2. X (Twitter) にアクセス
3. 内容を貼り付けて投稿

### 3. 手動で再生成

内容が気に入らない場合、Actionsタブから手動実行できます。

## ⚙️ セットアップ

### GitHub Secretsの設定

リポジトリの Settings → Secrets and variables → Actions で以下を追加：

- `OPENAI_API_KEY`: OpenAIのAPI Key

### 実行スケジュール

- 毎日 9時 (JST)
- 毎日 12時 (JST)
- 毎日 18時 (JST)

---

**Created by くーたん博士 🤖✨**

# X 生成AI情報自動投稿システム（GitHub Actions版）

くーたん博士が生成AI最新情報を自動でツイート！🤖✨

## 概要

このリポジトリは、GitHub Actionsを使用して、X（旧Twitter）に生成AI関連の最新情報を自動投稿するシステムです。

### 特徴

- 🤖 **くーたん博士風の親しみやすい口調**
- ✨ **LLMによる最新トレンドリサーチ**
- 💡 **所感を含む魅力的なツイート生成**
- 🚀 **GitHub Actionsで完全無料の自動投稿**
- 📅 **毎日9時、12時、18時に自動実行**

## セットアップ手順

### 1. リポジトリをフォーク

このリポジトリをあなたのGitHubアカウントにフォークしてください。

### 2. X API認証情報の取得

[X Developer Portal](https://developer.twitter.com/)で以下を取得：

1. **API Key** (Consumer Key)
2. **API Secret** (Consumer Secret)
3. **Access Token**
4. **Access Token Secret**

⚠️ **重要**: アプリの権限を **"Read and Write"** に設定してください。

### 3. GitHub Secretsの設定

リポジトリの `Settings` → `Secrets and variables` → `Actions` → `New repository secret` で以下を追加：

| Secret名 | 説明 |
|---------|------|
| `X_API_KEY` | X API Key (Consumer Key) |
| `X_API_SECRET` | X API Secret (Consumer Secret) |
| `X_ACCESS_TOKEN` | X Access Token |
| `X_ACCESS_TOKEN_SECRET` | X Access Token Secret |
| `OPENAI_API_KEY` | OpenAI API Key |

### 4. GitHub Actionsの有効化

1. リポジトリの `Actions` タブに移動
2. ワークフローを有効化

これで完了です！🎉

## 実行スケジュール

- **毎日 9時**（日本時間）
- **毎日 12時**（日本時間）
- **毎日 18時**（日本時間）

## 手動実行

`Actions` タブ → `X AI Auto Post` → `Run workflow` で手動実行も可能です。

## ツイート例

> こんにちは、くーたん博士だよ😊✨2025年10月は大規模マルチモーダルAIがすごい進化してるんだ！テキスト・画像・音声をリアルタイムで作り出せるなんて、わくわくだね🚀GPT-5 Turboは対話も推論もパワーアップ！企業向けカスタマイズも拡充中で、AIの未来がもっと広がりそう💡でもプライバシーや倫理も大事にしようね🌟みんなも一緒にAIの可能性を楽しもう！#生成AI #ChatGPT

## カスタマイズ

### 投稿頻度の変更

`.github/workflows/auto-post.yml` のcron式を編集してください。

```yaml
schedule:
  - cron: '0 0 * * *'  # 毎日9時（JST）
  - cron: '0 3 * * *'  # 毎日12時（JST）
  - cron: '0 9 * * *'  # 毎日18時（JST）
```

### 口調のカスタマイズ

`x_ai_smart_post.py` のプロンプト部分を編集してください。

## トラブルシューティング

### ワークフローが実行されない

- GitHub Actionsが有効化されているか確認
- Secretsが正しく設定されているか確認
- リポジトリがpublicまたはGitHub Pro/Teamプランか確認

### 投稿が失敗する

- X API権限が "Read and Write" になっているか確認
- Access Tokenが権限変更後に再生成されたものか確認
- ログを確認: `Actions` → 該当のワークフロー → `Upload logs`

## ライセンス

MIT License

## 作者

くーたん博士 🤖✨

---

**楽しいAIライフを！💡🚀**


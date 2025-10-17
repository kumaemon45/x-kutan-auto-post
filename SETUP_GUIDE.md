# GitHub Actionsセットアップガイド

このガイドに従って、X自動投稿システムをGitHub Actionsで設定してください。

## ステップ1: GitHubリポジトリの作成

### 1-1. GitHubにログイン

[GitHub](https://github.com/)にログインしてください。

### 1-2. 新しいリポジトリを作成

1. 右上の `+` → `New repository` をクリック
2. リポジトリ名: `x-ai-auto-post`（任意）
3. 公開設定: **Public**（Freeプランの場合、GitHub Actionsを使うにはPublicが必要）
4. `Create repository` をクリック

### 1-3. ローカルリポジトリをプッシュ

作成したリポジトリのURLをコピーして、以下のコマンドを実行：

```bash
cd /home/ubuntu/x-ai-auto-post
git remote add origin https://github.com/あなたのユーザー名/x-ai-auto-post.git
git branch -M main
git push -u origin main
```

## ステップ2: X API認証情報の取得と設定

### 2-1. X Developer Portalにアクセス

[X Developer Portal](https://developer.twitter.com/en/portal/dashboard)にアクセスしてログインします。

### 2-2. アプリの作成（まだの場合）

1. `Projects & Apps` → `+ Create App` をクリック
2. アプリ名を入力（例: `AI Auto Post Bot`）
3. アプリを作成

### 2-3. アプリ権限の設定

⚠️ **重要**: これが最も重要なステップです！

1. 作成したアプリをクリック
2. `Settings` タブに移動
3. `User authentication settings` → `Set up` をクリック
4. **App permissions** を **"Read and Write"** に変更
5. `Save` をクリック

### 2-4. API KeysとTokensの取得

1. `Keys and tokens` タブに移動
2. 以下をコピーして保存：
   - **API Key** (Consumer Key)
   - **API Secret** (Consumer Secret)
3. `Access Token and Secret` セクションで `Generate` をクリック
4. 以下をコピーして保存：
   - **Access Token**
   - **Access Token Secret**

⚠️ **注意**: 権限を変更した後は、必ずAccess Tokenを**再生成**してください！

### 2-5. OpenAI API Keyの取得

1. [OpenAI Platform](https://platform.openai.com/api-keys)にアクセス
2. `+ Create new secret key` をクリック
3. API Keyをコピーして保存

## ステップ3: GitHub Secretsの設定

### 3-1. リポジトリのSettings

1. GitHubのリポジトリページに移動
2. `Settings` タブをクリック

### 3-2. Secretsの追加

1. 左メニューから `Secrets and variables` → `Actions` をクリック
2. `New repository secret` をクリック
3. 以下の5つのSecretを追加：

#### Secret 1: X_API_KEY
- Name: `X_API_KEY`
- Secret: X Developer PortalのAPI Key（Consumer Key）を貼り付け
- `Add secret` をクリック

#### Secret 2: X_API_SECRET
- Name: `X_API_SECRET`
- Secret: X Developer PortalのAPI Secret（Consumer Secret）を貼り付け
- `Add secret` をクリック

#### Secret 3: X_ACCESS_TOKEN
- Name: `X_ACCESS_TOKEN`
- Secret: X Developer PortalのAccess Tokenを貼り付け
- `Add secret` をクリック

#### Secret 4: X_ACCESS_TOKEN_SECRET
- Name: `X_ACCESS_TOKEN_SECRET`
- Secret: X Developer PortalのAccess Token Secretを貼り付け
- `Add secret` をクリック

#### Secret 5: OPENAI_API_KEY
- Name: `OPENAI_API_KEY`
- Secret: OpenAIのAPI Keyを貼り付け
- `Add secret` をクリック

## ステップ4: GitHub Actionsの有効化

### 4-1. Actionsタブに移動

1. リポジトリの `Actions` タブをクリック
2. 「I understand my workflows, go ahead and enable them」をクリック

### 4-2. 手動テスト実行

1. `X AI Auto Post` ワークフローをクリック
2. `Run workflow` → `Run workflow` をクリック
3. 実行が完了するまで待つ（約1分）

### 4-3. 結果確認

1. 実行が完了したら、ワークフローをクリック
2. `post-tweet` ジョブをクリック
3. ログを確認して、投稿が成功したか確認

✅ **成功した場合**: Xアカウントに投稿が表示されます！

❌ **失敗した場合**: ログのエラーメッセージを確認してください。

## ステップ5: 自動実行の確認

設定が完了すると、以下のスケジュールで自動実行されます：

- **毎日 9時**（日本時間）
- **毎日 12時**（日本時間）
- **毎日 18時**（日本時間）

## トラブルシューティング

### エラー: 403 Forbidden

**原因**: X APIの権限が不足しています。

**解決方法**:
1. X Developer Portalでアプリ権限を "Read and Write" に変更
2. Access TokenとAccess Token Secretを**再生成**
3. GitHub Secretsを新しい値に更新

### エラー: Authentication failed

**原因**: GitHub Secretsが正しく設定されていません。

**解決方法**:
1. GitHub Secretsの名前が正確か確認（大文字小文字を含む）
2. 値に余分なスペースや改行が含まれていないか確認
3. すべてのSecretが設定されているか確認

### ワークフローが実行されない

**原因**: リポジトリがPrivateで、Freeプランを使用しています。

**解決方法**:
- リポジトリをPublicに変更
- または GitHub Pro/Teamプランにアップグレード

## 完了！🎉

これで、くーたん博士が自動的に生成AI情報をツイートしてくれます！

何か問題があれば、`Actions` タブのログを確認してください。

---

**楽しいAIライフを！🤖✨💡**


# Math Problem Management System

中高生向けの数学学習を支援する Django アプリケーション。単なる問題管理に留まらず、問題ごとに「解法の指針」「別解の検討」「注意点」をユーザー自身が言語化・入力することで、質の高いセルフ・アウトプットと深い理解を促します。

## 📋 概要

- ユーザー認証機能（ログイン・サインアップ）
- 学年・科目・タグ別の問題管理
- 画像付き問題登録機能
- 問題の検索・フィルタリング
- セキュアなログイン管理（ブルートフォース攻撃対策）
- 開発者（私）への質問機能

## 🛠 技術スタック

- **Framework**: Django 6.0.1
- **Database**: SQLite（開発環境）/ PostgreSQL（本番環境）
- **Authentication**: django-axes（ブルートフォース攻撃対策）
- **Server**: Gunicorn
- **Frontend**: HTML, CSS, JavaScript
- **Image Handling**: Pillow
- **Email**: SMTPメール送信機能

## 📦 必要な環境

- Python 3.13.3
- pip（Python パッケージ管理）

## 🚀 インストール方法

1. **リポジトリをクローン**
   ```bash
   git clone https://github.com/your-username/MathHint-Collector.git
   cd MathHint-Collector
   ```

2. **仮想環境を構築**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```

3. **依存パッケージをインストール**
   ```bash
   pip install -r requirements.txt
   ```

4. **環境変数を設定**
   
   `.env` ファイルを作成し、以下を記入：
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **マイグレーション実行**
   ```bash
   python manage.py migrate
   ```

6. **初期データ投入**
   ```bash
   python manage.py seed_taxonomy
   ```

7. **開発サーバー起動**
   ```bash
   python manage.py runserver
   ```

8. **ブラウザでアクセス**
   ```
   http://127.0.0.1:8000/
   ```

## 📁 プロジェクト構造

```
MathHint-Collector/
├── math_app/                 # メイン Django アプリケーション
│   ├── models.py            # データベースモデル（Grade, Tag, Problem, Question など）
│   ├── views.py             # ビュー処理
│   ├── forms.py             # フォーム定義
│   ├── urls.py              # URL ルーティング
│   ├── admin.py             # Django 管理画面設定
│   ├── management/
│   │   └── commands/
│   │       └── seed_taxonomy.py  # 初期データ投入コマンド
│   ├── templates/           # HTML テンプレート
│   │   └── math_app/
│   │       ├── index.html
│   │       ├── problem_list.html
│   │       ├── problem_detail.html
│   │       ├── problem_form.html
│   │       ├── auth_login.html
│   │       ├── auth_signup.html
│   │       ├── question_form.html
│   │       ├── question_success.html
│   │       └── lockout.html
│   ├── static/              # CSS, JavaScript
│   │   └── math_app/
│   │       └── css/
│   ├── migrations/          # データベースマイグレーション
│   └── __pycache__/
├── math_project/            # Django プロジェクト設定
│   ├── settings.py          # プロジェクト設定
│   ├── urls.py              # メインルーティング
│   ├── security_settings.py # セキュリティ設定（参考用）
│   ├── wsgi.py              # WSGI サーバー設定
│   ├── asgi.py              # ASGI サーバー設定
│   └── __pycache__/
├── fixtures/                # サンプルデータ
│   └── math_seed.json
├── .gitignore               # Git 除外設定
├── requirements.txt         # 依存パッケージ
├── manage.py                # Django 管理コマンド
├── db.sqlite3               # SQLite データベース（開発環境）
└── README.md                # このファイル
```

## 💾 主なモデル
（数I・A・II・B・III・C）
- **Tag**: 学習単元タグ（二次関数、確率など）
- **Problem**: 数学問題（画像、ヒント3種付き）
- **UserProfile**: ユーザー情報拡張
- **Question**: 開発者への質問
- **Problem**: 数学問題（画像、解説付き）
- **UserProfile**: ユーザー情報拡張

## 🔧 よく使うコマンド

```bash
# 初期データ投入
python manage.py seed_taxonomy

# マイグレーションの実行
python manage.py migrate

# マイグレーションファイルの作成
python manage.py makemigrations

# 本番環境でのサーバー起動
gunicorn math_project.wsgi --bind 0.0.0.0:8000
```

## 🔐 セキュリティ機能

- **ブルートフォース攻撃対策**: django-axes で連続ログイン試行を制限
- **CSRF 保護**: Django 標準の CSRF トークン保護
- **SQL インジェクション対策**: Django ORM による安全なクエリ
- **セキュリティヘッダー**: security_settings.py で設定管理

## 📝 主な機能

### 認証・ユーザー管理
- ユーザー登録（サインアップ）
- ブルートフォース攻撃対策（5回失敗で30分ロック）
- パスワードバリデーション（最低8文字）

### 問題管理
- 問題の新規作成・編集・削除
- 画像アップロード対応（問題画像）
- **3種類のヒント**
  - 📍 **指針**：解法の方針（テキスト + 画像）
  - 🔍 **検討**：別解や理解を深める視点（テキスト + 画像）
  - ⚠️ **注意点**：ミスしやすいポイント（テキスト + 画像）
- 手書き入力対応（キャンバス機能）
- タグ・科目・学年でのカテゴリ分け

### 検索・フィルタリング
- 学年による絞り込み
- 科目による絞り込み127.0.0.1:8000/`
- **ログイン**: `http://127.0.0.1:8000/login/`
- **サインアップ**: `http://127.0.0.1:8000/signup/`
- **問題一覧**: `http://127.0.0.1:8000/problems/`
- **質問フォーム**: `http://127.0.0.1:8000/question/`
- **管理画面**: `http://127.0.0.1
- 開発者への直接質問フォーム
- メール通知機能
- 画像添付可能込み
- タグによる検索

## 🌐 アクセス URL

- **ホームページ**: `http://localhost:8000/`
- **ログイン**: `http://localhost:8000/login/`
- **サインアップ**: `http://localhost:8000/signup/`
- **問題一覧**: `http://localhost:8000/problems/`
- **管理画面**: `http://localhost:8000/admin/`

## 📊 依存パッケージ

詳細は マイグレーションエラー
```bash
python manage.py makemigrations
python manage.py migrate
```

### 学年・科目データがない
```bash
python manage.py seed_taxonomy
```

### ログインがロックされた
```bash
python manage.py axes_reset
```

### 静的ファイルが見つからない
```bash
python manage.py collectstatic
```

## 🔮 今後の追加予定機能

- 復習日管理・間隔反復学習
- 難易度・理解度の記録
- 学習統計グラフ
- お気に入り/重要問題マーク
- ダークモード

## 📝 ライセンス

このプロジェクトはオープンソースです。ご自由にお使いください。

## 👤 作成者

**haya10-535** - [GitHub](https://github.com/haya10-535)

## 📞 サポート

問題が発生した場合や、質問がある場合は：
- GitHub の Issue を作成
- アプリ内の質問フォームから直接質問

**返信用メール**: ksw2570215@stu.o-hara.ac.jp

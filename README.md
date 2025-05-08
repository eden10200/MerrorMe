# Mirror Me - AI駆動自己PR生成サービス

Mirror Meは、就職活動中の学生や転職希望者のための、AIを活用した自己PR生成・管理サービスです。ユーザーの性格特性から効果的な自己PRを自動生成し、保存・管理することができます。

## 🌟 機能

- 🤖 AI駆動の自己PR生成
- 📝 複数パターンのPR生成（1回で3つのバリエーション）
- 💼 業界別PRの生成対応
- 📂 生成したPRの保存・管理
- ✏️ 保存したPRの編集・更新
- 🔒 ユーザー認証システム

## 🛠️ 技術スタック

- **バックエンド**: Python (Flask)
- **フロントエンド**: HTML, CSS, JavaScript
- **データベース**: MySQL
- **AI**: OpenAI API (GPT-3.5)
- **認証**: Flask-Login
- **ORM**: SQLAlchemy
- **その他**: Flask-SQLAlchemy, python-dotenv

## 📋 必要条件

- Python 3.8以上
- MySQL 8.0以上
- OpenAI APIキー

## 🚀 セットアップ手順

1. リポジトリをクローン：
```bash
git clone https://github.com/yourusername/mirror-me.git
cd mirror-me
```

2. 仮想環境を作成し有効化：
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. 依存パッケージをインストール：
```bash
pip install -r requirements.txt
```

4. 環境変数の設定：
`.env`ファイルを作成し、以下の内容を設定してください：
```
SECRET_KEY=your_secret_key_here
DATABASE_URL=mysql+pymysql://username:password@localhost/mirror_me
OPENAI_API_KEY=your_openai_api_key_here
```

5. データベースの作成：
```sql
CREATE DATABASE mirror_me;
```

6. アプリケーションの起動：
```bash
python app.py
```

アプリケーションは http://localhost:5000 で起動します。

## 💫 使用方法

1. アカウントを作成またはログイン
2. 「自己PR生成」フォームで性格特性を入力
3. 必要に応じて希望業界を指定
4. 「PRを生成」をクリック
5. 生成されたPRから好きなものを選んで保存
6. 保存したPRは「マイPR」で管理可能

## ⚙️ 環境設定

アプリケーションの動作をカスタマイズするには、`.env`ファイルで以下の設定が可能です：

- `SECRET_KEY`: アプリケーションの秘密鍵
- `DATABASE_URL`: データベース接続URL
- `OPENAI_API_KEY`: OpenAI APIキー

## 🔧 開発環境での実行

デバッグモードでの実行:
```bash
python app.py
```

## 👥 コントリビューション

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルをご覧ください。

## 👤 作者

- 学籍番号: XXXXXXXX
- 氏名: XXXX
- 所属: ○○大学

## 🙏 謝辞

- Flask開発チーム
- OpenAIチーム
- その他、このプロジェクトに貢献してくださった全ての方々
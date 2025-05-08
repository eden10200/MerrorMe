from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from openai import OpenAI
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@localhost/mirror_me')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# OpenAIクライアントの初期化
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# データベースモデル
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    prs = db.relationship('PR', backref='user', lazy=True)

class PR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    traits = db.Column(db.Text, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def generate_pr(traits, industry=None):
    # OpenAI APIを使用して自己PR文を生成
    prompt = f"以下の性格特性に基づいて、就職活動用の自己PR文を3つ生成してください。それぞれ違う角度から書いてください：\n{traits}"
    if industry:
        prompt += f"\n業界：{industry}"
    
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=500,
            n=3,
            stop=None,
            temperature=0.7
        )
        return [choice.text.strip() for choice in response.choices]
    except Exception as e:
        print(f"Error generating PR: {e}")
        error_message = str(e)
        if "insufficient_quota" in error_message:
            return ["申し訳ありませんが、現在システムが混み合っています。しばらく時間をおいてから再度お試しください。"]
        elif "rate_limit_exceeded" in error_message:
            return ["リクエストが集中しています。少し時間をおいてから再度お試しください。"]
        else:
            return ["エラーが発生しました。もう一度お試しください。エラーが続く場合は管理者にお問い合わせください。"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
@login_required
def generate():
    traits = request.form.get('traits')
    industry = request.form.get('industry')
    
    if not traits:
        flash('性格特性を入力してください。')
        return redirect(url_for('index'))
    
    generated_prs = generate_pr(traits, industry)
    return render_template('results.html', prs=generated_prs, traits=traits)

@app.route('/save_pr', methods=['POST'])
@login_required
def save_pr():
    content = request.form.get('content')
    title = request.form.get('title')
    traits = request.form.get('traits')
    
    if not all([content, title, traits]):
        flash('必要な情報が不足しています。')
        return redirect(url_for('index'))
    
    pr = PR(content=content, title=title, traits=traits, user_id=current_user.id)
    db.session.add(pr)
    db.session.commit()
    
    flash('PRが保存されました。')
    return redirect(url_for('my_prs'))

@app.route('/my_prs')
@login_required
def my_prs():
    prs = PR.query.filter_by(user_id=current_user.id).order_by(PR.created_at.desc()).all()
    return render_template('my_prs.html', prs=prs)

@app.route('/delete_pr/<int:pr_id>', methods=['POST'])
@login_required
def delete_pr(pr_id):
    pr = PR.query.get_or_404(pr_id)
    if pr.user_id != current_user.id:
        flash('権限がありません。')
        return redirect(url_for('my_prs'))
    
    db.session.delete(pr)
    db.session.commit()
    flash('PRが削除されました。')
    return redirect(url_for('my_prs'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('このユーザー名は既に使用されています。')
            return redirect(url_for('register'))
        
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        
        flash('登録が完了しました。ログインしてください。')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        
        flash('ユーザー名またはパスワードが正しくありません。')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/edit_pr/<int:pr_id>', methods=['POST'])
@login_required
def edit_pr(pr_id):
    pr = PR.query.get_or_404(pr_id)
    if pr.user_id != current_user.id:
        flash('権限がありません。')
        return redirect(url_for('my_prs'))
    
    pr.title = request.form.get('title')
    pr.content = request.form.get('content')
    pr.traits = request.form.get('traits')
    db.session.commit()
    
    flash('PRが更新されました。')
    return redirect(url_for('my_prs'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
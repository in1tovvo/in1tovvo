# 认证模块
from functools import wraps
from flask import session, redirect, url_for, request, flash, render_template
import sqlite3
import os
from werkzeug.security import check_password_hash, generate_password_hash

def get_db_connection():
    """获取数据库连接（与app.py一致）"""
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgresql://'):
        try:
            import psycopg2
            import psycopg2.extras
            conn = psycopg2.connect(database_url)
            conn.cursor_factory = psycopg2.extras.RealDictCursor
            return conn
        except ImportError:
            raise RuntimeError("PostgreSQL support requires psycopg2-binary")
    else:
        # SQLite
        db_path = 'data/wedding.db'
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

def init_auth():
    """初始化用户认证系统，创建users表并添加默认管理员"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 根据数据库类型写兼容SQL
    db_url = os.environ.get('DATABASE_URL', '')
    is_postgres = db_url.startswith('postgresql://')
    
    if is_postgres:
        # PostgreSQL语法
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    else:
        # SQLite语法
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    # 检查是否已有用户（统一使用别名）
    cursor.execute('SELECT COUNT(*) as cnt FROM users')
    row = cursor.fetchone()
    count = row['cnt']
    
    if count == 0:
        default_pw = 'admin123'
        hashed = generate_password_hash(default_pw, method='pbkdf2:sha256', salt_length=16)
        if is_postgres:
            cursor.execute(
                'INSERT INTO users (username, password) VALUES (%s, %s)',
                ('admin', hashed)
            )
        else:
            cursor.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                ('admin', hashed)
            )
        print('⚠️  默认账户创建：admin / admin123（请首次登录后修改密码）')
    
    conn.commit()
    conn.close()

def login_required(view_func):
    """装饰器：要求登录"""
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login_route', next=request.endpoint))
        return view_func(*args, **kwargs)
    return wrapped_view

def login_view():
    """处理登录请求"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s' if os.environ.get('DATABASE_URL','').startswith('postgresql://') else 'SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            next_page = request.args.get('next')
            flash(f'欢迎回来，{user["username"]}！', 'success')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('用户名或密码错误', 'danger')
    return render_template('login.html')

def logout_view():
    """处理退出登录"""
    session.clear()
    flash('已退出登录', 'info')
    return redirect(url_for('login_route'))

def change_password_view():
    """修改密码"""
    if request.method == 'POST':
        old_pw = request.form.get('old_password')
        new_pw = request.form.get('new_password')
        confirm_pw = request.form.get('confirm_password')
        
        if not old_pw or not new_pw or not confirm_pw:
            flash('请填写所有密码字段', 'danger')
            return render_template('change_password.html')
        
        if new_pw != confirm_pw:
            flash('两次输入的新密码不一致', 'danger')
            return render_template('change_password.html')
        
        if len(new_pw) < 6:
            flash('新密码长度至少6位', 'danger')
            return render_template('change_password.html')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE id = %s' if os.environ.get('DATABASE_URL','').startswith('postgresql://') 
            else 'SELECT * FROM users WHERE id = ?', 
            (session['user_id'],)
        )
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], old_pw):
            hashed = generate_password_hash(new_pw, method='pbkdf2:sha256', salt_length=16)
            cursor.execute(
                'UPDATE users SET password = %s WHERE id = %s' if os.environ.get('DATABASE_URL','').startswith('postgresql://')
                else 'UPDATE users SET password = ? WHERE id = ?',
                (hashed, session['user_id'])
            )
            conn.commit()
            conn.close()
            flash('密码修改成功', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('原密码错误', 'danger')
    return render_template('change_password.html')

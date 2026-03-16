# 备婚大作战 - 功能增强与部署方案

## 任务一：添加登录验证功能

### 方案A：简单会话保护（推荐 - 5分钟改动）
**优点**：改动最小，无需复杂数据库，适合个人使用

```python
# 在 app.py 开头添加：
from flask import session
import uuid

# 在现有数据库中添加 users 表：
# CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT);

# 新增路由：
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        # TODO: 验证密码
        session['user_id'] = username
        flash('登录成功！', 'success')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# 保护所有路由（在现有路由定义前添加）：
@app.before_request
def require_login():
    # 排除登录、静态文件等公开路由
    public_routes = ['login', 'static', 'logout']
    if request.endpoint not in public_routes and 'user_id' not in session:
        return redirect(url_for('login'))
```

**工作流程**：
1. 首次运行初始化admin账户
2. 访问任何页面自动跳转登录页
3. 简单密码存储在数据库（生产环境需哈希）

---

### 方案B：Flask-Login扩展（更规范）
**优点**：标准做法，功能完善（记住我、权限管理等）

```bash
cd wedding-planner && ./venv/bin/pip install flask-login
```

改动较大但更专业，需要：
- 用户模型类
- 登录管理器初始化
- 密码哈希（werkzeug.security）
- 装饰器保护视图

建议采用方案A快速上线，后续如需多用户再升级。

---

### 实施方案A - 详细步骤

**步骤1：创建数据库迁移文件 `add_auth.py`**

```python
import sqlite3

conn = sqlite3.connect('data/wedding.db')
cursor = conn.cursor()

# 添加用户表
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 添加默认管理员（密码：admin123，首次登录后请修改）
cursor.execute('''
INSERT OR IGNORE INTO users (username, password)
VALUES ('admin', 'pbkdf2:sha256:260000$...')  -- 实际使用生成哈希
''')

conn.commit()
conn.close()
print('✅ 用户表创建完成，默认账户：admin / admin123')
```

**步骤2：创建认证模块 `auth.py`**

```python
from flask import session, redirect, url_for, request, flash, render_template
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import os

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_auth():
    """初始化认证系统"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # 检查是否已有用户，没有则创建默认admin
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        # 使用简单哈希（生产环境建议更强）
        default_pw = 'admin123'
        hashed = generate_password_hash(default_pw, method='pbkdf2:sha256', salt_length=16)
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', hashed))
        print('⚠️  默认账户创建：admin / admin123（请首次登录后修改密码）')
    conn.commit()
    conn.close()

def login_required(view_func):
    """装饰器：要求登录"""
    from functools import wraps
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login', next=request.endpoint))
        return view_func(*args, **kwargs)
    return wrapped_view

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            next_page = request.args.get('next')
            flash(f'欢迎回来，{user["username"]}！', 'success')
            return redirect(next_page or url_for('index'))
        else:
            flash('用户名或密码错误', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('已退出登录', 'info')
    return redirect(url_for('login'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_pw = request.form.get('old_password')
        new_pw = request.form.get('new_password')
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        if check_password_hash(user['password'], old_pw):
            hashed = generate_password_hash(new_pw, method='pbkdf2:sha256', salt_length=16)
            conn.execute('UPDATE users SET password = ? WHERE id = ?', (hashed, session['user_id']))
            conn.commit()
            conn.close()
            flash('密码修改成功', 'success')
            return redirect(url_for('index'))
        else:
            flash('原密码错误', 'danger')
    return render_template('change_password.html')
```

**步骤3：创建登录页面模板 `templates/login.html`**

```html
{% extends "base.html" %}
{% block title %}登录 - 备婚大作战{% endblock %}
{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-4">
            <div class="card shadow-sm">
                <div class="card-body">
                    <h3 class="text-center mb-4">🔐 登录</h3>
                    {% with messages = get_flashed_messages(with_categories=true) %}
                        {% if messages %}
                            {% for category, message in messages %}
                                <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                                    {{ message }}
                                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                </div>
                            {% endfor %}
                        {% endif %}
                    {% endwith %}
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label">用户名</label>
                            <input type="text" name="username" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">密码</label>
                            <input type="password" name="password" class="form-control" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">登录</button>
                    </form>
                    <div class="mt-3 text-center">
                        <a href="{{ url_for('index') }}" class="text-muted">← 返回首页</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**步骤4：修改 `app.py` 主文件**
- 导入 `init_auth`，在 `if __name__ == '__main__':` 前调用 `init_auth()`
- 在 `@app.before_request` 中调用 `login_required` 保护视图
- 或直接在需要保护的路由上加 `@login_required` 装饰器

**步骤5：修改 `templates/base.html` 添加用户信息**
在导航栏添加：
```html
{% if session.username %}
    <span class="navbar-text me-3">欢迎，{{ session.username }}</span>
    <a href="{{ url_for('logout') }}" class="btn btn-sm btn-outline-secondary">退出</a>
    <a href="{{ url_for('change_password') }}" class="btn btn-sm btn-outline-primary">修改密码</a>
{% endif %}
```

---

## 任务二：国内免费部署方案

### 方案对比

| 平台 | 免费额度 | Flask支持 | 数据库 | 访问速度 | 限制 | 推荐度 |
|------|----------|-----------|--------|----------|------|--------|
| **Vercel** | 100GB/月 | ✅ 需无状态（SQLite需改用外部DB） | ❌ 需外部DB | 国内外都行 | Serverless架构，需适配 | ⭐⭐⭐ |
| **Render** | 750小时/月 | ✅ 支持持久进程 | ✅ 支持PostgreSQL免费 | 国外稍慢 | 15分钟无使用休眠 | ⭐⭐⭐⭐ |
| ** Railway** | $5免费额度 | ✅ 支持 | ✅ 支持PostgreSQL免费 | 国外稍慢 | 需信用卡验证 | ⭐⭐⭐ |
| ** PythonAnywhere** | 500MB | ✅ 支持 | ✅ 内置MySQL免费 | 国外慢 | 仅Python，无Node | ⭐⭐ |
| **Heroku** | ❌ 已取消 | - | - | - | 无免费层 | ⭐ |
| **千码云/阿里云/腾讯云** | ⚠️ 需学生认证 | ✅ | ✅ | 国内快 | 有免费额度但限制多 | ⭐⭐⭐⭐⭐ (学生) |

### 推荐方案：Render (简单直接)

**理由**：
1. ✅ 完全免费（PostgreSQL 90天自动续期，实际长期可用）
2. ✅ 原生支持Flask + 持久进程（非Serverless）
3. ✅ 使用SQLite文件或PostgreSQL均可
4. ✅ 自动HTTPS + 自定义域名（*.onrender.com）
5. ✅ 部署简单（GitHub仓库直连）

**部署步骤**：

**步骤1：准备部署配置文件**

创建 `render.yaml`：
```yaml
services:
  - type: web
    name: wedding-planner
    env: python
    buildCommand: |
      pip install -r requirements.txt
      python -c "from app import init_auth; init_auth()"
    startCommand: python app.py
    plan: free
    autoDeploy: true
```

创建 `requirements.txt`：
```
Flask==2.3.3
Werkzeug==2.3.7
```

**步骤2：修改app.py适配Render**
```python
import os
app.config['DATABASE'] = os.path.join(BASE_DIR, 'data', 'wedding.db')
# Render环境下使用临时目录
if os.environ.get('RENDER'):
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
    os.makedirs('/tmp/uploads', exist_ok=True)
```

**步骤3：Git推送至GitHub，Render自动部署**
1. 创建GitHub仓库
2. 推送代码
3. Render添加Web Service，选择仓库
4. 自动部署完成，获得 `wedding-planner.onrender.com`

**步骤4：后续访问**
- 使用提供的onrender域名
- 国内DNS解析正常（无需翻墙）

---

### 备选方案：Vercel + 外部数据库（适合技术用户）

**架构调整**：
- Flask应用改为无状态（session存Redis）
- SQLite替换为PostgreSQL/MySQL（数据库需单独部署）
- 文件上传改为OSS/CDN

**复杂度**：高，不推荐快速上线

---

## 最优组合方案（总览）

**阶段一（本周末完成）**：
1. ✅ 添加登录验证（方案A，1-2小时）
2. ✅ 修复所有已知bug（已完成）
3. ✅ 生成requirements.txt
4. ✅ 添加render.yaml和Procfile备用

**阶段二（下周部署）**：
1. 代码推送到GitHub
2. Render创建Web Service
3. 测试线上功能，确认数据库正常
4. 绑定自定义域名（可选，需备案）

**阶段三（长期优化）**：
1. 如有需要，升级到Flask-Login（方案B）
2. 添加用户权限管理（查看/编辑）
3. 考虑数据导入导出优化

---

## 风险评估与对策

| 风险 | 影响 | 对策 |
|------|------|------|
| Render免费版休眠 | 首次访问慢（30秒冷启动） | 使用UptimeRobot定时访问保持活跃（免费） |
| 数据库持久化 | Render重启会清空 /tmp 目录 | 使用PostgreSQL而非文件存储，或定期备份恢复 |
| 上传文件丢失 | Render磁盘临时 | 改为云存储或限制小文件（<1MB） |
| 国内访问速度 | Render全球CDN，国内还可以 | 如遇问题，考虑国内云厂商学生免费套餐 |

---

## 结论：立即行动清单

**优先级1（今天做）**：
- [ ] 添加登录验证代码（auth.py + 修改app.py）
- [ ] 创建登录页面模板（login.html + change_password.html）
- [ ] 更新base.html导航栏显示用户

**优先级2（部署前）**：
- [ ] 生成requirements.txt
- [ ] 创建render.yaml
- [ ] 推送代码到GitHub私有仓库
- [ ] 创建Render Web Service

**优先级3（部署后）**：
- [ ] 测试所有功能（登录、CRUD、上传）
- [ ] 设置环境变量（SECRET_KEY等）
- [ ] 配置自定义域名（可选）

---

## 时间预估

- 登录功能开发：1-2小时
- 测试与修复：30分钟
- Render部署：20分钟
- 总计：约2-3小时即可上线

---

**需要我现在开始实施方案A的代码吗？还是你有其他想法？**
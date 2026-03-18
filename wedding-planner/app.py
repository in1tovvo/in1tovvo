#!/usr/bin/env python3
"""
备婚大作战 - V2 修复版（添加登录验证）
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta, date
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, g, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from auth import init_auth, login_required, login_view, logout_view, change_password_view

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'wedding-planner-secret-change-in-production')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库配置：优先使用环境变量（Vercel Neon），否则本地SQLite
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    app.config['DATABASE_TYPE'] = 'postgresql'
    app.config['DATABASE_URL'] = DATABASE_URL
else:
    app.config['DATABASE_TYPE'] = 'sqlite'
    app.config['DATABASE'] = os.path.join(BASE_DIR, 'data', 'wedding.db')

# Vercel环境：使用/tmp作为上传目录（只读文件系统）
if os.environ.get('VERCEL'):
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
else:
    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'images')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def get_db():
    """获取数据库连接（支持SQLite和PostgreSQL）"""
    if 'db' not in g:
        if app.config['DATABASE_TYPE'] == 'postgresql':
            import psycopg2
            from psycopg2.extras import RealDictCursor
            conn = psycopg2.connect(app.config['DATABASE_URL'])
            conn.cursor_factory = RealDictCursor
            g.db = DBAdapter(conn, 'postgresql')
        else:
            conn = sqlite3.connect(app.config['DATABASE'])
            conn.row_factory = sqlite3.Row
            g.db = DBAdapter(conn, 'sqlite')
    return g.db

class DBAdapter:
    """数据库适配器，统一SQLite和PostgreSQL的接口"""
    def __init__(self, conn, db_type):
        self.conn = conn
        self.db_type = db_type
        self.cursor = None
    
    def execute(self, sql, params=None):
        """执行SQL，自动转换占位符"""
        if self.db_type == 'postgresql':
            sql = sql.replace('?', '%s')
        self.cursor = self.conn.cursor()
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        return self.cursor
    
    def commit(self):
        """提交事务"""
        self.conn.commit()
    
    def rollback(self):
        """回滚事务"""
        self.conn.rollback()
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """初始化数据库表（支持SQLite和PostgreSQL）"""
    if app.config['DATABASE_TYPE'] == 'postgresql':
        # PostgreSQL 使用 get_db().conn 获取原始连接
        db_adapter = get_db()
        conn = db_adapter.conn
        cursor = conn.cursor()
    else:
        db_path = os.path.dirname(app.config['DATABASE'])
        os.makedirs(db_path, exist_ok=True)
        conn = sqlite3.connect(app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
    
    # 表结构定义（使用通用语法，两种数据库都兼容）
    # PostgreSQL 和 SQLite 都支持 SERIAL/INTEGER PRIMARY KEY AUTOINCREMENT
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id SERIAL PRIMARY KEY,
            key TEXT UNIQUE NOT NULL,
            value TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            due_date DATE,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guests (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT,
            relationship TEXT NOT NULL,
            side TEXT NOT NULL,
            status TEXT NOT NULL,
            table_number INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget (
            id SERIAL PRIMARY KEY,
            category TEXT NOT NULL,
            item TEXT NOT NULL,
            estimated REAL,
            actual REAL,
            paid REAL DEFAULT 0,
            vendor TEXT,
            notes TEXT,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendors (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            price_range TEXT,
            rating REAL,
            notes TEXT,
            contract_date DATE,
            contract_file TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS moodboard (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            image_path TEXT NOT NULL,
            category TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tables (
            id SERIAL PRIMARY KEY,
            table_number INTEGER UNIQUE NOT NULL,
            table_name TEXT NOT NULL,
            shape TEXT DEFAULT 'round',
            capacity INTEGER DEFAULT 10
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guest_tables (
            id SERIAL PRIMARY KEY,
            guest_id INTEGER REFERENCES guests(id) ON DELETE CASCADE,
            table_id INTEGER REFERENCES tables(id) ON DELETE CASCADE,
            seat_number INTEGER,
            UNIQUE(guest_id)
        )
    ''')
    
    conn.commit()
    if app.config['DATABASE_TYPE'] == 'sqlite':
        conn.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== 全局上下文 ====================

@app.context_processor
def inject_context():
    db = get_db()
    
    pending_tasks = db.execute(
        "SELECT COUNT(*) as count FROM tasks WHERE status != 'completed'"
    ).fetchone()['count'] or 0
    
    # 兼容新旧宾客表结构
    try:
        # 新结构：status字段
        unconfirmed_guests = db.execute(
            "SELECT COUNT(*) as count FROM guests WHERE status = 'no_response' OR status = ''"
        ).fetchone()['count'] or 0
    except:
        # 旧结构：invitation_status + rsvp_status
        unconfirmed_guests = db.execute(
            "SELECT COUNT(*) as count FROM guests WHERE invitation_status = 'pending' OR rsvp_status = 'no_response' OR rsvp_status = ''"
        ).fetchone()['count'] or 0
    
    wedding_date = db.execute("SELECT value FROM settings WHERE key='wedding_date'").fetchone()
    wedding_date = wedding_date['value'] if wedding_date else None
    if wedding_date:
        wedding_date = datetime.strptime(wedding_date, '%Y-%m-%d').date()
    
    today = date.today()
    
    return dict(
        pending_tasks=pending_tasks,
        unconfirmed_guests=unconfirmed_guests,
        wedding_date=wedding_date,
        today=today
    )

# ==================== 认证路由 ====================

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    return login_view()

@app.route('/logout')
def logout_route():
    return logout_view()

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password_route():
    return change_password_view()

@app.route('/settings/wedding-date', methods=['GET', 'POST'])
@login_required
def wedding_date_settings():
    """设置或修改婚礼日期"""
    db = get_db()
    
    # 获取当前设置的婚礼日期
    wedding_date_row = db.execute(
        "SELECT value FROM settings WHERE key='wedding_date'"
    ).fetchone()
    current_date = wedding_date_row['value'] if wedding_date_row else ''
    
    if request.method == 'POST':
        wedding_date_str = request.form.get('wedding_date')
        try:
            # 验证日期格式
            wedding_date = datetime.strptime(wedding_date_str, '%Y-%m-%d').date()
            
            # 保存到数据库（upsert）
            if current_date:
                db.execute(
                    "UPDATE settings SET value = ? WHERE key = 'wedding_date'",
                    (wedding_date_str,)
                )
            else:
                db.execute(
                    "INSERT INTO settings (key, value) VALUES ('wedding_date', ?)",
                    (wedding_date_str,)
                )
            db.commit()
            flash('婚礼日期已保存', 'success')
            return redirect(url_for('dashboard'))
        except ValueError:
            flash('日期格式错误，请使用 YYYY-MM-DD 格式', 'danger')
    
    # 计算剩余天数用于显示
    today = date.today()
    days_left = None
    if current_date:
        try:
            wedding_date = datetime.strptime(current_date, '%Y-%m-%d').date()
            days_left = (wedding_date - today).days
        except:
            days_left = None
    
    return render_template('wedding_date_form.html',
                          current_date=current_date,
                          today=today,
                          wedding_date=datetime.strptime(current_date, '%Y-%m-%d').date() if current_date else None,
                          days_left=days_left)

# 全局请求钩子：保护需要登录的路由
@app.before_request
def require_login():
    public_endpoints = ['login_route', 'static', 'logout_route']
    if request.endpoint not in public_endpoints and 'user_id' not in session:
        if request.endpoint:
            return redirect(url_for('login_route', next=request.endpoint))

# ==================== 测试路由 ====================
@app.route('/test-db')
def test_db():
    """测试数据库连接（临时调试用）"""
    try:
        db = get_db()
        cursor = db.execute("SELECT version() as ver")
        version = cursor.fetchone()
        if version:
            version = version[0] if isinstance(version, (list, tuple)) else version['ver']
        
        # 获取表列表
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' ORDER BY table_name
        """)
        tables = [row['table_name'] if isinstance(row, dict) else row[0] for row in cursor.fetchall()]
        
        return jsonify({
            'status': 'success',
            'database_type': app.config['DATABASE_TYPE'],
            'postgresql_version': str(version)[:60] if version else None,
            'tables': tables,
            'table_count': len(tables)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ==================== 主页 ====================

@app.route('/')
def dashboard():
    db = get_db()
    
    # 统计数据
    total_tasks = db.execute('SELECT COUNT(*) as count FROM tasks').fetchone()['count']
    completed_tasks = db.execute("SELECT COUNT(*) as count FROM tasks WHERE status = 'completed'").fetchone()['count']
    
    # 需要执行的任务（未完成且日期未过期或今天到期）
    today = date.today()
    needed_tasks = db.execute(
        "SELECT COUNT(*) as count FROM tasks WHERE status != 'completed' AND (due_date IS NULL OR due_date >= ?)",
        (today,)
    ).fetchone()['count']
    
    # 紧急任务（未来7天内到期且未完成）
    week_later = today + timedelta(days=7)
    urgent_tasks = db.execute(
        "SELECT * FROM tasks WHERE status != 'completed' AND due_date BETWEEN ? AND ? ORDER BY due_date",
        (today, week_later)
    ).fetchall()
    
    # 近期任务（接下来7天）
    upcoming = urgent_tasks
    
    return render_template('dashboard.html',
                          total_tasks=total_tasks,
                          completed_tasks=completed_tasks,
                          needed_tasks=needed_tasks,
                          urgent_tasks=urgent_tasks,
                          upcoming=upcoming)

@app.route('/tasks')
def tasks():
    db = get_db()
    
    # 任务查询（支持筛选）
    status_filter = request.args.get('status')
    phase_filter = request.args.get('phase')
    
    query = 'SELECT * FROM tasks WHERE 1=1'
    params = []
    
    if status_filter:
        query += ' AND status = ?'
        params.append(status_filter)
    
    if phase_filter:
        query += ' AND phase = ?'
        params.append(phase_filter)
    
    query += ' ORDER BY CASE WHEN due_date IS NULL THEN 1 ELSE 0 END, due_date ASC, priority DESC'
    tasks = db.execute(query, params).fetchall()
    
    # 将任务转换为字典并处理日期
    tasks_list = []
    for t in tasks:
        task_dict = dict(t)
        # 转换 due_date 字符串为 date 对象（如果存在）
        if task_dict.get('due_date'):
            try:
                task_dict['due_date_obj'] = datetime.strptime(task_dict['due_date'], '%Y-%m-%d').date()
            except:
                task_dict['due_date_obj'] = None
        else:
            task_dict['due_date_obj'] = None
        tasks_list.append(task_dict)
    
    # 统计数据
    total_tasks = len(tasks_list)
    completed_tasks = sum(1 for t in tasks_list if t['status'] == 'completed')
    needed_tasks = sum(1 for t in tasks_list if t['status'] != 'completed')
    
    # 获取所有阶段（用于筛选）
    phases = db.execute('SELECT DISTINCT phase FROM tasks WHERE phase IS NOT NULL ORDER BY phase').fetchall()
    phases = [p[0] for p in phases]
    
    # 获取今天的日期，用于比较
    today = date.today()
    
    return render_template('tasks.html',
                          tasks=tasks_list,
                          total_tasks=total_tasks,
                          completed_tasks=completed_tasks,
                          needed_tasks=needed_tasks,
                          phases=phases,
                          today=today)

@app.route('/guests')
def guests():
    db = get_db()
    guests = db.execute('SELECT * FROM guests ORDER BY name').fetchall()
    
    # 统计
    total = len(guests)
    # 兼容新旧字段
    confirmed = 0
    pending = 0
    for g in guests:
        # 转换为普通字典，方便操作
        guest_dict = dict(g)
        # 新结构：status 字段
        if 'status' in guest_dict:
            status = guest_dict['status'] or ''
            if status == 'yes' or status == 'attended':
                confirmed += 1
            elif status == 'no_response' or status == '':
                pending += 1
        else:
            # 旧结构： invitation_status 和 rsvp_status
            rsvp = guest_dict.get('rsvp_status', '')
            if rsvp == 'yes':
                confirmed += 1
            elif rsvp == 'no_response' or rsvp == '':
                pending += 1
    
    return render_template('guests.html', 
                          guests=guests,
                          stats={'total': total, 'confirmed': confirmed, 'pending': pending})

@app.route('/budget')
def budget():
    db = get_db()
    budgets = db.execute('SELECT * FROM budget ORDER BY category, item_name').fetchall()
    
    # 统计数据
    total_est = db.execute('SELECT SUM(estimated_cost) as sum FROM budget').fetchone()['sum'] or 0
    actual_spent = db.execute('SELECT SUM(actual_cost) as sum FROM budget').fetchone()['sum'] or 0
    
    return render_template('budget.html',
                          budgets=budgets,
                          total_est=total_est,
                          actual_spent=actual_spent)

@app.route('/vendors')
def vendors():
    db = get_db()
    vendors = db.execute('SELECT * FROM vendors ORDER BY name').fetchall()
    return render_template('vendors.html', vendors=vendors)

@app.route('/moodboard')
def moodboard():
    db = get_db()
    moodboards = db.execute('SELECT * FROM moodboard ORDER BY created_at DESC').fetchall()
    # 构建完整的图片URL
    base_url = request.host_url.rstrip('/')
    items = []
    for item in moodboards:
        items.append({
            'id': item['id'],
            'title': item['title'],
            'category': item['category'],
            'tags': item['tags'],
            'image_url': f"{base_url}/static/images/{item['image_path']}"
        })
    return render_template('moodboard.html', moodboards=items)

@app.route('/seating')
def seating():
    db = get_db()
    # 获取所有桌席
    tables = db.execute('SELECT * FROM tables ORDER BY table_number').fetchall()
    tables_list = [dict(t) for t in tables]
    
    # 获取所有宾客
    guests = db.execute('SELECT * FROM guests ORDER BY name').fetchall()
    guests_list = [dict(g) for g in guests]
    
    # 获取已安排的座位信息
    seating_data = db.execute('''
        SELECT gt.guest_id, gt.table_id, gt.seat_number, t.table_number, t.table_name
        FROM guest_tables gt
        JOIN tables t ON gt.table_id = t.id
    ''').fetchall()
    seating_list = [dict(s) for s in seating_data]
    
    # 构建已安排宾客ID集合
    assigned_guest_ids = set(s['guest_id'] for s in seating_list)
    assigned_guests = [g for g in guests_list if g['id'] in assigned_guest_ids]
    
    # 未安排宾客
    unassigned_guests = [g for g in guests_list if g['id'] not in assigned_guest_ids]
    
    return render_template('seating_chart.html',
                          tables=tables_list,
                          guests=guests_list,
                          assigned_guests=assigned_guests,
                          unassigned_guests=unassigned_guests,
                          seating_data=seating_list,
                          all_guests=guests_list)

# ==================== API路由（示例） ====================

@app.route('/tasks/api')
def api_tasks():
    db = get_db()
    tasks = db.execute('SELECT * FROM tasks ORDER BY due_date').fetchall()
    result = [dict(t) for t in tasks]
    return jsonify(result)

@app.route('/tasks/create', methods=['POST'])
def create_task():
    title = request.form.get('title')
    category = request.form.get('category')
    priority = request.form.get('priority', 'medium')
    due_date = request.form.get('due_date')
    status = request.form.get('status', 'pending')
    
    db = get_db()
    db.execute(
        'INSERT INTO tasks (title, category, priority, status, due_date) VALUES (?, ?, ?, ?, ?)',
        (title, category, priority, status, due_date)
    )
    db.commit()
    flash('任务创建成功', 'success')
    return redirect(url_for('tasks'))

@app.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
def edit_task(id):
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()
    if not task:
        flash('任务不存在', 'danger')
        return redirect(url_for('tasks'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        priority = request.form.get('priority')
        due_date = request.form.get('due_date')
        status = request.form.get('status')
        notes = request.form.get('notes')
        
        db.execute(
            'UPDATE tasks SET title=?, category=?, priority=?, status=?, due_date=?, notes=? WHERE id=?',
            (title, category, priority, status, due_date, notes, id)
        )
        db.commit()
        flash('任务已更新', 'success')
        return redirect(url_for('tasks'))
    
    return render_template('edit_task.html', task=task)

@app.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (id,))
    db.commit()
    flash('任务已删除', 'success')
    return redirect(url_for('tasks'))

@app.route('/tasks/<int:id>/complete', methods=['POST'])
def complete_task(id):
    db = get_db()
    db.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (id,))
    db.commit()
    flash('任务标记为已完成', 'success')
    return redirect(url_for('tasks'))

@app.route('/tasks/<int:id>/toggle-needed', methods=['POST'])
def toggle_needed(id):
    data = request.get_json()
    is_needed = data.get('is_needed', 1)
    # 这里只是一个示例，实际可能需要添加 is_needed 字段到 tasks 表
    # 目前我们使用 status != 'completed' 作为需要执行的标记
    return jsonify({'success': True})

# ==================== 宾客管理 ====================

@app.route('/guests/create', methods=['POST'])
def create_guest():
    name = request.form.get('name')
    phone = request.form.get('phone')
    relationship = request.form.get('relationship')
    side = request.form.get('side')
    status = request.form.get('status', 'no_response')
    notes = request.form.get('notes')
    
    # 将新结构的 status 映射到旧表的 invitation_status 和 rsvp_status
    invitation_status = 'pending'  # 默认未发送
    rsvp_status = 'no_response'
    
    if status == 'yes':
        invitation_status = 'sent'
        rsvp_status = 'yes'
    elif status == 'no':
        invitation_status = 'sent'
        rsvp_status = 'no'
    elif status == 'attended':
        invitation_status = 'delivered'
        rsvp_status = 'yes'
    # 'no_response' 保持默认
    
    db = get_db()
    db.execute(
        'INSERT INTO guests (name, phone, relationship, side, invitation_status, rsvp_status, notes) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (name, phone, relationship, side, invitation_status, rsvp_status, notes)
    )
    db.commit()
    flash('宾客添加成功', 'success')
    return redirect(url_for('guests'))

@app.route('/guests/<int:id>/edit', methods=['GET', 'POST'])
def edit_guest(id):
    db = get_db()
    guest = db.execute('SELECT * FROM guests WHERE id = ?', (id,)).fetchone()
    if not guest:
        flash('宾客不存在', 'danger')
        return redirect(url_for('guests'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        relationship = request.form.get('relationship')
        side = request.form.get('side')
        status = request.form.get('status')
        notes = request.form.get('notes')
        
        # 将新结构的 status 映射到旧表的 invitation_status 和 rsvp_status
        invitation_status = guest['invitation_status'] if 'invitation_status' in guest.keys() else 'pending'
        rsvp_status = guest['rsvp_status'] if 'rsvp_status' in guest.keys() else 'no_response'
        
        if status == 'yes':
            invitation_status = 'sent'
            rsvp_status = 'yes'
        elif status == 'no':
            invitation_status = 'sent'
            rsvp_status = 'no'
        elif status == 'attended':
            invitation_status = 'delivered'
            rsvp_status = 'yes'
        elif status == 'no_response':
            # 保持原值或设为默认
            pass
        
        db.execute(
            'UPDATE guests SET name=?, phone=?, relationship=?, side=?, invitation_status=?, rsvp_status=?, notes=? WHERE id=?',
            (name, phone, relationship, side, invitation_status, rsvp_status, notes, id)
        )
        db.commit()
        flash('宾客信息已更新', 'success')
        return redirect(url_for('guests'))
    
    return render_template('edit_guest.html', guest=guest)

@app.route('/guests/<int:id>/delete', methods=['POST'])
def delete_guest(id):
    db = get_db()
    db.execute('DELETE FROM guests WHERE id = ?', (id,))
    db.commit()
    flash('宾客已删除', 'success')
    return redirect(url_for('guests'))

@app.route('/guests/import', methods=['POST'])
def import_guests():
    # CSV导入逻辑
    if 'csv_file' not in request.files:
        flash('未选择文件', 'danger')
        return redirect(url_for('guests'))
    
    file = request.files['csv_file']
    if file.filename == '':
        flash('未选择文件', 'danger')
        return redirect(url_for('guests'))
    
    import csv
    import io
    
    try:
        stream = io.StringIO(file.stream.read().decode('utf-8-sig'))
        csv_reader = csv.DictReader(stream)
        db = get_db()
        
        count = 0
        for row in csv_reader:
            db.execute(
                'INSERT INTO guests (name, phone, relationship, side, status) VALUES (?, ?, ?, ?, ?)',
                (row.get('姓名', ''), row.get('电话', ''), row.get('关系', ''), 
                 row.get('阵营', ''), row.get('状态', 'no_response'))
            )
            count += 1
        db.commit()
        flash(f'成功导入 {count} 位宾客', 'success')
    except Exception as e:
        flash(f'导入失败: {str(e)}', 'danger')
    
    return redirect(url_for('guests'))

@app.route('/guests/export')
def export_guests():
    db = get_db()
    guests = db.execute('SELECT * FROM guests ORDER BY name').fetchall()
    
    import csv, io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', '姓名', '电话', '关系', '阵营', '状态', '备注'])
    for guest in guests:
        writer.writerow([
            guest['id'], guest['name'], guest['phone'], guest['relationship'],
            guest['side'], guest['status'], guest['notes']
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'guests_{date.today().strftime("%Y%m%d")}.csv'
    )

# ==================== 预算管理 ====================

@app.route('/budget/create', methods=['POST'])
def create_budget():
    category = request.form.get('category')
    item_name = request.form.get('item')
    estimated_cost = request.form.get('estimated', type=float)
    actual_cost = request.form.get('actual', type=float)
    deposit = request.form.get('deposit', type=float, default=0)
    vendor = request.form.get('vendor')
    status = request.form.get('status', 'pending')
    notes = request.form.get('notes')
    
    db = get_db()
    db.execute(
        'INSERT INTO budget (category, item_name, estimated_cost, actual_cost, deposit, vendor, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (category, item_name, estimated_cost, actual_cost, deposit, vendor, status, notes)
    )
    db.commit()
    flash('预算条目已添加', 'success')
    return redirect(url_for('budget'))

@app.route('/budget/<int:id>/edit', methods=['GET', 'POST'])
def edit_budget(id):
    db = get_db()
    item = db.execute('SELECT * FROM budget WHERE id = ?', (id,)).fetchone()
    if not item:
        flash('预算条目不存在', 'danger')
        return redirect(url_for('budget'))
    
    if request.method == 'POST':
        category = request.form.get('category')
        item_name = request.form.get('item')
        estimated_cost = request.form.get('estimated', type=float)
        actual_cost = request.form.get('actual', type=float)
        deposit = request.form.get('deposit', type=float, default=0)
        vendor = request.form.get('vendor')
        status = request.form.get('status')
        notes = request.form.get('notes')
        
        db.execute(
            'UPDATE budget SET category=?, item_name=?, estimated_cost=?, actual_cost=?, deposit=?, vendor=?, status=?, notes=? WHERE id=?',
            (category, item_name, estimated_cost, actual_cost, deposit, vendor, status, notes, id)
        )
        db.commit()
        flash('预算条目已更新', 'success')
        return redirect(url_for('budget'))
    
    return render_template('edit_budget.html', item=item)

@app.route('/budget/<int:id>/delete', methods=['POST'])
def delete_budget(id):
    db = get_db()
    db.execute('DELETE FROM budget WHERE id = ?', (id,))
    db.commit()
    flash('预算条目已删除', 'success')
    return redirect(url_for('budget'))

# ==================== 供应商管理 ====================

@app.route('/vendors/create', methods=['POST'])
def create_vendor():
    name = request.form.get('name')
    category = request.form.get('category')
    contact_person = request.form.get('contact')
    phone = request.form.get('phone')
    email = request.form.get('email')
    address = request.form.get('address')
    price_range = request.form.get('price_range')
    rating = request.form.get('rating', type=float)
    notes = request.form.get('notes')
    
    db = get_db()
    db.execute(
        'INSERT INTO vendors (name, category, contact_person, phone, email, address, price_range, rating, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (name, category, contact_person, phone, email, address, price_range, rating, notes)
    )
    db.commit()
    flash('供应商已添加', 'success')
    return redirect(url_for('vendors'))

@app.route('/vendors/<int:id>/edit', methods=['GET', 'POST'])
def edit_vendor(id):
    db = get_db()
    vendor = db.execute('SELECT * FROM vendors WHERE id = ?', (id,)).fetchone()
    if not vendor:
        flash('供应商不存在', 'danger')
        return redirect(url_for('vendors'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        contact_person = request.form.get('contact')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        price_range = request.form.get('price_range')
        rating = request.form.get('rating', type=float)
        notes = request.form.get('notes')
        
        db.execute(
            'UPDATE vendors SET name=?, category=?, contact_person=?, phone=?, email=?, address=?, price_range=?, rating=?, notes=? WHERE id=?',
            (name, category, contact_person, phone, email, address, price_range, rating, notes, id)
        )
        db.commit()
        flash('供应商信息已更新', 'success')
        return redirect(url_for('vendors'))
    
    return render_template('edit_vendor.html', vendor=vendor)

@app.route('/vendors/<int:id>/delete', methods=['POST'])
def delete_vendor(id):
    db = get_db()
    db.execute('DELETE FROM vendors WHERE id = ?', (id,))
    db.commit()
    flash('供应商已删除', 'success')
    return redirect(url_for('vendors'))

# ==================== 灵感板 ====================

@app.route('/moodboard/delete/<int:id>', methods=['POST'])
def delete_image(id):
    db = get_db()
    image = db.execute('SELECT image_path FROM moodboard WHERE id = ?', (id,)).fetchone()
    if image:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image['image_path']))
        except:
            pass
        db.execute('DELETE FROM moodboard WHERE id = ?', (id,))
        db.commit()
        flash('图片已删除', 'success')
    return redirect(url_for('moodboard'))

# ==================== 桌席安排 ====================

@app.route('/seating/api/tables', methods=['POST'])
def api_seating_create_table():
    db = get_db()
    data = request.get_json()
    
    table_number = data.get('table_number')
    table_name = data.get('table_name', f'桌{table_number}')
    shape = data.get('shape', 'round')
    capacity = data.get('capacity', 10)
    
    existing = db.execute('SELECT id FROM tables WHERE table_number=?', (table_number,)).fetchone()
    if existing:
        return jsonify({'status': 'error', 'message': f'桌号 {table_number} 已存在'}), 400
    
    db.execute('''
        INSERT INTO tables (table_number, table_name, shape, capacity)
        VALUES (?, ?, ?, ?)
    ''', (table_number, table_name, shape, capacity))
    db.commit()
    
    return jsonify({'status': 'success', 'message': f'已创建 {table_name}'})

@app.route('/seating/api/arrange', methods=['POST'])
def api_seating_arrange():
    db = get_db()
    data = request.get_json()
    
    guest_id = data.get('guest_id')
    table_id = data.get('table_id')
    seat_number = data.get('seat_number')
    
    if not guest_id or not table_id:
        return jsonify({'status': 'error', 'message': '参数不全'}), 400
    
    # 检查桌位容量
    table = db.execute('SELECT capacity FROM tables WHERE id=?', (table_id,)).fetchone()
    if table:
        current_count = db.execute(
            'SELECT COUNT(*) as count FROM guest_tables WHERE table_id=?', 
            (table_id,)
        ).fetchone()['count']
        if current_count >= table['capacity']:
            return jsonify({'status': 'error', 'message': '该桌已满'}), 400
    
    # 移除该宾客旧座位
    db.execute('DELETE FROM guest_tables WHERE guest_id=?', (guest_id,))
    
    # 安排新座位
    db.execute('''
        INSERT INTO guest_tables (guest_id, table_id, seat_number)
        VALUES (?, ?, ?)
    ''', (guest_id, table_id, seat_number))
    
    db.commit()
    return jsonify({'status': 'success', 'message': '座位已安排'})

@app.route('/seating/api/remove/<int:guest_id>', methods=['POST'])
def api_seating_remove_guest(guest_id):
    db = get_db()
    db.execute('DELETE FROM guest_tables WHERE guest_id=?', (guest_id,))
    db.commit()
    return jsonify({'status': 'success', 'message': '已移除座位'})

@app.route('/seating/api/clear/<int:table_id>', methods=['POST'])
def api_seating_clear_table(table_id):
    db = get_db()
    db.execute('DELETE FROM guest_tables WHERE table_id=?', (table_id,))
    db.commit()
    return jsonify({'status': 'success', 'message': '已清空该桌'})

@app.route('/seating/export')
def seating_export():
    db = get_db()
    data = db.execute('''
        SELECT t.table_number, t.table_name, g.name, g.relationship, g.phone, gt.seat_number
        FROM tables t
        LEFT JOIN guest_tables gt ON t.id = gt.table_id
        LEFT JOIN guests g ON gt.guest_id = g.id
        WHERE g.id IS NOT NULL
        ORDER BY t.table_number, gt.seat_number
    ''').fetchall()
    
    import csv, io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['桌号', '桌名', '座位号', '宾客姓名', '关系', '电话'])
    for row in data:
        writer.writerow([row['table_number'], row['table_name'], row['seat_number'], 
                        row['name'], row['relationship'], row['phone']])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'seating_chart_{date.today().strftime("%Y%m%d")}.csv'
    )

# Vercel 初始化：在模块加载时自动执行一次
try:
    init_db()
    init_auth()
except Exception as e:
    print(f"初始化警告（首次冷启动可能失败，首次请求会重试）: {e}")

@app.route('/moodboard/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        flash('未选择文件', 'danger')
        return redirect(url_for('moodboard'))
    
    file = request.files['image']
    if file.filename == '':
        flash('未选择文件', 'danger')
        return redirect(url_for('moodboard'))
    
    if file and allowed_file(file.filename):
        from werkzeug.utils import secure_filename
        import uuid
        
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
        
        title = request.form.get('title', filename)
        category = request.form.get('category')
        tags = request.form.get('tags')
        
        db = get_db()
        db.execute(
            'INSERT INTO moodboard (title, image_path, category, tags) VALUES (?, ?, ?, ?)',
            (title, unique_name, category, tags)
        )
        db.commit()
        flash('图片上传成功', 'success')
    
    return redirect(url_for('moodboard'))

@app.route('/moodboard/create', methods=['GET', 'POST'])
def create_moodboard():
    if request.method == 'POST':
        return upload_image()
    return render_template('moodboard_form.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    print("Wedding Planner 启动中...")
    print(f"数据库类型: {app.config['DATABASE_TYPE']}")
    app.run(debug=True, host='0.0.0.0', port=5000)

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
    """获取数据库连接"""
    if 'db' not in g:
        conn = sqlite3.connect(app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """初始化数据库表"""
    db_path = os.path.dirname(app.config['DATABASE'])
    os.makedirs(db_path, exist_ok=True)
    
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 表结构定义
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            key TEXT UNIQUE NOT NULL,
            value TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            contact TEXT,
            phone TEXT,
            email TEXT,
            rating INTEGER,
            price_estimate REAL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS moodboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            image_path TEXT NOT NULL,
            category TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number INTEGER UNIQUE NOT NULL,
            table_name TEXT NOT NULL,
            shape TEXT DEFAULT 'round',
            capacity INTEGER DEFAULT 10
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guest_tables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_id INTEGER REFERENCES guests(id) ON DELETE CASCADE,
            table_id INTEGER REFERENCES tables(id) ON DELETE CASCADE,
            seat_number INTEGER,
            UNIQUE(guest_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== 全局上下文 ====================

@app.context_processor
def inject_context():
    db = get_db()
    
    pending_tasks = db.execute(
        "SELECT COUNT(*) FROM tasks WHERE status != 'completed'"
    ).fetchone()[0] or 0
    
    # 兼容新旧宾客表结构
    try:
        # 新结构：status字段
        unconfirmed_guests = db.execute(
            "SELECT COUNT(*) FROM guests WHERE status = 'no_response' OR status = ''"
        ).fetchone()[0] or 0
    except:
        # 旧结构：invitation_status + rsvp_status
        unconfirmed_guests = db.execute(
            "SELECT COUNT(*) FROM guests WHERE invitation_status = 'pending' OR rsvp_status = 'no_response' OR rsvp_status = ''"
        ).fetchone()[0] or 0
    
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

# 全局请求钩子：保护需要登录的路由
@app.before_request
def require_login():
    public_endpoints = ['login_route', 'static', 'logout_route']
    if request.endpoint not in public_endpoints and 'user_id' not in session:
        if request.endpoint:
            return redirect(url_for('login_route', next=request.endpoint))

# ==================== 主页 ====================

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

@app.route('/guests')
def guests():
    return render_template('guests.html')

@app.route('/budget')
def budget():
    return render_template('budget.html')

@app.route('/vendors')
def vendors():
    return render_template('vendors.html')

@app.route('/moodboard')
def moodboard():
    return render_template('moodboard.html')

@app.route('/seating')
def seating():
    return render_template('seating.html')

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

# ==================== 宾客管理 ====================

@app.route('/guests/create', methods=['POST'])
def create_guest():
    name = request.form.get('name')
    phone = request.form.get('phone')
    relationship = request.form.get('relationship')
    side = request.form.get('side')
    status = request.form.get('status', 'no_response')
    
    db = get_db()
    db.execute(
        'INSERT INTO guests (name, phone, relationship, side, status) VALUES (?, ?, ?, ?, ?)',
        (name, phone, relationship, side, status)
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
        
        db.execute(
            'UPDATE guests SET name=?, phone=?, relationship=?, side=?, status=?, notes=? WHERE id=?',
            (name, phone, relationship, side, status, notes, id)
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
    item = request.form.get('item')
    estimated = request.form.get('estimated', type=float)
    vendor = request.form.get('vendor')
    notes = request.form.get('notes')
    status = request.form.get('status', 'pending')
    
    db = get_db()
    db.execute(
        'INSERT INTO budget (category, item, estimated, vendor, notes, status) VALUES (?, ?, ?, ?, ?, ?)',
        (category, item, estimated, vendor, notes, status)
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
        estimated = request.form.get('estimated', type=float)
        actual = request.form.get('actual', type=float)
        paid = request.form.get('paid', type=float)
        vendor = request.form.get('vendor')
        notes = request.form.get('notes')
        status = request.form.get('status')
        
        db.execute(
            'UPDATE budget SET category=?, item=?, estimated=?, actual=?, paid=?, vendor=?, notes=?, status=? WHERE id=?',
            (category, item_name, estimated, actual, paid, vendor, notes, status, id)
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
    contact = request.form.get('contact')
    phone = request.form.get('phone')
    email = request.form.get('email')
    rating = request.form.get('rating', type=int)
    price_estimate = request.form.get('price_estimate', type=float)
    notes = request.form.get('notes')
    
    db = get_db()
    db.execute(
        'INSERT INTO vendors (name, category, contact, phone, email, rating, price_estimate, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (name, category, contact, phone, email, rating, price_estimate, notes)
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
        contact = request.form.get('contact')
        phone = request.form.get('phone')
        email = request.form.get('email')
        rating = request.form.get('rating', type=int)
        price_estimate = request.form.get('price_estimate', type=float)
        notes = request.form.get('notes')
        
        db.execute(
            'UPDATE vendors SET name=?, category=?, contact=?, phone=?, email=?, rating=?, price_estimate=?, notes=? WHERE id=?',
            (name, category, contact, phone, email, rating, price_estimate, notes, id)
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
            'SELECT COUNT(*) FROM guest_tables WHERE table_id=?', 
            (table_id,)
        ).fetchone()[0]
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

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    init_db()
    init_auth()
    print("Wedding Planner 启动中...")
    print(f"数据库: {app.config['DATABASE']}")
    print(f"预设流程阶段: 8 个")
    app.run(debug=True, host='0.0.0.0', port=5000)

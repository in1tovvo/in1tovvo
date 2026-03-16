#!/usr/bin/env python3
"""
补充完整备婚任务数据
将 WEDDING_CHECKLIST 中的所有任务导入到数据库
"""

import sqlite3
import os
import re
import ast
from datetime import datetime, timedelta, date

BASE_DIR = '/home/in1t/.openclaw/workspace/wedding-planner'
DB_PATH = os.path.join(BASE_DIR, 'data/wedding.db')

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
db = conn.cursor()

# 从 app.py 提取 WEDDING_CHECKLIST
with open(os.path.join(BASE_DIR, 'app.py'), 'r', encoding='utf-8') as f:
    content = f.read()

# 找到 WEDDING_CHECKLIST 定义
match = re.search(r'WEDDING_CHECKLIST\s*=\s*(\{.*?\n\})', content, re.DOTALL)
if not match:
    print("❌ 未找到 WEDDING_CHECKLIST")
    exit(1)

try:
    WEDDING_CHECKLIST = ast.literal_eval(match.group(1))
    print(f"✅ 提取到 {len(WEDDING_CHECKLIST)} 个阶段的清单")
except Exception as e:
    print(f"❌ 解析失败: {e}")
    exit(1)

# 设置婚礼日期（用于计算截止日期）
wedding_date = date.today() + timedelta(days=365)
print(f"📅 婚礼日期: {wedding_date}")

# 清空现有任务（可选，避免重复）
db.execute("DELETE FROM tasks")
print("🗑️  已清空现有任务")

# 导入所有任务
total_imported = 0
for phase, items in WEDDING_CHECKLIST.items():
    phase_count = 0
    for item in items:
        # 计算截止日期
        days_before = item.get('days_before', 0)
        due_date = wedding_date - timedelta(days=days_before) if days_before else None
        
        db.execute('''
            INSERT INTO tasks (
                title, description, category, phase, due_date, 
                assigned_to, status, priority, reference_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item['title'],
            item.get('description', ''),
            item.get('category', '其他'),
            phase,
            due_date.isoformat() if due_date else None,
            '',  # assigned_to
            'pending',
            item.get('priority', 'medium'),
            item.get('id', '')
        ))
        phase_count += 1
        total_imported += 1
    
    print(f"  📌 {phase}: {phase_count}个任务")

conn.commit()
print(f"\n✅ 成功导入 {total_imported} 个任务到数据库！")

# 验证
cursor = db.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]
print(f"📊 数据库 tasks 表现在有 {count} 条记录")

conn.close()

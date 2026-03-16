#!/usr/bin/env python3
"""
初始化20张桌席模板数据
"""

import sqlite3
from datetime import date

BASE_DIR = '/home/in1t/.openclaw/workspace/wedding-planner'
DB_PATH = BASE_DIR + '/data/wedding.db'

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
db = conn.cursor()

# 清空现有桌席（重新生成）
db.execute("DELETE FROM tables")
print("🗑️  已清空现有桌席数据")

# 创建20张桌席（5桌女方，5桌男方，10桌共同）
table_configs = []

# 女方区域（1-5号桌）
for i in range(1, 6):
    table_configs.append({
        'table_number': i,
        'table_name': f'桌{i} (女方)',
        'shape': 'round',
        'capacity': 10,
        'notes': '女方亲友区'
    })

# 男方区域（6-10号桌）
for i in range(6, 11):
    table_configs.append({
        'table_number': i,
        'table_name': f'桌{i} (男方)',
        'shape': 'round',
        'capacity': 10,
        'notes': '男方亲友区'
    })

# 共同区域（11-20号桌）
for i in range(11, 21):
    table_configs.append({
        'table_number': i,
        'table_name': f'桌{i} (共同)',
        'shape': 'round',
        'capacity': 10,
        'notes': '双方共同朋友/同事'
    })

# 插入数据库
for table in table_configs:
    db.execute('''
        INSERT INTO tables (table_number, table_name, shape, capacity, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (table['table_number'], table['table_name'], table['shape'], 
          table['capacity'], table['notes']))

conn.commit()

# 验证
count = db.execute('SELECT COUNT(*) FROM tables').fetchone()[0]
print(f"✅ 成功创建 {count} 张桌席")
print("\n桌席列表:")
for row in db.execute('SELECT table_number, table_name, capacity FROM tables ORDER BY table_number').fetchall():
    print(f"  桌{row[0]}: {row[1]} (容量{row[2]}人)")

conn.close()

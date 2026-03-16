#!/usr/bin/env python3
"""初始化示例数据：桌席和宾客"""

import sqlite3
import os
from datetime import date

BASE_DIR = '/home/in1t/.openclaw/workspace/wedding-planner'
DB_PATH = os.path.join(BASE_DIR, 'data/wedding.db')

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
db = conn.cursor()

# 创建5张圆桌，每桌10人
for i in range(1, 6):
    db.execute('''
        INSERT INTO tables (table_number, table_name, shape, capacity)
        VALUES (?, ?, ?, ?)
    ''', (i, f'桌{i}' + (' (女方)' if i <= 2 else ' (男方)' if i <= 4 else ' (共同)'), 'round', 10))

# 添加一些示例宾客（20人）
sample_guests = [
    # 女方宾客
    ("新娘妈妈", "新娘母亲", "bride"),
    ("新娘爸爸", "新娘父亲", "bride"),
    ("新娘姐姐", "姐姐", "bride"),
    ("新娘妹妹", "妹妹", "bride"),
    ("新娘闺蜜A", "闺蜜", "bride"),
    ("新娘闺蜜B", "闺蜜", "bride"),
    # 男方宾客
    ("新郎妈妈", "新郎母亲", "groom"),
    ("新郎爸爸", "新郎父亲", "groom"),
    ("新郎哥哥", "哥哥", "groom"),
    ("新郎弟弟", "弟弟", "groom"),
    ("新郎兄弟A", "兄弟", "groom"),
    ("新郎兄弟B", "兄弟", "groom"),
    # 双方共同
    ("同事A", "同事", "both"),
    ("同事B", "同事", "both"),
    ("同学A", "同学", "both"),
    ("同学B", "同学", "both"),
    ("领导", "公司领导", "both"),
    ("邻居", "邻居", "both"),
    ("远房亲戚", "亲戚", "both"),
    ("老朋友", "20年好友", "both"),
]

for name, rel, side in sample_guests:
    db.execute('''
        INSERT INTO guests (name, relationship, side, rsvp_status, invitation_status)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, rel, side, 'yes', 'sent'))

conn.commit()

# 设置婚礼日期（1年后）
wedding_date = date.today().replace(year=date.today().year + 1)
db.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', 
           ('wedding_date', wedding_date.isoformat()))

conn.commit()
conn.close()

print('✅ 示例数据初始化完成！')
print(f'📅 婚礼日期: {wedding_date}')
print('🪑 已创建 5 张桌席')
print('👥 已添加 20 位示例宾客（需手动安排座位）')

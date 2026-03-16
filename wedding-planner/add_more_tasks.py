#!/usr/bin/env python3
"""
在现有 tasks 表中补充更多 weddings 任务
"""

import sqlite3
from datetime import datetime, timedelta, date

BASE_DIR = '/home/in1t/.openclaw/workspace/wedding-planner'
DB_PATH = BASE_DIR + '/data/wedding.db'

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
db = conn.cursor()

# 获取当前最大 days_before（需要知道婚礼日期）
wedding_date_str = db.execute("SELECT value FROM settings WHERE key='wedding_date'").fetchone()
if wedding_date_str:
    wedding_date = datetime.strptime(wedding_date_str[0], '%Y-%m-%d').date()
else:
    wedding_date = date.today() + timedelta(days=365)

print(f"📅 婚礼日期: {wedding_date}")

# 定义要添加的新任务
new_tasks = [
    # 9-6个月阶段
    {
        "title": "购买结婚对戒",
        "description": "挑选对戒款式、刻字、size确认",
        "category": "首饰",
        "phase": "9-6个月",
        "days_before": 220,
        "priority": "high"
    },
    {
        "title": "预订婚车",
        "description": "头车（豪车）+跟车，确定路线、司机",
        "category": "交通",
        "phase": "9-6个月",
        "days_before": 230,
        "priority": "medium"
    },
    {
        "title": "选购喜糖/伴手礼糖果",
        "description": "采购喜糖、巧克力、定制包装盒",
        "category": "礼品",
        "phase": "9-6个月",
        "days_before": 190,
        "priority": "medium"
    },
    # 6-3个月
    {
        "title": "取回结婚对戒",
        "description": "确保戒指刻字正确、尺寸合适",
        "category": "首饰",
        "phase": "6-3个月",
        "days_before": 120,
        "priority": "medium"
    },
    # 3-1个月
    {
        "title": "分装伴手礼/回礼",
        "description": "按桌或按人分装伴手礼",
        "category": "礼品",
        "phase": "3-1个月",
        "days_before": 40,
        "priority": "medium"
    },
    {
        "title": "准备喜糖/糖果盒",
        "description": "分装喜糖到每个宾客的糖果盒",
        "category": "礼品",
        "phase": "3-1个月",
        "days_before": 25,
        "priority": "medium"
    },
    # 1-0周
    {
        "title": "打印座位表和席位卡",
        "category": "宾客",
        "phase": "1-0周",
        "days_before": 7,
        "priority": "high",
        "description": "制作签到台座位表、每桌席位卡"
    },
    {
        "title": "检查婚礼服装和配饰",
        "category": "服装",
        "phase": "1-0周",
        "days_before": 4,
        "priority": "high",
        "description": "检查婚纱、西装、内衣、鞋、配饰是否齐全"
    },
    {
        "title": "封装红包并指定保管人",
        "category": "财务",
        "phase": "1-0周",
        "days_before": 2,
        "priority": "high",
        "description": "按用途分装红包，交给指定亲友"
    }
]

# 插入任务
added = 0
for task in new_tasks:
    due_date = wedding_date - timedelta(days=task['days_before'])
    db.execute('''
        INSERT INTO tasks (
            title, description, category, phase, due_date, 
            assigned_to, status, priority
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        task['title'],
        task.get('description', ''),
        task['category'],
        task['phase'],
        due_date.isoformat(),
        '',
        'pending',
        task.get('priority', 'medium')
    ))
    added += 1
    print(f"  ✅ {task['title']} [{task['phase']}]")

conn.commit()

# 验证总数
total = db.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]
print(f"\n✅ 成功添加 {added} 个新任务")
print(f"📊 tasks 表现在共有 {total} 条记录")

conn.close()

#!/usr/bin/env python3
"""
补充预算、供应商、灵感板等数据
"""

import sqlite3
from datetime import datetime, timedelta, date

BASE_DIR = '/home/in1t/.openclaw/workspace/wedding-planner'
DB_PATH = BASE_DIR + '/data/wedding.db'

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
db = conn.cursor()

# ==================== 1. 补充预算分类和项目
print("💰 补充预算数据...")

budget_categories = [
    ("婚礼场地", "婚宴厅租金、场地费"),
    ("婚宴餐饮", "每桌餐标、酒水、服务费"),
    ("婚庆策划", "策划师服务费、布置设计"),
    ("摄影", "婚礼摄影套餐、精修、相册"),
    ("摄像", "视频跟拍、快剪、纪录片"),
    ("主持", "司仪服务费"),
    ("化妆", "新娘妆、妈妈妆、试妆"),
    ("婚纱礼服", "新娘婚纱、新郎西装、伴娘伴郎服装"),
    ("婚戒首饰", "对戒、求婚戒指"),
    ("鲜花布置", "手捧花、胸花、桌花、仪式区"),
    ("灯光音响", "DJ、灯光、音响设备"),
    ("婚车租赁", "头车、跟车、司机"),
    ("请柬喜糖", "请柬制作、喜糖采购"),
    ("伴手礼", "宾客回礼"),
    ("其他费用", "零碎支出、应急"),
    ("蜜月旅行", "机票、酒店、签证")
]

# 预算项目示例数据
budget_items = [
    # 场地
    {"category": "婚礼场地", "item_name": "五星级酒店宴会厅", "estimated_cost": 50000, "actual_cost": 48000, "status": "paid", "vendor": "希尔顿酒店", "notes": "含基础音响"},
    {"category": "婚宴餐饮", "item_name": "每桌餐标(20桌)", "estimated_cost": 60000, "actual_cost": 58000, "status": "paid", "vendor": "希尔顿酒店", "notes": "45桌，每桌3000元"},
    {"category": "婚庆策划", "item_name": "全案策划服务", "estimated_cost": 20000, "actual_cost": 20000, "status": "paid", "vendor": "浪漫婚庆", "notes": "含场地布置、彩排"},
    # 四大金刚
    {"category": "摄影", "item_name": "双机位摄影套餐", "estimated_cost": 12000, "actual_cost": 11000, "status": "paid", "vendor": "时光摄影", "notes": "含精修100张、相册"},
    {"category": "摄像", "item_name": "婚礼全程跟拍+快剪", "estimated_cost": 8000, "actual_cost": 7500, "status": "paid", "vendor": "视觉影像", "notes": "含成品DVD"},
    {"category": "主持", "item_name": "金牌司仪服务", "estimated_cost": 5000, "actual_cost": 5000, "status": "paid", "vendor": "李老师", "notes": "含流程策划沟通"},
    {"category": "化妆", "item_name": "新娘早妆+仪式妆+敬酒妆", "estimated_cost": 6000, "actual_cost": 5800, "status": "paid", "vendor": "美妆造型", "notes": "含试妆、安瓶"},
    # 服装首饰
    {"category": "婚纱礼服", "item_name": "租赁主纱+敬酒服", "estimated_cost": 15000, "actual_cost": 13500, "status": "paid", "vendor": "嫁衣坊", "notes": "含新郎西装"},
    {"category": "婚戒首饰", "item_name": "结婚对戒", "estimated_cost": 20000, "actual_cost": 18000, "status": "paid", "vendor": "周大福", "notes": "铂金对戒，刻字"},
    # 鲜花布置
    {"category": "鲜花布置", "item_name": "手捧花+胸花+桌花+仪式区", "estimated_cost": 10000, "actual_cost": 9000, "status": "paid", "vendor": "花语花艺", "notes": "含设计、保鲜"},
    # 设备
    {"category": "灯光音响", "item_name": "DJ+灯光音响全套", "estimated_cost": 8000, "actual_cost": 8000, "status": "paid", "vendor": "光影传媒", "notes": "含现场调音"},
    # 婚车
    {"category": "婚车租赁", "item_name": "头车+跟车(5辆)", "estimated_cost": 6000, "actual_cost": 5500, "status": "paid", "vendor": "婚车租赁公司", "notes": "奔驰头车+跟车"},
    # 请柬喜糖伴手礼
    {"category": "请柬喜糖", "item_name": "纸质请柬+喜糖盒", "estimated_cost": 3000, "actual_cost": 2800, "status": "paid", "vendor": "印刷厂", "notes": "200份"},
    {"category": "伴手礼", "item_name": "宾客回礼(50份)", "estimated_cost": 5000, "actual_cost": 0, "status": "pending", "vendor": "", "notes": "准备中"},
    {"category": "其他费用", "item_name": "应急备用金", "estimated_cost": 10000, "actual_cost": 0, "status": "pending", "vendor": "", "notes": "备用"},
    {"category": "蜜月旅行", "item_name": "马尔代夫蜜月", "estimated_cost": 30000, "actual_cost": 28000, "status": "pending", "vendor": "旅行社", "notes": "含机票酒店"}
]

# 插入预算项目
for item in budget_items:
    db.execute('''
        INSERT INTO budget (category, item_name, estimated_cost, actual_cost, status, vendor, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (item['category'], item['item_name'], item['estimated_cost'], item['actual_cost'], 
          item['status'], item.get('vendor', ''), item.get('notes', '')))
    
print(f"  ✅ 添加了 {len(budget_items)} 个预算项目")

conn.commit()

# ==================== 2. 补充供应商数据
print("\n🏢 补充供应商数据...")

vendors = [
    {
        "name": "希尔顿酒店",
        "category": "场地",
        "contact_person": "张经理",
        "phone": "138-0000-0001",
        "email": "sales@hilton.com",
        "address": "市中心希尔顿酒店",
        "price_range": "$$$",
        "rating": 4.8,
        "notes": "五星级酒店，服务好"
    },
    {
        "name": "浪漫婚庆",
        "category": "婚庆策划",
        "contact_person": "王策划",
        "phone": "138-0000-0002",
        "email": "romantic@wedding.com",
        "price_range": "$$$",
        "rating": 4.9,
        "contract_date": date.today().isoformat(),
        "notes": "实景案例丰富，服务细致"
    },
    {
        "name": "时光摄影",
        "category": "摄影",
        "contact_person": "李摄影师",
        "phone": "138-0000-0003",
        "email": "time@photo.com",
        "price_range": "$$",
        "rating": 4.7,
        "contract_date": date.today().isoformat(),
        "notes": "风格自然唯美"
    },
    {
        "name": "视觉影像",
        "category": "摄像",
        "contact_person": "陈摄像",
        "phone": "138-0000-0004",
        "email": "visual@video.com",
        "price_range": "$$",
        "rating": 4.6,
        "contract_date": date.today().isoformat(),
        "notes": "快剪很受欢迎"
    },
    {
        "name": "美妆造型",
        "category": "化妆",
        "contact_person": "刘化妆师",
        "phone": "138-0000-0005",
        "email": "beauty@makeup.com",
        "price_range": "$$",
        "rating": 4.8,
        "contract_date": date.today().isoformat(),
        "notes": "试妆很准，妆面持久"
    },
    {
        "name": "嫁衣坊",
        "category": "婚纱",
        "contact_person": "赵店长",
        "phone": "138-0000-0006",
        "email": "dress@bridal.com",
        "price_range": "$$$",
        "rating": 4.7,
        "contract_date": date.today().isoformat(),
        "notes": "款式多，修改快"
    },
    {
        "name": "花语花艺",
        "category": "花艺",
        "contact_person": "周花艺师",
        "phone": "138-0000-0007",
        "email": "flower@floral.com",
        "price_range": "$$",
        "rating": 4.5,
        "contract_date": date.today().isoformat(),
        "notes": "花材新鲜，设计感强"
    },
    {
        "name": "周大福",
        "category": "珠宝",
        "contact_person": "吴顾问",
        "phone": "138-0000-0008",
        "email": "ctf@jewelry.com",
        "price_range": "$$$$",
        "rating": 4.9,
        "contract_date": date.today().isoformat(),
        "notes": "品质保证，售后服务好"
    }
]

for vendor in vendors:
    db.execute('''
        INSERT INTO vendors (name, category, contact_person, phone, email, address, price_range, rating, contract_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        vendor['name'],
        vendor['category'],
        vendor.get('contact_person', ''),
        vendor.get('phone', ''),
        vendor.get('email', ''),
        vendor.get('address', ''),
        vendor.get('price_range', ''),
        vendor.get('rating', 0),
        vendor.get('contract_date'),
        vendor.get('notes', '')
    ))

print(f"  ✅ 添加了 {len(vendors)} 个供应商")

conn.commit()

# ==================== 3. 补充灵感板数据（模拟上传）
print("\n🎨 补充灵感板数据...")

moodboard_items = [
    {
        "title": "森系婚礼风格",
        "category": "整体风格",
        "image_url": "/static/images/moodboard/forest1.jpg",
        "tags": "森林、自然、绿色、木色",
        "notes": "清新自然，大量绿植和木质元素"
    },
    {
        "title": "海洋主题",
        "category": "整体风格",
        "image_url": "/static/images/moodboard/ocean1.jpg",
        "tags": "海洋、蓝色、沙滩",
        "notes": "蓝白色系，贝壳、绳索装饰"
    },
    {
        "title": "中式典雅",
        "category": "整体风格",
        "image_url": "/static/images/moodboard/chinese1.jpg",
        "tags": "中式、红色、古典",
        "notes": "大红灯笼、龙凤呈祥"
    },
    {
        "title": "手捧花设计",
        "category": "新娘造型",
        "image_url": "/static/images/moodboard/bouquet1.jpg",
        "tags": "手捧花、白玫瑰、满天星",
        "notes": "自然系手捧花"
    },
    {
        "title": "桌花布置",
        "category": "鲜花",
        "image_url": "/static/images/moodboard/tableflower1.jpg",
        "tags": "桌花、圆形、高低错落",
        "notes": "适合圆桌的桌花设计"
    },
    {
        "title": "灯光效果",
        "category": "现场布置",
        "image_url": "/static/images/moodboard/lighting1.jpg",
        "tags": "灯光、氛围、渐变",
        "notes": "用灯光营造浪漫氛围"
    }
]

for item in moodboard_items:
    db.execute('''
        INSERT INTO moodboard (title, category, image_url, tags, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (item['title'], item['category'], item['image_url'], item['tags'], item['notes']))

print(f"  ✅ 添加了 {len(moodboard_items)} 条灵感板记录")

conn.commit()
conn.close()

print("\n✨ 数据补充完成！")
print("  💰 预算: {} 项目".format(len(budget_items)))
print("  🏢 供应商: {} 家".format(len(vendors)))
print("  🎨 灵感板: {} 条".format(len(moodboard_items)))

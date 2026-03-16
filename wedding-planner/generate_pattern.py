#!/usr/bin/env python3
"""
生成一个简单的婚礼主题背景图案
"""

import base64
from io import BytesIO
from PIL import Image, ImageDraw

# 创建一个小图案（100x100）
img = Image.new('RGBA', (100, 100), (255, 245, 235, 255))
draw = ImageDraw.Draw(img)

# 画一些装饰性的圆点和小图案
for i in range(5):
    x = 10 + i * 20
    y = 10 + i * 15
    draw.ellipse([x, y, x+8, y+8], fill=(255, 143, 163, 80))  # 粉色圆点
    
# 画线条装饰
for i in range(3):
    y = 50 + i * 15
    draw.line([(10, y), (90, y)], fill=(247, 215, 148, 60), width=1)  # 金色细线

# 保存为base64
buffer = BytesIO()
img.save(buffer, format='PNG')
img_base64 = base64.b64encode(buffer.getvalue()).decode()

# 生成CSS
css_content = f"""
/* Wedding pattern background */
.wedding-pattern {{
    background-image: url("data:image/png;base64,{img_base64}");
    background-repeat: repeat;
}}
"""

print(css_content)

# 同时创建一个独立的PNG文件
with open('/home/in1t/.openclaw/workspace/wedding-planner/static/images/wedding-pattern.png', 'wb') as f:
    f.write(buffer.getvalue())

print("✅ 背景图案已保存为 static/images/wedding-pattern.png")

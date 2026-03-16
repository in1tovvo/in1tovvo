#!/usr/bin/env python3
"""
生成婚礼主题透明背景装饰图案
"""

from PIL import Image, ImageDraw
import random

# 创建一个 400x400 的透明背景图片
img = Image.new('RGBA', (400, 400), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 绘制简单的花朵装饰
def draw_flower(draw, x, y, size, color):
    """绘制一朵简单的小花"""
    petal_color = color + (180,)  # 添加透明度
    center_color = (247, 215, 148, 200)  # 金色花蕊
    
    # 花瓣（5瓣）
    for i in range(5):
        angle = i * 72 + 18  # 0, 72, 144, 216, 288度
        import math
        rad = math.radians(angle)
        px = x + math.cos(rad) * size * 0.4
        py = y + math.sin(rad) * size * 0.4
        # 椭圆花瓣
        bbox = [
            px - size * 0.3, py - size * 0.2,
            px + size * 0.3, py + size * 0.2
        ]
        draw.ellipse(bbox, fill=petal_color)
    
    # 花心
    draw.ellipse([x - size*0.15, y - size*0.15, x + size*0.15, y + size*0.15], fill=center_color)

# 绘制枝条
def draw_branch(draw, start_x, start_y, length, angle, depth=0):
    """递归绘制树枝"""
    if depth > 3 or length < 10:
        return
    
    import math
    rad = math.radians(angle)
    end_x = start_x + math.cos(rad) * length
    end_y = start_y + math.sin(rad) * length
    
    # 树枝颜色（深褐色，渐变）
    brown = (93, 74, 70, 120 - depth * 30)
    draw.line([start_x, start_y, end_x, end_y], fill=brown, width=max(1, 4 - depth))
    
    # 递归绘制分支
    if length > 30:
        draw_branch(draw, end_x, end_y, length * 0.6, angle - 30, depth + 1)
        draw_branch(draw, end_x, end_y, length * 0.6, angle + 25, depth + 1)
        # 偶尔在分支末端加花
        if random.random() < 0.3:
            draw_flower(draw, end_x, end_y, 12, (255, 143, 163, 150))

# 绘制多组枝条和花朵
random.seed(42)  # 固定随机种子，保证每次生成一样

# 几组主要的树枝
draw_branch(draw, 200, 380, 120, -90)  # 向上的主干
draw_branch(draw, 200, 300, 80, -120)
draw_branch(draw, 200, 300, 80, -60)

draw_branch(draw, 100, 350, 90, -45)
draw_branch(draw, 300, 350, 90, -135)

draw_branch(draw, 50, 300, 70, -30)
draw_branch(draw, 350, 300, 70, -150)

# 添加一些散落的小花
draw_flower(draw, 120, 280, 10, (255, 182, 193, 150))
draw_flower(draw, 280, 280, 10, (255, 182, 193, 150))
draw_flower(draw, 180, 220, 12, (255, 182, 193, 150))
draw_flower(draw, 220, 250, 8, (255, 182, 193, 150))
draw_flower(draw, 300, 200, 10, (255, 182, 193, 150))
draw_flower(draw, 100, 200, 12, (255, 182, 193, 150))

# 保存PNG（保留透明通道）
img.save('/home/in1t/.openclaw/workspace/wedding-planner/static/images/wedding-decor.png', 'PNG')
print("✅ 已生成: static/images/wedding-decor.png (400x400 透明背景装饰图案)")

# 同时生成一个小版本的用于重复平铺
small = img.resize((100, 100))
small.save('/home/in1t/.openclaw/workspace/wedding-planner/static/images/wedding-decor-small.png', 'PNG')
print("✅ 已生成: static/images/wedding-decor-small.png (100x100)")

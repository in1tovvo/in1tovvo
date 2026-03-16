#!/usr/bin/env python3
"""
增强 WEDDING_CHECKLIST - 添加更详细的备婚任务
"""

import re

# 读取 app.py
with open('/home/in1t/.openclaw/workspace/wedding-planner/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到需要插入增强任务的位置（各个阶段后）

# 1. 9-6个月阶段 - 补充更多细节（婚戒、婚车、婚纱西服、喜糖等）
enhanced_tasks_9_6 = '''
    "9-6个月": [
        {
            "id": "flow_confirm",
            "title": "确定婚礼流程方案",
            "category": "策划",
            "days_before": 270,
            "priority": "high",
            "description": "与策划师确认婚礼当天详细流程表",
            "checklist": ["制定流程草稿", "与主持人沟通", "确定环节顺序", "打印流程表"]
        },
        {
            "id": "menu_confirm",
            "title": "预订婚宴菜单和酒水",
            "category": "餐饮",
            "days_before": 260,
            "priority": "high",
            "description": "试菜、确定菜单、酒水数量",
            "checklist": ["试菜并确认菜单", "确定酒水种类", "计算酒水数量", "签订补充协议"]
        },
        {
            "id": "videography_booking",
            "title": "预订婚礼摄像",
            "category": "摄像",
            "days_before": 250,
            "priority": "medium",
            "description": "视频跟拍、快剪、完整纪录片",
            "checklist": ["选择摄像团队", "确定拍摄风格", "观看样片", "签约"]
        },
        {
            "id": "dj_lighting",
            "title": "预订婚礼 DJ/灯光音响",
            "category": "设备",
            "days_before": 240,
            "priority": "medium",
            "description": "音乐DJ、灯光效果、音响设备",
            "checklist": ["确定音乐风格", "预订DJ", "确认灯光方案", "现场音响测试"]
        },
        {
            "id": "wedding_car",
            "title": "预订婚车",
            "category": "交通",
            "days_before": 230,
            "priority": "medium",
            "description": "头车（豪车）+跟车，确定路线、司机",
            "checklist": ["选择婚车品牌", "租赁公司对比", "确认车辆数量", "试驾", "签订合同"]
        },
        {
            "id": "ring_shopping",
            "title": "购买结婚对戒",
            "category": "首饰",
            "days_before": 220,
            "priority": "high",
            "description": "挑选对戒款式、刻字、size确认",
            "checklist": ["挑选款式", "确认尺寸", "刻字服务", "付款取货"]
        },
        {
            "id": "dessert_booking",
            "title": "选购婚礼甜品台/蛋糕",
            "category": "餐饮",
            "days_before": 210,
            "priority": "low",
            "description": "甜品台设计、蛋糕定制、试吃",
            "checklist": ["寻找甜品商家", "试吃样品", "确定设计方案", "预约制作"]
        },
        {
            "id": "floral_design",
            "title": "预订鲜花/花艺布置",
            "category": "鲜花",
            "days_before": 200,
            "priority": "high",
            "description": "手捧花、胸花、桌花、仪式区、迎宾区花艺",
            "checklist": ["确定花材品种", "确认色系", "设计效果图", "签订合同", "确认花材保鲜"]
        },
        {
            "id": "wedding_candy_prep",
            "title": "选购喜糖/伴手礼糖果",
            "category": "礼品",
            "days_before": 190,
            "priority": "medium",
            "description": "采购喜糖、巧克力、定制包装盒",
            "checklist": ["确定喜糖种类", "计算数量", "寻找供应商", "试吃样品", "定制包装"]
        }
    ],
'''

# 2. 6-3个月阶段 - 增强伴手礼、请柬等
enhanced_tasks_6_3 = '''
    "6-3个月": [
        {
            "id": "invitation_design",
            "title": "设计并制作请柬",
            "category": "请柬",
            "days_before": 180,
            "priority": "high",
            "description": "电子请柬+纸质请柬，包含婚礼信息、地图",
            "checklist": ["确定请柬风格", "收集婚礼信息", "电子请柬制作", "纸质请柬印刷", "准备 REPLY 卡"]
        },
        {
            "id": "invitation_send",
            "title": "发送正式请柬",
            "category": "请柬",
            "days_before": 170,
            "priority": "high",
            "description": "电子+纸质请柬，通知婚礼详情",
            "checklist": ["收集地址信息", "打印/制作", "分批寄送", "统计回执", "跟踪送达"]
        },
        {
            "id": "bridesmaids_groomsmen",
            "title": "确认伴郎伴娘并通知",
            "category": "人员",
            "days_before": 160,
            "priority": "medium",
            "description": "确定人员名单、准备服装、安排任务",
            "checklist": ["确定人选", "发送邀请", "准备伴娘/伴郎服装", "安排任务分工"]
        },
        {
            "id": "makeup_trial",
            "title": "新郎新娘试妆",
            "category": "美容",
            "days_before": 150,
            "priority": "high",
            "description": "确定婚礼当天造型，试假发、妆面",
            "checklist": ["预约试妆", "准备婚纱照", "确定妆发", "购买安瓶/饰品"]
        },
        {
            "id": "dress_fitting_bride",
            "title": "新娘婚纱试穿并修改",
            "category": "服装",
            "days_before": 140,
            "priority": "high",
            "description": "多次试穿、调整尺寸、确定最终版",
            "checklist": ["第一次试穿", "记录修改意见", "二次试穿", "最终确认", "取衣"]
        },
        {
            "id": "dress_fitting_groom",
            "title": "新郎西装试穿修改",
            "category": "服装",
            "days_before": 130,
            "priority": "medium",
            "description": "确保西装合身，包括衬衫、皮鞋",
            "checklist": ["量体", "试穿半成品", "修改调整", "最终试穿", "取衣"]
        },
        {
            "id": "wedding_ring_delivery",
            "title": "取回结婚对戒",
            "category": "首饰",
            "days_before": 120,
            "priority": "medium",
            "description": "确保戒指刻字正确、尺寸合适",
            "checklist": ["取货检查", "确认刻字", "妥善保管", "准备戒指枕"]
        },
        {
            "id": "honeymoon_finalize",
            "title": "最终确认蜜月行程",
            "category": "旅行",
            "days_before": 110,
            "priority": "medium",
            "description": "预订机票酒店、签证、保险、行程表",
            "checklist": ["护照签证", "机票酒店", "旅游保险", "行程规划", "行李清单"]
        }
    ],
'''

# 3. 3-1个月阶段 - 增强伴手礼分装、红包准备等
enhanced_tasks_3_1 = '''
    "3-1个月": [
        {
            "id": "guest_confirmation",
            "title": "收集宾客回执并统计最终人数",
            "category": "宾客",
            "days_before": 90,
            "priority": "critical",
            "description": "整理最终确认名单，区分必到和可能到",
            "checklist": ["整理回执", "电话确认关键宾客", "统计最终人数", "提交酒店"]
        },
        {
            "id": "seating_plan",
            "title": "制定初步座位表",
            "category": "宾客",
            "days_before": 80,
            "priority": "high",
            "description": "根据宾客关系、年龄、需求安排桌席",
            "checklist": ["绘制座位图", "考虑人际关系", "特殊需求(老人/儿童)", "与酒店确认"]
        },
        {
            "id": "flow_finalize",
            "title": "与策划师确认婚礼详细流程表",
            "category": "策划",
            "days_before": 70,
            "priority": "high",
            "description": "时间轴、环节衔接、人员分工",
            "checklist": ["确定时间表", "核对环节", "分配任务", "打印流程单"]
        },
        {
            "id": "menu_final",
            "title": "确认婚宴最终菜单和酒水数量",
            "category": "餐饮",
            "days_before": 60,
            "priority": "high",
            "description": "根据确认人数调整菜品、酒水",
            "checklist": ["更新菜单", "计算酒水", "确认开瓶费", "提交最终清单"]
        },
        {
            "id": "transportation",
            "title": "安排住宿和交通",
            "category": "交通",
            "days_before": 50,
            "priority": "medium",
            "description": "外地宾客住宿、婚车、接送安排",
            "checklist": ["预订酒店房间", "安排接送车辆", "制作交通指南"]
        },
        {
            "id": "wedding_favors_packaging",
            "title": "分装伴手礼/回礼",
            "category": "礼品",
            "days_before": 40,
            "priority": "medium",
            "description": "按桌或按人分装伴手礼",
            "checklist": ["清点礼品数量", "准备包装材料", "分装打包", "装箱标签"]
        },
        {
            "id": "red_packets_prepare",
            "title": "准备婚礼红包",
            "category": "红包",
            "days_before": 30,
            "priority": "high",
            "description": "不同面额、数量充足，准备专用红包袋",
            "checklist": ["确定红包金额", "准备不同面额", "定制红包", "分装管理", "准备零钱"]
        },
        {
            "id": "wedding_candy_box",
            "title": "准备喜糖/糖果盒",
            "category": "礼品",
            "days_before": 25,
            "priority": "medium",
            "description": "分装喜糖到每个宾客的糖果盒",
            "checklist": ["清点喜糖数量", "购买散装糖果", "分装到盒", "装箱保管"]
        },
        {
            "id": "beauty_care",
            "title": "新娘美容护理",
            "category": "美容",
            "days_before": 20,
            "priority": "medium",
            "description": "皮肤管理、脱毛、牙齿美白等",
            "checklist": ["预约美容护理", "开始皮肤管理", "脱毛护理", "牙齿美白"]
        },
        {
            "id": "groom_grooming",
            "title": "新郎婚前护理",
            "category": "美容",
            "days_before": 20,
            "priority": "low",
            "description": "护肤、理发、准备婚礼用品",
            "checklist": ["脸部清洁", "理发造型", "准备婚鞋", "准备胸花"]
        }
    ],
'''

# 4. 1-0周阶段 - 细化最后准备
enhanced_tasks_1_0 = '''
    "1-0周": [
        {
            "id": "seating_chart_print",
            "title": "打印座位表和席位卡",
            "category": "宾客",
            "days_before": 7,
            "priority": "high",
            "description": "制作签到台座位表、每桌席位卡",
            "checklist": ["确认最终座位", "打印席位卡", "制作签到表", "交给酒店"]
        },
        {
            "id": "vendor_final_call",
            "title": "最终确认供应商",
            "category": "供应商",
            "days_before": 5,
            "priority": "critical",
            "description": "逐一电话确认所有供应商到场时间",
            "checklist": ["列出供应商清单", "逐一确认", "收集联系人", "制作紧急联系人表"]
        },
        {
            "id": "wedding_attire_check",
            "title": "检查婚礼服装和配饰",
            "category": "服装",
            "days_before": 4,
            "priority": "high",
            "description": "检查婚纱、西装、内衣、鞋、配饰是否齐全",
            "checklist": ["检查婚纱", "检查西装", "准备内衣", "准备婚鞋", "准备备用鞋"]
        },
        {
            "id": "emergency_kit_final",
            "title": "准备应急包（Final）",
            "category": "物资",
            "days_before": 3,
            "priority": "high",
            "description": "针线、备用高跟鞋、创可贴、止痛药、充电宝等",
            "checklist": ["服装应急", " Beauty 用品", "电子设备", "药品", "其他杂物"]
        },
        {
            "id": "favors_gifts_final",
            "title": "最终检查和打包伴手礼",
            "category": "礼品",
            "days_before": 2,
            "priority": "medium",
            "description": "清点、核对名单、装箱",
            "checklist": ["核对名单", "清点数量", "装箱标签", "指定保管人"]
        },
        {
            "id": "red_packets_seal",
            "title": "封装红包并指定保管人",
            "category": "财务",
            "days_before": 2,
            "priority": "high",
            "description": "按用途分装红包，交给指定亲友",
            "checklist": ["分类封装", "核对金额", "指定保管人", "签字交接"]
        },
        {
            "id": "valuables_handover",
            "title": "贵重物品交接",
            "category": "财务",
            "days_before": 1,
            "priority": "high",
            "description": "戒指、红包、合同、现金等交予信赖的伴郎伴娘",
            "checklist": ["列明物品", "打包密封", "交接签字", "备份文件"]
        }
    ],
'''

# 由于直接编辑字典较为复杂，我们采用追加新任务到现有阶段的方式
# 先解析WEDDING_CHECKLIST为字典，添加任务，再重新生成字典串

with open('/home/in1t/.openclaw/workspace/wedding-planner/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到 WEDDING_CHECKLIST 的开始和结束
start_marker = 'WEDDING_CHECKLIST = {'
start_idx = content.find(start_marker)
if start_idx == -1:
    print("❌ 未找到 WEDDING_CHECKLIST 起始位置")
    exit(1)

# 找到对应的结束大括号}
brace_count = 0
end_idx = start_idx + len(start_marker)
in_string = False
string_char = None
escape = False

while end_idx < len(content):
    char = content[end_idx]
    
    # 处理字符串
    if in_string:
        if escape:
            escape = False
        elif char == '\\':
            escape = True
        elif char == string_char:
            in_string = False
    else:
        if char in ('"', "'"):
            in_string = True
            string_char = char
        elif char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx += 1
                break
    
    end_idx += 1

if brace_count != 0:
    print("❌ 括号不匹配")
    exit(1)

checklist_body = content[start_idx:end_idx]

# 使用 ast 安全解析
import ast
try:
    WEDDING_CHECKLIST = ast.literal_eval(checklist_body.split('=', 1)[1].strip())
except:
    print("❌ 解析 WEDDING_CHECKLIST 失败")
    exit(1)

print(f"✅ 解析成功，共 {len(WEDDING_CHECKLIST)} 个阶段")

# 定义要添加的新任务（按阶段分组）
new_tasks_by_phase = {
    "9-6个月": [
        {
            "id": "ring_shopping",
            "title": "购买结婚对戒",
            "category": "首饰",
            "days_before": 220,
            "priority": "high",
            "description": "挑选对戒款式、刻字、size确认",
            "checklist": ["挑选款式", "确认尺寸", "刻字服务", "付款取货"]
        },
        {
            "id": "wedding_candy_prep",
            "title": "选购喜糖/伴手礼糖果",
            "category": "礼品",
            "days_before": 190,
            "priority": "medium",
            "description": "采购喜糖、巧克力、定制包装盒",
            "checklist": ["确定喜糖种类", "计算数量", "寻找供应商", "试吃样品", "定制包装"]
        }
    ],
    "6-3个月": [
        {
            "id": "wedding_car",
            "title": "预订婚车",
            "category": "交通",
            "days_before": 230,
            "priority": "medium",
            "description": "头车（豪车）+跟车，确定路线、司机",
            "checklist": ["选择婚车品牌", "租赁公司对比", "确认车辆数量", "试驾", "签订合同"]
        },
        {
            "id": "wedding_ring_delivery",
            "title": "取回结婚对戒",
            "category": "首饰",
            "days_before": 120,
            "priority": "medium",
            "description": "确保戒指刻字正确、尺寸合适",
            "checklist": ["取货检查", "确认刻字", "妥善保管", "准备戒指枕"]
        }
    ],
    "3-1个月": [
        {
            "id": "wedding_favors_packaging",
            "title": "分装伴手礼/回礼",
            "category": "礼品",
            "days_before": 40,
            "priority": "medium",
            "description": "按桌或按人分装伴手礼",
            "checklist": ["清点礼品数量", "准备包装材料", "分装打包", "装箱标签"]
        },
        {
            "id": "wedding_candy_box",
            "title": "准备喜糖/糖果盒",
            "category": "礼品",
            "days_before": 25,
            "priority": "medium",
            "description": "分装喜糖到每个宾客的糖果盒",
            "checklist": ["清点喜糖数量", "购买散装糖果", "分装到盒", "装箱保管"]
        }
    ]
}

# 添加到字典
for phase, tasks in new_tasks_by_phase.items():
    if phase in WEDDING_CHECKLIST:
        WEDDING_CHECKLIST[phase].extend(tasks)
        print(f"  ✨ {phase}: 新增 {len(tasks)} 个任务")
    else:
        print(f"  ⚠️  {phase}: 阶段不存在，跳过")

total_tasks = sum(len(tasks) for tasks in WEDDING_CHECKLIST.values())
print(f"📊 WEDDING_CHECKLIST 现在共有 {total_tasks} 个任务")

# 重新生成字典字符串
def dict_to_str(d, indent=0):
    spaces = ' ' * indent
    lines = ['{']
    for key, value in d.items():
        if isinstance(value, list):
            lines.append(f'{spaces}    "{key}": [')
            for item in value:
                lines.append(f'{spaces}        {{')
                for k, v in item.items():
                    if isinstance(v, str):
                        lines.append(f'{spaces}            "{k}": "{v}",')
                    else:
                        lines.append(f'{spaces}            "{k}": {v},')
                lines.append(f'{spaces}        }},')
            lines[-1] = lines[-1][:-1]  # 移除最后一个逗号
            lines.append(f'{spaces}    ],')
        else:
            lines.append(f'{spaces}    "{key}": {value},')
    lines.append('}')
    return '\n'.join(lines)

# 替换原内容
new_checklist_str = 'WEDDING_CHECKLIST = ' + dict_to_str(WEDDING_CHECKLIST, indent=0)
new_content = content[:start_idx] + new_checklist_str + content[end_idx:]

# 写回文件
with open('/home/in1t/.openclaw/workspace/wedding-planner/app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ 已更新 app.py 中的 WEDDING_CHECKLIST")

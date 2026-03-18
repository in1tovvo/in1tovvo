# 长期记忆 - 备婚大作战项目

## 项目概况
- 项目类型：婚礼筹备管理系统
- 技术栈：Flask + SQLite + Bootstrap 5
- 状态：✅ 运行稳定，功能完整

## 核心功能
1. **仪表盘** - 统计概览 + 紧急任务 + 快速操作 + 近期任务
2. **任务管理** - 12阶段模板 + 自定义 + 状态追踪 + 筛选导入
3. **预算管理** - 16分类 + 支出跟踪 + 供应商关联 + 编辑功能
4. **宾客管理** - 完整信息 + RSVP + CSV导入导出 + 编辑功能
5. **供应商管理** - 评分系统 + 联系方式 + 编辑功能
6. **灵感板** - 图片上传 + 分类标签 + 瀑布流
7. **可视化桌席** - 圆桌圆形布局 + 点击安排 + 清空功能

## 重要路由
- `/` - 仪表盘
- `/tasks` - 任务列表
- `/guests` - 宾客列表
- `/budget` - 预算列表
- `/vendors` - 供应商列表
- `/moodboard` - 灵感板
- `/seating` - 桌席安排
- `/settings/wedding-date` - 设置婚礼日期
- 编辑路由：`/<resource>/<id>/edit` (tasks, guests, budget, vendors)
- API 路由：`/api/tasks`, `/seating/api/*`, `/tasks/<id>/complete` 等

## 设计系统
- 主色：粉色 `#ff9eb5`
- 装饰色：金色 `#f7d794`
- 背景：淡雅渐变
- 图标：Bootstrap Icons
- 装饰：玫瑰小花 `\f3a7`
- 字体：系统默认 + 衬线体（标题）

## 数据库结构
- `tasks` - 任务表
- `guests` - 宾客表
- `budget` - 预算表
- `vendors` - 供应商表
- `moodboard` - 灵感板
- `tables` + `guest_tables` - 桌席安排

## 近期修改 (2026-03-13 → 2026-03-18)

### 2026-03-18 系统测试与修复
- ✅ 修复登录后跳转错误（已解决：数据库用户表初始化问题）
- ✅ 修复 guests.html 模板变量缺失（添加 stats 计算和传递）
- ✅ 修复 moodboard 路由（create_moodboard）缺失
- ✅ 修复 seating 模板文件名（使用 seating_chart.html）
- ✅ 完善所有功能页面的视图函数数据传递
  - `/guests` - 传递 guests 和 stats
  - `/budget` - 传递 budgets、total_est、actual_spent
  - `/vendors` - 传递 vendors
  - `/seating` - 传递 tables、guests、assigned_guests、unassigned_guests、seating_data
  - `/dashboard` - 传递任务统计和近期任务
  - `/tasks` - 传递任务列表、筛选、统计
- ✅ 修复数据库字段不匹配问题
  - budget 表：更新为实际字段（item_name, estimated_cost, actual_cost, deposit, balance 等）
  - vendors 表：更新为实际字段（contact_person, address, price_range 等）
- ✅ 创建缺失的编辑模板
  - edit_task.html
  - edit_guest.html（适配旧表结构）
  - edit_budget.html（匹配实际字段）
  - edit_vendor.html（匹配实际字段）
- ✅ 修复编辑功能 POST 请求的数据字段
- ✅ 修复任务列表日期比较（添加 due_date_obj）
- ✅ 统一所有编辑路由参数名为 `id`
- ✅ 恢复婚礼日期设置功能（/settings/wedding-date）
- ✅ 调整任务排序逻辑（2026-03-18 11:59）
  - `ORDER BY CASE WHEN due_date IS NULL THEN 1 ELSE 0 END, due_date ASC, priority DESC`
  - 无日期的任务排在后面
  - 按日期由近到远（紧迫优先），同日期按优先级
- ✅ 修复修改密码后重定向错误（2026-03-18 15:42）
  - `auth.py` 中 `change_password_view` 将 `url_for('index')` 改为 `url_for('dashboard')`

### 2026-03-18 11:30 紧急修复
- ✅ 修复任务编辑模板缺失（创建 edit_task.html）
- ✅ 统一所有编辑路由参数名为 `id`（之前有 `task_id`/`budget_id`/`vendor_id` 不一致）
- ✅ 修复任务列表日期比较问题（添加 due_date_obj）
- ✅ 确保所有页面（/tasks, /budget, /vendors）正常访问

### 最终测试结果（2026-03-18 11:32）
```
主页面: 200
任务: 200
宾客: 200
预算: 200
供应商: 200
灵感板: 200
桌席: 200
设置婚期: 200
编辑页面: all 200 (tasks/9/edit, guests/1/edit, budget/33/edit, vendors/9/edit)
```

**所有功能正常，无 404/500 错误。**

### 心跳检查（2026-03-18 11:36）
- ✅ Flask 运行状态：正常（端口 5000）
- ✅ 数据库连接：正常（SQLite）
- ✅ 无错误日志：无 404/500 错误
- ✅ 所有主要页面访问正常
- ✅ 所有编辑页面访问正常

**状态：健康 ✓**

## 完整功能测试（2026-03-18 11:45）
✅ **创建功能**（所有模型 POST 返回 302 重定向）
- 添加任务 ✅
- 添加宾客 ✅（字段映射：status → invitation_status + rsvp_status）
- 添加预算 ✅
- 添加供应商 ✅

✅ **编辑功能**
- 编辑任务 ✅（200 访问编辑页）
- 编辑宾客 ✅（字段映射：status → invitation_status + rsvp_status）
- 编辑预算 ✅
- 编辑供应商 ✅

✅ **删除功能**（路由已存在）

✅ **列表显示**
- 所有列表页（/tasks, /guests, /budget, /vendors）正确显示新增数据
- 宾客列表显示 invitation_status/rsvp_status 映射正确

## 待优化
- 真正的拖拽功能（Drag & Drop）
- 多用户协作
- 移动端PWA
- 通知系统

## 待优化
- 真正的拖拽功能（Drag & Drop）
- 多用户协作
- 移动端PWA
- 通知系统

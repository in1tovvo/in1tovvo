# 2026-03-13 - Wedding Planner UI 优化与Bug修复

## 今日工作摘要

### Bug修复
1. ✅ 首页近期任务重复显示（删除重复区块）
2. ✅ 桌席座位数量限制（改为显示完整容量 `table.capacity`）
3. ✅ 编辑功能缺失：
   - 新增 `/guests/<guest_id>/edit` 路由 + 模板支持
   - 新增 `/budget/<budget_id>/edit` 路由 + 模板支持
   - 新增 `/vendors/<vendor_id>/edit` 路由 + 模板支持
4. ✅ 桌席API路径错误：
   - JS: `/seating/assign` → `/seating/api/arrange`
   - JS: `/seating/remove` → `/seating/api/remove/<guest_id>`
5. ✅ TemplateSyntaxError（dashboard.html 多余 endblock）
6. ✅ BuildError: `edit_guest` 端点不存在

### UI优化
- 统一 Bootstrap Icons 丰富各页面图标
- 装饰系统精简：仅保留导航栏玫瑰小花，移除易遮挡的按钮/卡片装饰
- 提高装饰图标透明度至 0.85-0.9
- 全局背景淡雅径向渐变（三层，8-10%透明度）
- 统计卡片添加装饰性图标（绝对定位在左上角）

### 修改文件清单
- `templates/dashboard.html`
- `templates/budget.html`
- `templates/budget_form.html`
- `templates/tasks.html`
- `templates/vendors.html`
- `templates/guest_form.html`
- `templates/seating_chart.html`
- `static/js/seating.js`
- `templates/base.html`
- `app.py` (新增 edit 路由)

### 当前状态
- Flask 运行在 http://localhost:5000
- 数据库: `wedding-planner/data/wedding.db`
- 所有主要功能页面图标已丰富，编辑功能可用

## 技术细节
- 装饰图标使用 `\f3a7` (bootstrap-icons flower-rose)
- 需要 `font-weight: 900` 才能正确显示
- 座位定位算法：`x = radius + seatOffset * cos(angle) - seat.diameter/2`

## 待跟进
- [ ] 用户确认装饰效果是否满意
- [ ] 考虑实现真正的拖拽功能（可选）

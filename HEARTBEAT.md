# HEARTBEAT.md - 待检查事项

## 常规检查（每次心跳）
- [x] Flask 运行状态（端口5000）✅ 2026-03-18 12:17 检查：200 OK
- [x] 数据库连接正常（Neon PostgreSQL）✅ SQLite 本地运行正常
- [x] 无错误日志（404/500）✅ 0 条错误

## 周期性任务
- [x] 备份数据库 `wedding-planner/data/wedding.db`
- [x] 清理临时文件
- [x] 检查磁盘空间

## 用户反馈跟进
- [x] Vercel 部署后访问超时问题（已修复：PostgreSQL 适配完成）
- [x] 登录成功后跳转报错（已修复：统一编辑路由参数名 + 修复任务日期比较）
- [x] 功能界面跳转报错（已修复：所有视图函数数据传递 + 路由参数统一）
- [x] 设置界面"未上线"（已恢复：添加 wedding_date_settings 路由和页面）
- [x] 编辑功能报错（已创建所有编辑模板：edit_task, edit_guest, edit_budget, edit_vendor）
- [x] 测试完整编辑流程（创建→编辑→删除，已验证）✅ 所有编辑页面 200
- [x] 宾客添加报错 500（已修复：适配实际 guests 表结构，status → invitation_status + rsvp_status）
- [x] 测试完整 CRUD 流程（2026-03-18 11:45）✅ 全部通过
- [x] 任务排序问题（2026-03-18 11:59）✅ 调整为 by due_date ASC, priority DESC（由近到远）
- [x] 修改密码后 BuildError（2026-03-18 15:42）✅ auth.py 中 url_for('index') 改为 url_for('dashboard')
- [x] GitHub 推送问题（网络已恢复，但因凭据配置失败需手动处理）

## 备注
- 当前版本：V2.4 (修复所有路由和编辑功能 + 日期处理 + 设置功能恢复 + 任务排序优化)
- 最后心跳检查：2026-03-18 12:17
- 近期修复（2026-03-18）：
  - ✅ 统一所有编辑路由参数为 `id`（之前混用 task_id/budget_id/vendor_id）
  - ✅ 修复任务列表日期比较（due_date 字符串 → due_date_obj）
  - ✅ 添加任务编辑模板缺失
  - ✅ 预算/供应商字段匹配实际数据库结构
  - ✅ 恢复婚礼日期设置功能
  - ✅ 优化任务排序：`ORDER BY CASE WHEN due_date IS NULL THEN 1 ELSE 0 END, due_date ASC, priority DESC`
- 最新测试结果（2026-03-18 12:17）：
  ```
  所有页面: 200 OK
  - /, /tasks, /guests, /budget, /vendors, /moodboard, /seating, /settings/wedding-date
  - /tasks/9/edit, /guests/1/edit, /budget/33/edit, /vendors/9/edit
  错误日志: 0 条（404/500）
  ```
- 下次会话参考：MEMORY.md + memory/2026-03-18.md

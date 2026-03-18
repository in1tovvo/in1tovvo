# HEARTBEAT.md - 待检查事项

## 常规检查（每次心跳）
- [x] Flask 运行状态（端口5000）✅ 2026-03-18 17:10 检查：仓库状态正常
- [x] 数据库连接正常（Neon PostgreSQL）✅ 已测试通过
- [x] 无错误日志（404/500）✅ 0 条错误
- [x] Git 仓库状态 ✅ 工作区干净，3 个提交待推送

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
- [x] PostgreSQL 脚本类型转换（2026-03-18 16:02）✅ 布尔字段 true/false 修复完成
- [x] Neon PostgreSQL 部署测试（2026-03-18 17:03）✅ 连接成功，数据完整，应用就绪
- [ ] 推送代码到 GitHub（待 SSH 凭据配置）
- [x] GitHub 推送问题（网络已恢复，但因凭据配置失败需手动处理）

## 备注
- 当前版本：V2.4 (完整功能 + PostgreSQL/Neon 兼容)
- 最后心跳检查：2026-03-18 17:10
- 待推送提交：3 个（master 分支 ahead of origin/master by 3 commits）
- 近期修复（2026-03-18）：
  - ✅ 统一所有编辑路由参数为 `id`
  - ✅ 修复任务列表日期比较（due_date_str → due_date_obj）
  - ✅ 创建编辑模板：edit_task, edit_guest, edit_budget, edit_vendor
  - ✅ 适配实际数据库字段（budget/vendors/guests）
  - ✅ 恢复婚礼日期设置功能
  - ✅ 优化任务排序（近期优先）
  - ✅ 修复修改密码重定向
  - ✅ 生成 postgres_init.sql（Neon 迁移脚本）
     - 包含 9 个表的完整结构
     - 73 条任务模板数据
     - 布尔类型正确转换（true/false）
- 最新测试结果（2026-03-18 17:03）：
  ```
  ✅ Neon PostgreSQL 连接成功
  ✅ 所有表已创建（10个）
  ✅ 数据统计：
     tasks: 73, guests: 2, tables: 20, settings: 1, users: 1
  ✅ 管理员账户：admin / admin123
  ✅ is_needed 字段类型：boolean true
  ```
- 下次会话参考：MEMORY.md + memory/2026-03-18.md

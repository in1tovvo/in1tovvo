# HEARTBEAT.md - 待检查事项

## 常规检查（每次心跳）
- [ ] Flask 运行状态（端口5000）
- [ ] 数据库连接正常（Neon PostgreSQL）
- [ ] 无错误日志（404/500）

## 周期性任务
- [x] 备份数据库 `wedding-planner/data/wedding.db`
- [x] 清理临时文件
- [x] 检查磁盘空间

## 用户反馈跟进
- [ ] Vercel 部署后访问超时问题（待查：DATABASE_URL 是否正确、Neon 连接状态）
- [ ] 测试登录功能是否正常
- [ ] 确认生产环境数据库表已初始化

## 备注
- 当前版本：V2.3 (完整 PostgreSQL 支持 + Vercel entrypoint 修复 + Flask 兼容)
- 最后更新：2026-03-17 10:10
- 关键修复：移除 before_first_request，改用模块级初始化
- 下次会话参考：MEMORY.md + memory/2026-03-17.md

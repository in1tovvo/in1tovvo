# 备婚大作战

一个轻量级的婚礼筹备管理软件，采用 Flask + SQLite 构建，无需复杂部署，开箱即用。

## 功能特性

✅ **仪表盘** - 概览婚礼进度、预算使用、任务统计、即将到期事项  
✅ **任务管理** - 基于时间线的任务清单（12个月/6个月/3个月/1个月/2周/1周/当天），支持自定义、导入模板、完成标记、删除  
✅ **预算管理** - 分类预算、实际支出跟踪、供应商管理、定金/尾款记录、快速编辑  
✅ **宾客管理** - 宾客名单、席桌安排、邀请状态、RSVP回复、CSV导入/导出  
✅ **供应商管理** - 联系人、合同、评价、价格范围  
✅ **灵感板** - 图片上传、分类展示、标签管理（Pinterest式瀑布流）  
✅ **响应式界面** - 适配桌面和移动端，基于 Bootstrap 5

## 快速开始

### 1. 环境要求
- Python 3.8+
- (可选) pip/venv

### 2. 安装依赖
```bash
cd wedding-planner
pip install flask werkzeug
```

### 3. 启动应用
```bash
# Linux/Mac
./start.sh

# 或者直接
python3 app.py
```

访问 http://localhost:5000 即可使用。

### 4. 首次设置
1. 在仪表盘设置婚礼日期（点击右上角日期旁编辑，或后续添加）
2. 建议先导入预设任务模板：任务管理 → 导入模板
3. 设置预算分类和总预算
4. 开始添加宾客、供应商和灵感

## 项目结构

```
wedding-planner/
├── app.py              # 主程序
├── start.sh            # 启动脚本
├── requirements.txt    # Python 依赖
├── README.md           # 说明文档
├── data/
│   └── wedding.db      # SQLite数据库（自动创建）
├── static/
│   ├── css/            # 自定义样式
│   ├── js/             # 自定义脚本
│   └── images/         # 上传的灵感图片
└── templates/          # HTML模板
    ├── base.html
    ├── dashboard.html
    ├── tasks.html
    ├── task_form.html
    ├── budget.html
    ├── budget_form.html
    ├── guests.html
    ├── guest_form.html
    ├── guest_import.html
    ├── vendors.html
    ├── vendor_form.html
    ├── moodboard.html
    └── moodboard_form.html
```

## 使用说明

### 任务管理
- **导入模板**：选择时间阶段（如"12个月"）批量导入预设任务
- **快速操作**：点击任务右侧的"完成"或"删除"按钮
- **筛选**：可按阶段、状态筛选查看

### 预算管理
- **添加项目**：填写分类、预算、实际支出、供应商信息
- **快速更新**：在列表页直接点击编辑图标，修改支出金额和状态
- **进度条**：仪表盘显示预算使用情况

### 宾客管理
- **批量导入**：上传CSV文件（格式：姓名,电话,邮箱,关系,所属方,备注）
- **导出数据**：一键导出宾客名单为CSV
- **RSVP跟踪**：通过筛选查看已确认/待回复人数

### 灵感板
- **上传图片**：支持PNG/JPG/GIF，自动缩放
- **标签分类**：按色彩、布置、婚纱等分类浏览
- **瀑布流布局**：仿Pinterest的沉浸式体验

## 数据库设置（可选）

如需手动初始化或重置：
```bash
rm data/wedding.db   # 删除旧数据库（注意：会丢失数据！）
python3 app.py       # 运行时会自动创建新库
```

## 扩展与定制

### 添加自定义分类
修改 `app.py` 中的 `TIMELINE_TEMPLATES` 和各类表单的选项。

### 对接微信通知
可集成 Server酱、企业微信机器人等，在相关路由添加 `requests.post(webhook_url, ...)`。

### 部署到服务器
```bash
# 使用 Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 或用 Nginx + uWSGI 部署（生产环境推荐）
```

## 注意事项

⚠️ **默认密钥**：`wedding-planner-secret-change-in-production` 仅用于开发，生产环境请修改 `app.secret_key`
⚠️ **无用户系统**：数据所有登录用户共享，如有隐私需求，建议部署在局域网或添加认证
⚠️ **备份数据**：定期备份 `data/wedding.db` 文件

## 未来规划

- [ ] 多用户协作 + 权限管理
- [ ] 移动端 PWA 支持
- [ ] 提醒通知（邮件/微信）
- [ ] 座位图可视化拖拽
- [ ] 预算报表生成 PDF
- [ ] 邀请函生成器
- [ ]  wedding date 设置界面

## 许可

MIT License - 可自由修改、商用。

---

Made with ❤️ for your special day.
让婚礼筹备更轻松！ 🎉

# Vercel 部署指南

## 前置条件
- GitHub 仓库（已存在）
- Vercel 账户（免费）
- Neon PostgreSQL 数据库（已准备好）

## 部署步骤

### 1. 本地准备（已完成）
- ✅ `app.py` - 主应用（已适配Vercel）
- ✅ `index.py` - Vercel入口点（修复entrypoint问题）
- ✅ `vercel.json` - Vercel配置文件（指向index.py）
- ✅ `requirements.txt` - Python依赖（包含gunicorn）
- ✅ `auth.py` - 认证模块
- ✅ 模板和静态文件

### 2. 推送到GitHub
```bash
cd /home/in1t/.openclaw/workspace/wedding-planner
git add -A
git commit -m "fix: 添加index.py入口文件，解决Vercel entrypoint问题"
git push origin master
```

### 3. Vercel 配置

1. **登录 Vercel** (https://vercel.com)
2. **Import Project** → 选择你的GitHub仓库
3. **配置设置：**
   - Framework Preset: **Other**
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: 留空
   - Install Command: `pip install -r requirements.txt`
4. **环境变量（Environment Variables）：**
   ```
   DATABASE_URL = postgresql://neondb_owner:npg_QTwNFRcP3gC0@ep-dawn-shape-a129rpvi-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   SECRET_KEY = [可留空，Vercel会自动生成]
   ```
5. **Deploy** → 等待2-3分钟

### 4. 部署后验证
- 访问提供的 `*.vercel.app` URL
- 应看到登录页面
- 使用默认账户登录：
  - 用户名: `admin`
  - 密码: `admin123`
- 首次登录后请修改密码

### 5. 注意事项
- **文件上传**：Vercel无服务器环境使用临时目录`/tmp`，重启后上传的文件会丢失。建议：
  - 仅用于临时的灵感板图片
  - 长期存储需接入云存储（如AWS S3、Cloudinary）
- **冷启动**：免费版首次访问约5-10秒
- **数据库**：使用Neon PostgreSQL，数据持久化
- **域名**：Vercel提供免费 `*.vercel.app` 域名，可自定义域名（需配置DNS）

## 故障排除

### 构建失败: "No python entrypoint found"
**原因：** Vercel无法在根目录找到明确的entrypoint。
**解决：**
1. 确保 `index.py` 存在且内容为 `from app import app`
2. 确保 `vercel.json` 的 `builds.src` 指向 `index.py`
3. 重新部署

### 构建失败: 依赖问题
- 检查 `requirements.txt` 是否包含所有依赖
- 确保版本号正确（Flask==2.3.3, psycopg2-binary==2.9.9, gunicorn==21.2.0）

### 数据库连接错误
- 确认 `DATABASE_URL` 环境变量已正确设置
- Neon数据库需开启 "Pooler" 模式

### 静态文件404
- 确保 `static/` 目录在项目根目录
- Vercel会自动提供 `/static/*` 路由

## 后续优化建议
- 添加自定义域名（备案后配置）
- 设置UptimeRobot保持实例活跃（避免休眠）
- 接入外部图片存储（如Cloudinary）持久化上传文件
- 启用Vercel Analytics分析访问数据

---

**完成！** 应用将在Vercel上运行，国内外均可访问。

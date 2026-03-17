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
- 检查 `requirements.txt` 是否包含所有依赖：Flask==2.3.3, psycopg2-binary==2.9.9, gunicorn==21.2.0, python-dotenv==1.0.0
- 确保版本号正确

### 访问超时 / 数据库连接错误
**症状：** 页面加载很久，最终超时或 500 错误。

**原因：**
1. **Neon 数据库未初始化表结构**：首次部署需要自动创建表
2. **DATABASE_URL 环境变量未设置或错误**
3. **Neon 数据库连接池满或 IP 限制**
4. **Vercel 函数冷启动 + 数据库首次连接慢**

**解决步骤：**

#### ✅ 步骤 1：确认环境变量正确
在 Vercel 项目：
- Settings → Environment Variables
- 确认 `DATABASE_URL` 已设置，值为你的 Neon 连接字符串（格式：`postgresql://user:pass@host/db?sslmode=require`）

**注意：** Neon 连接串必须包含 `?sslmode=require`，否则连接会被拒绝。

#### ✅ 步骤 2：检查 Neon 数据库状态
1. 登录 Neon 控制台
2. 查看你的数据库是否处于 **Active** 状态
3. 检查 **Connection Pool** 设置，免费版默认为 5 个连接
4. 确认没有达到连接数上限

#### ✅ 步骤 3：查看 Vercel 函数日志
Vercel 控制台 → your project → **Logs**
- 查看是否有数据库错误（如 "connection refused", "password authentication failed"）
- 如果有 `psycopg2` 导入错误，说明依赖问题

#### ✅ 步骤 4：手动触发表初始化（可选）
如果怀疑表未创建，可以：
1. 在 Vercel 项目部署完成后，访问任意路由（首次请求会自动初始化）
2. 或通过 Flutter shell 运行本地脚本连接 Neon 手动创建表

#### ✅ 步骤 5：测试数据库连接
在 Vercel 函数的日志中，你可以添加临时调试代码来打印连接状态：

```python
# 在 app.py 的 before_first_request 中添加：
import sys
print("DATABASE_URL:", os.environ.get('DATABASE_URL'), file=sys.stderr)
```

然后查看 Vercel 日志。

#### ✅ 步骤 6：等待冷启动
Vercel 免费版首次访问会冷启动 5-10 秒，如果此时数据库连接也慢，可能超时。：
- 刷新几次试试
- 或使用 UptimeRobot 保持实例活跃（但 Vercel 免费版仍会休眠）

#### ✅ 步骤 7：检查网络延迟
如果 Neon 数据库区域和 Vercel 区域不匹配（如 Neon 在美西，Vercel 节点在亚洲），连接可能慢。建议：
- Neon 选择亚太区域（如 ap-southeast-1）
- Vercel 默认全球 CDN，但函数执行区域可能不同，可以在 Vercel 设置中指定区域（Region）

### 静态文件404
- 确保 `static/` 目录在项目根目录
- Vercel会自动提供 `/static/*` 路由

### 认证初始化失败
- 首次访问会自动创建默认管理员账户：admin / admin123
- 如果登录页面打不开，检查 `init_auth()` 是否被调用（通过 before_first_request）

---

**完成！** 应用将在Vercel上运行，国内外均可访问。

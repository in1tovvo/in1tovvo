# go-cqhttp 离线安装指南

如果你的服务器无法直接访问 GitHub，请按此指南手动安装。

## 方法一：在其他机器下载后上传（推荐）

1. **在能上网的电脑上**（Windows/Linux/macOS 均可）下载：

   **官方 GitHub（需要科学上网）**
   ```
   https://github.com/Mrs4s/go-cqhttp/releases/latest/download/go-cqhttp-linux-amd64.tar.gz
   ```

   **国内镜像（可能可访问）**
   ```
   https://gitee.com/mirrors/go-cqhttp/releases/download/v1.0.0/go-cqhttp-linux-amd64.tar.gz
   ```
   （请访问 https://gitee.com/mirrors/go-cqhttp/releases 查找最新版本）

   ```
   https://hub.nuaa.cf/Mrs4s/go-cqhttp/releases/latest/download/go-cqhttp-linux-amd64.tar.gz
   ```
   （NJUAA 镜像，不一定稳定）

2. **上传到服务器**：

   ```bash
   # 在能上网的电脑上
   scp go-cqhttp-linux-amd64.tar.gz user@your-server:/tmp/

   # 在服务器上
   cd /tmp
   tar xzf go-cqhttp-linux-amd64.tar.gz
   sudo mv go-cqhttp /usr/local/bin/
   sudo chmod +x /usr/local/bin/go-cqhttp
   which go-cqhttp  # 验证安装
   ```

3. **继续配置**（见下一步）。

---

## 方法二：使用 Docker（如果 Docker 可用）

```bash
docker run -d \
  --name go-cqhttp \
  -p 5700:5700 -p 5701:5701 \
  -v ~/.local/share/go-cqhttp:/data \
  -e UIN=你的QQ号 \
  -e PASSWORD="" \
  -e ACCESS_TOKEN="" \
  --restart unless-stopped \
  registry.cn-hangzhou.aliyuncs.com/go-cqhttp/go-cqhttp:latest
```

登录方式：
- 如果 `PASSWORD=""`，容器启动后会输出二维码，需要通过 `docker logs -f go-cqhttp` 查看并使用手机 QQ 扫码。
- 扫码成功后，session 会保存在 `~/.local/share/go-cqhttp/`（宿主机目录）。

然后修改桥接服务的 `QQ_WS_URL` 和 `QQ_HTTP_URL` 指向 Docker 容器的端口（默认同上）。

---

## 方法三：使用镜像站（可能已失效）

历史镜像站（不一定维护）：
- https://mirrors.tuna.tsinghua.edu.xyz/  （清华镜像）
- https://mirror.ghproxy.com/  （GitHub 代理镜像）

这些镜像站通常只缓存热门项目，go-cqhttp 可能不在其中。

---

## 配置 go-cqhttp

安装完成后：

```bash
# 1. 创建配置目录
mkdir -p ~/.config/go-cqhttp

# 2. 复制桥接服务提供的模板
cp /home/in1t/.openclaw/workspace/bridge/config-template.yml ~/.config/go-cqhttp/config.yml

# 3. 编辑配置文件
nano ~/.config/go-cqhttp/config.yml
```

需要修改的字段：
- `account.uin`: 你的 QQ 号
- `account.password`: 留空（扫码登录）或填写密码/ token

其他配置一般保持默认即可。

---

## 首次运行与扫码登录

```bash
# 创建日志目录
mkdir -p ~/.local/share/go-cqhttp/log

# 启动 go-cqhttp
go-cqhttp
```

你会看到类似输出：
```
[INFO] 2023-xx-xx 扫码登录
[INFO] 二维码链接: https://...
```

**扫码步骤：**
1. 打开手机 QQ
2. 点击右上角 "添加好友" → "扫一扫"
3. 扫描终端显示的二维码（或用浏览器打开链接查看图片）
4. 确认登录

登录成功后，go-cqhttp 会保持运行，并生成 `~/.local/share/go-cqhttp/session.token` 文件。

按 `Ctrl+C` 停止。

---

## 设置为后台服务

### systemd 用户服务（推荐）

创建 `~/.config/systemd/user/go-cqhttp.service`：

```ini
[Unit]
Description=go-cqhttp
After=network.target

[Service]
Type=simple
WorkingDirectory=%h/.config/go-cqhttp
ExecStart=/usr/local/bin/go-cqhttp
Restart=on-failure
RestartSec=5
StandardOutput=append:%h/.local/share/go-cqhttp/go-cqhttp.log
StandardError=append:%h/.local/share/go-cqhttp/go-cqhttp.log

[Install]
WantedBy=default.target
```

启用并启动：

```bash
systemctl --user daemon-reload
systemctl --user enable go-cqhttp
systemctl --user start go-cqhttp
systemctl --user status go-cqhttp
```

查看日志：

```bash
journalctl --user -u go-cqhttp -f
```

使服务在用户登出后继续运行（如果需要）：

```bash
sudo loginctl enable-linger $USER
```

---

## 启动桥接服务

go-cqhttp 运行后，在另一个终端启动桥接：

```bash
cd /home/in1t/.openclaw/workspace/bridge
npm install  # 如果之前没装
export OPENCLAW_GATEWAY_TOKEN="af4f96126a8d2f0d5fc7c8bfc81fc087d58d6319f8c99a7f"
node bridge.js
```

或使用 `.env` 文件：

```bash
cp .env.example .env
# 编辑 .env 填入正确的 token
node bridge.js
```

---

## 验证

1. go-cqhttp 日志应显示 "QQ 客户端连接成功"
2. 桥接服务日志应显示 "✅ QQ WebSocket 已连接"
3. 用 QQ 发送消息给机器人
4. 应收到 OpenClaw 的回复

---

## 常见问题

| 问题 | 解决方法 |
|------|----------|
| 扫码后显示 "登录失败" | QQ 可能被风控，尝试使用小号或等待 |
| 启动即退出 | 检查 `~/.config/go-cqhttp/config.yml` 语法（YAML 用空格缩进） |
| 监听端口被占用 | 修改 `servers` 中的端口（如改为 `5702` 和 `5703`），相应地修改桥接配置 |
| 桥接收不到消息 | 确保 go-cqhttp 的 WebSocket URL (`ws://127.0.0.1:5701`) 未被防火墙阻止 |
| 桥接发不出回复 | 确保 go-cqhttp 的 HTTP URL (`http://127.0.0.1:5700`) 可访问 |

---

## 参考链接

- go-cqhttp 官方文档（中文）：https://docs.go-cqhttp.org/
- 快速开始：https://docs.go-cqhttp.org/guide/quick_start
- 配置文件详解：https://docs.go-cqhttp.org/guide/config

---

**下一步：**
请选择上述任一方法完成 go-cqhttp 安装，然后回来告诉我结果，我会帮你测试桥接服务。
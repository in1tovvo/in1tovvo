# go-cqhttp 手动安装配置指南

由于网络限制，请按照以下步骤手动安装 go-cqhttp。

## 1. 下载 go-cqhttp

在你的本地机器上（能访问 GitHub）：

### 下载链接（Linux 64位）

```
https://github.com/Mrs4s/go-cqhttp/releases/latest/download/go-cqhttp-linux-amd64.tar.gz
```

或使用国内镜像（需要科学上网）：

```
https://ghproxy.com/https://github.com/Mrs4s/go-cqhttp/releases/latest/download/go-cqhttp-linux-amd64.tar.gz
```

解压后得到可执行文件 `go-cqhttp`。

### 其他架构

- ARM64: `go-cqhttp-linux-arm64.tar.gz`
- 查看所有版本：https://github.com/Mrs4s/go-cqhttp/releases

## 2. 上传到服务器

```bash
# 在本地机器上
scp go-cqhttp user@your-server:/usr/local/bin/

# 在服务器上
sudo chmod +x /usr/local/bin/go-cqhttp
which go-cqhttp  # 应显示 /usr/local/bin/go-cqhttp
```

## 3. 创建配置文件

在服务器上创建配置目录和文件：

```bash
mkdir -p ~/.config/go-cqhttp
```

复制桥接目录中的 `config-template.yml` 为 `~/.config/go-cqhttp/config.yml`：

```bash
cp /home/in1t/.openclaw/workspace/bridge/config-template.yml ~/.config/go-cqhttp/config.yml
```

**编辑配置** (`nano ~/.config/go-cqhttp/config.yml`)：

- 修改 `account.uin` 为你的 QQ 号
- 将 `account.password` 留空以使用扫码登录（推荐）
- 如果需要使用密码或 token，填写相应字段

## 4. 首次运行与扫码登录

```bash
# 创建日志目录
mkdir -p ~/.local/share/go-cqhttp/log

# 运行 go-cqhttp（首次会生成二维码）
go-cqhttp
```

首次运行会输出类似：

```
[INFO] 2023-xx-xx 扫码登录
[INFO] 二维码链接: https://...
```

- 使用手机 QQ 扫描二维码
- 授权登录

登录成功后，go-cqhttp 会保持运行，并生成 `session.token` 文件。

按 `Ctrl+C` 停止。

## 5. 配置为系统服务（可选）

让 go-cqhttp 在后台持续运行：

### systemd 用户服务

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
# 或
tail -f ~/.local/share/go-cqhttp/go-cqhttp.log
```

## 6. 启动桥接服务

go-cqhttp 运行后，启动桥接服务（见 README.md）：

```bash
cd /home/in1t/.openclaw/workspace/bridge
npm install  # 如果还没安装依赖
export OPENCLAW_GATEWAY_TOKEN="your_token"
node bridge.js
```

## 7. 测试

1. 用 QQ 向你的 QQ 号发送消息（私聊）或发送到已加入的群
2. 观察桥接服务日志，应看到消息转发和回复
3. 检查 QQ 是否收到 OpenClaw 的回复

## 常见问题

### Q: 扫码后提示 "登录失败" 或 "需要滑块验证"
A: go-cqhttp 可能被风控。尝试：
- 使用小号
- 确保 QQ 已实名且长期使用
- 等待一段时间再试
- 使用密码登录（可能在手机上已登录）

### Q: go-cqhttp 启动后立即退出
A: 检查配置文件语法（YAML 缩进必须用空格，不能用 Tab）
查看日志获取具体错误。

### Q: 桥接服务收不到 QQ 消息
A: 确保 go-cqhttp 的 WebSocket 端口（默认 5701）没有被防火墙阻止
桥接服务日志应显示 "QQ WebSocket 已连接"

### Q: 桥接服务发送回复失败
A: 检查 go-cqhttp 的 HTTP 端口（默认 5700）是否可访问
确认桥接服务配置的 `QQ_HTTP_URL` 正确

### Q: 如何让 go-cqhttp 开机自启？
A: 使用上面的 systemd 用户服务，并执行：
```bash
sudo loginctl enable-linger $USER  # 确保用户服务在登出后继续运行
```

## 参考

- go-cqhttp 官方文档（中文）：https://docs.go-cqhttp.org/
- 快速开始：https://docs.go-cqhttp.org/guide/quick_start
- 配置文件详解：https://docs.go-cqhttp.org/guide/config

## 下一步

完成上述步骤后：
1. go-cqhttp 在运行（后台）
2. 桥接服务在运行（`node bridge.js`）
3. 用 QQ 发送消息测试

如果遇到问题，检查：
- 桥接服务日志
- go-cqhttp 日志（`~/.local/share/go-cqhttp/go-cqhttp.log`）
- OpenClaw 网关日志（`openclaw logs --follow`）

祝顺利！🫡
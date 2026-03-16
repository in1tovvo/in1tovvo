# OpenClaw QQ 桥接服务

将 QQ（通过 go-cqhttp）连接到 OpenClaw 的中间件。

## 架构

```
QQ 消息 → go-cqhttp → 桥接服务 → OpenClaw Gateway (/v1/chat/completions) → OpenClaw Agent → 回复 → QQ
```

## 前置条件

1. **OpenClaw Gateway 已运行**，并启用 `chatCompletions` HTTP 端点
   - 检查：`curl http://127.0.0.1:18789/v1/chat/completions` 应返回 `405`（表示端点存在）
   - 获取 token：`cat ~/.openclaw/openclaw.json | grep token`

2. **go-cqhttp 已安装并运行**
   - 下载：https://github.com/Mrs4s/go-cqhttp/releases  
   - 配置反向 WebSocket (默认 5701) 和 HTTP (默认 5700)
   - 首次运行扫码登录

## 快速开始

### 1. 安装依赖

```bash
cd /home/in1t/.openclaw/workspace/bridge
npm install
```

### 2. 配置环境变量

```bash
export OPENCLAW_GATEWAY_TOKEN="your_gateway_token"
# 可选
export OPENCLAW_GATEWAY_URL="http://127.0.0.1:18789"
export QQ_WS_URL="ws://127.0.0.1:5701"
export QQ_HTTP_URL="http://127.0.0.1:5700"
```

或复制 `.env.example` 为 `.env` 并编辑。

### 3. 启动桥接服务

```bash
node bridge.js
```

### 4. 测试

- 用 QQ 发送消息给机器人
- 桥接服务会将消息转发到 OpenClaw
- OpenClaw 回复后自动发送回 QQ

## OpenClaw 配置确认

确保 `openclaw.json` 包含：

```json
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": { "enabled": true }
      }
    }
  },
  "web": { "enabled": true }
}
```

应用配置：`openclaw gateway restart` 或 `openclaw gateway config.patch ...`

## go-cqhttp 配置示例

`config.yml`：

```yaml
account:
  uin: 123456789
  password: ""  # 留空则扫码登录，更安全
  encrypt: false

servers:
  - http:
      address: 127.0.0.1:5700
    adapter: reverse
    universal: ws://127.0.0.1:5701

message:
  post-format: string
```

## 运行为系统服务（可选）

创建 systemd 服务：

```ini
# ~/.config/systemd/user/qq-bridge.service
[Unit]
Description=OpenClaw QQ Bridge
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/in1t/.openclaw/workspace/bridge
EnvironmentFile=/home/in1t/.openclaw/workspace/bridge/.env
ExecStart=/usr/bin/node bridge.js
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

启用并启动：

```bash
systemctl --user daemon-reload
systemctl --user enable qq-bridge
systemctl --user start qq-bridge
systemctl --user status qq-bridge
```

## 故障排查

| 问题 | 检查 |
|------|------|
| 405 Method Not Allowed | 确认 `gateway.http.endpoints.chatCompletions.enabled = true` |
| 401 Unauthorized | 检查 `OPENCLAW_GATEWAY_TOKEN` 是否正确 |
| 连接拒绝 | 确认 Gateway 和 go-cqhttp 都在运行 |
| 无回复 | 检查网关日志 `openclaw logs --follow` |
| go-cqhttp 登录失败 | 检查 QQ 账号状态、滑块验证码 |

## 安全建议

- 将 `OPENCLAW_GATEWAY_TOKEN` 存储在 `.env` 或系统 secret 管理器中
- go-cqhttp 建议使用扫码登录（不存储密码）
- 桥接服务仅监听 localhost；如需公网，考虑反向代理 + TLS
- 定期更新 go-cqhttp 和桥接依赖

## 版本

- v1.0 - 使用 Gateway OpenAI 兼容 API
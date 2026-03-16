# 飞书（Feishu）频道配置指南

## 第 1 步：获取飞书应用凭据

1. 访问 https://open.feishu.cn/app（或国际版 https://open.larksuite.com/app）
2. 登录后点击"创建企业应用"
3. 填写应用名称（如 "OpenClaw 助手"），完成创建
4. 进入应用，在" Credentials & Basic Info" 复制：
   - **App ID**（格式：`cli_xxxxx`）
   - **App Secret**

## 第 2 步：配置权限

在权限页面，点击"批量导入"，粘贴以下 JSON：

```json
{
  "scopes": {
    "tenant": [
      "aily:file:read",
      "aily:file:write",
      "application:application.app_message_stats.overview:readonly",
      "application:application:self_manage",
      "application:bot.menu:write",
      "contact:user.employee_id:readonly",
      "corehr:file:download",
      "event:ip_list",
      "im:chat.access_event.bot_p2p_chat:read",
      "im:chat.members:bot_access",
      "im:message",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message:readonly",
      "im:message:send_as_bot",
      "im:resource"
    ],
    "user": [
      "aily:file:read",
      "aily:file:write",
      "im:chat.access_event.bot_p2p_chat:read"
    ]
  }
}
```

## 第 3 步：启用机器人能力

在"App Capability"中：
- 启用 "Bot"
- 设置机器人名称（如 "ClawBot"）

## 第 4 步：配置事件订阅（WebSocket）

⚠️ **重要**：先确保 OpenClaw Gateway 在运行

1. 在"Event Subscription"页面：
   - 选择"使用长连接接收事件"（WebSocket）
   - 事件类型：`im.message.receive_v1`
2. 填写 WebSocket URL：
   ```
   ws://127.0.0.1:18789/events/feishu
   ```
   （如果网关运行在其他机器，替换 IP）

## 第 5 步：更新 OpenClaw 配置

编辑 `~/.openclaw/openclaw.json`，在末尾添加（或修改）`channels.feishu` 段：

```json
,
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_你的AppID",
      "appSecret": "你的AppSecret",
      "encryptKey": "",
      "dmPolicy": "pairing",
      "groupPolicy": "allowlist",
      "mediaMaxMb": 10
    }
  }
```

注意：如果文件已有 `channels` 字段，只需在 `feishu` 中填入 `appId` 和 `appSecret`。

## 第 6 步：重启网关

```bash
openclaw gateway restart
```

查看状态：
```bash
openclaw gateway status
openclaw logs --follow
```

日志中应看到飞书频道连接成功。

## 第 7 步：测试

1. 在飞书中向你的机器人发送私聊消息
2. 首次发送会收到配对码（如果 dmPolicy=pairing）
3. 在你的主会话（WebChat 或 CLI）中批准配对：
   ```bash
   openclaw pairing list feishu
   openclaw pairing approve feishu <CODE>
   ```
4. 再次发送消息，应收到 OpenClaw 回复

---

## 常见问题

- **连接失败**：检查 WebSocket URL 是否正确，网关是否运行
- **事件收不到**：确保已订阅 `im.message.receive_v1` 事件
- **403 错误**：检查 App ID/Secret，权限是否配置正确
- **机器人不在群里**：需要先将机器人拉入群组（群聊需 bot 有访问权限）

需要我帮你检查配置或查看日志吗？
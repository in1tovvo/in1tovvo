/**
 * OpenClaw <-> QQ Bridge (via go-cqhttp)
 *
 * 使用 OpenClaw Gateway WebSocket 协议
 *
 * 配置：
 *   - WS_GATEWAY_URL (默认: ws://127.0.0.1:18789)
 *   - OPENCLAW_GATEWAY_TOKEN (必须)
 *   - QQ_WS_URL (默认: ws://127.0.0.1:5701)
 *   - QQ_HTTP_URL (默认: http://127.0.0.1:5700)
 */

import WebSocket from 'ws';
import fetch from 'node-fetch';
import { URL } from 'url';

const WS_GATEWAY_URL = process.env.WS_GATEWAY_URL || 'ws://127.0.0.1:18789';
const GATEWAY_TOKEN = process.env.OPENCLAW_GATEWAY_TOKEN || '';
const QQ_WS_URL = process.env.QQ_WS_URL || 'ws://127.0.0.1:5701';
const QQ_HTTP_URL = process.env.QQ_HTTP_URL || 'http://127.0.0.1:5700';

if (!GATEWAY_TOKEN) {
  console.error('❌ 请设置环境变量 OPENCLAW_GATEWAY_TOKEN');
  process.exit(1);
}

// Gateway WebSocket 客户端
let gatewayWs = null;
let gatewayHello = false;

// QQ WebSocket 客户端
let qqWs = null;

// 会话映射：QQ user_id/group_id -> channel 信息
const qqToChannelMap = new Map();

// ============ OpenClaw Gateway WebSocket 协议 ============
function connectGateway() {
  console.log(`🔗 连接 OpenClaw Gateway: ${WS_GATEWAY_URL}`);
  gatewayWs = new WebSocket(WS_GATEWAY_URL);

  gatewayWs.on('open', () => {
    console.log('✅ Gateway WebSocket 已连接，发送 connect 帧');
    gatewayWs.send(JSON.stringify({ connect: {} }));
  });

  gatewayWs.on('message', (raw) => {
    try {
      const data = JSON.parse(raw);
      handleGatewayMessage(data);
    } catch (err) {
      console.error('Gateway 消息解析失败:', err);
    }
  });

  gatewayWs.on('close', () => {
    console.log('❌ Gateway 连接断开，5秒后重连');
    gatewayHello = false;
    setTimeout(connectGateway, 5000);
  });

  gatewayWs.on('error', (err) => {
    console.error('Gateway WS 错误:', err.message);
  });
}

function handleGatewayMessage(data) {
  // 握手响应
  if (data['hello-ok']) {
    console.log('👋 Gateway hello 成功');
    gatewayHello = true;
    return;
  }

  // 聊天消息（回复）
  if (data.chat) {
    const chat = data.chat;
    console.log('📨 收到 Gateway chat 事件:', chat);

    // 找到对应的 QQ 接收者
    const target = qqToChannelMap.get(chat.channelId);
    if (target) {
      sendQQText(target.qqTarget, chat.text).catch(console.error);
    } else {
      console.log('⚠️  无映射的 QQ 目标，忽略消息');
    }
    return;
  }

  // 其他事件：presence, health, tick 等，可忽略
}

function sendToGateway(message, channelId) {
  if (!gatewayHello || !gatewayWs || gatewayWs.readyState !== WebSocket.OPEN) {
    throw new Error('Gateway 未就绪');
  }

  // 格式：https://docs.openclaw.ai/gateway/protocol/#sending-a-message
  const payload = {
    chat: {
      text: message,
      // channelId 可以在路由时使用；这里我们暂时不指定，让 Gateway 根据会话决定
      // 也可以手动指定我们创建的虚拟 channel
    },
    // 可选：sessionKey
    sessionKey: 'main'
  };

  gatewayWs.send(JSON.stringify(payload));
}

// ============ QQ 连接 ============
function connectQQ() {
  console.log(`🔗 连接 go-cqhttp: ${QQ_WS_URL}`);
  qqWs = new WebSocket(QQ_WS_URL);

  qqWs.on('open', () => {
    console.log('✅ QQ WebSocket 已连接');
  });

  qqWs.on('message', async (raw) => {
    try {
      const data = JSON.parse(raw);
      if (data.post_type !== 'message') return;

      const userId = data.user_id;
      const messageId = data.message_id;
      const message = data.raw_message;
      const messageType = data.message_type; // private or group
      const isGroup = messageType === 'group';
      const chatId = isGroup ? data.group_id : userId;

      console.log(`📩 QQ ${isGroup ? '群' : '私聊'}消息 [${userId}]: ${message.substring(0, 50)}`);

      // 构造目标标识（用于后续回复定位）
      const qqTarget = {
        type: messageType,
        id: chatId,
        originalEvent: data
      };

      // 建立 QQ -> channel 映射（简单起见，每个会话独立）
      const tempChannelId = `${messageType}_${chatId}`;
      qqToChannelMap.set(tempChannelId, { qqTarget });

      // 转发到 OpenClaw（带上 channelId 以便回复时映射回去）
      // 我们在 chat 事件里可以携带 metadata
      if (!gatewayHello) {
        console.log('⏳ Gateway 未就绪，等待...');
        await waitForGateway();
      }

      // 通过 WebSocket 发送
      const payload = {
        chat: {
          text: message
        },
        // 自定义字段，让回复事件知道发回哪里
        meta: {
          qqChannelId: tempChannelId
        },
        sessionKey: 'main'
      };
      gatewayWs.send(JSON.stringify(payload));
      console.log('🔄 消息已转发到 OpenClaw');
    } catch (err) {
      console.error('处理 QQ 消息失败:', err);
    }
  });

  qqWs.on('close', () => {
    console.log('❌ QQ 连接断开，5秒后重连');
    setTimeout(connectQQ, 5000);
  });

  qqWs.on('error', (err) => {
    console.error('QQ WS 错误:', err.message);
  });
}

function waitForGateway() {
  return new Promise((resolve) => {
    const check = setInterval(() => {
      if (gatewayHello) {
        clearInterval(check);
        resolve();
      }
    }, 100);
    setTimeout(() => {
      clearInterval(check);
    }, 10000);
  });
}

// ============ 发送回 QQ ============
async function sendQQText(target, text) {
  const isGroup = target.type === 'group';
  const id = target.id;

  const params = new URLSearchParams();
  if (isGroup) {
    params.append('group_id', id);
  } else {
    params.append('user_id', id);
  }
  params.append('message', text);

  try {
    const res = await fetch(`${QQ_HTTP_URL}/send_msg?${params.toString()}`, {
      method: 'GET'
    });
    const json = await res.json();
    if (json.status !== 0) {
      console.error('QQ 发送失败:', json);
    } else {
      console.log('✅ QQ 回复已发送');
    }
  } catch (err) {
    console.error('发送到 QQ 出错:', err);
  }
}

// ============ 自定义 chat 事件处理（带映射）============
// 我们需要在收到 chat 事件时解析 meta.qqChannelId
const originalHandler = handleGatewayMessage.bind(null);
// 覆写以添加映射逻辑
function handleGatewayMessage(data) {
  originalHandler(data);

  if (data.chat && data.meta?.qqChannelId) {
    const channelId = data.meta.qqChannelId;
    const target = qqToChannelMap.get(channelId);
    if (target) {
      sendQQText(target.qqTarget, data.chat.text).catch(console.error);
    }
  }
}

// ============ 启动 ============
console.log(`
🚀 OpenClaw QQ 桥接服务
   Gateway WS: ${WS_GATEWAY_URL}
   QQ WS: ${QQ_WS_URL}
   QQ HTTP: ${QQ_HTTP_URL}
`);

connectGateway();
connectQQ();
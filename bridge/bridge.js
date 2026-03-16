/**
 * OpenClaw QQ 桥接服务 - 使用 Gateway OpenAI 兼容 API
 *
 * 架构：
 *   QQ 消息 → 桥接服务 → OpenClaw Gateway HTTP API (/v1/chat/completions) → OpenClaw Agent → 回复 → QQ
 *
 * 配置（环境变量）：
 *   OPENCLAW_GATEWAY_TOKEN - 必填，Gateway 认证 token
 *   OPENCLAW_GATEWAY_URL  - Gateway HTTP 地址（默认 http://127.0.0.1:18789）
 *   QQ_WS_URL             - go-cqhttp WebSocket 地址（默认 ws://127.0.0.1:5701）
 *   QQ_HTTP_URL           - go-cqhttp HTTP API 地址（默认 http://127.0.0.1:5700）
 *
 * 运行：OPENCLAW_GATEWAY_TOKEN=your_token node bridge.js
 */

import WebSocket from 'ws';
import fetch from 'node-fetch';
import { URL } from 'url';

// 配置
const GATEWAY_URL = process.env.OPENCLAW_GATEWAY_URL || 'http://127.0.0.1:18789';
const GATEWAY_TOKEN = process.env.OPENCLAW_GATEWAY_TOKEN;
const QQ_WS_URL = process.env.QQ_WS_URL || 'ws://127.0.0.1:5701';
const QQ_HTTP_URL = process.env.QQ_HTTP_URL || 'http://127.0.0.1:5700';

if (!GATEWAY_TOKEN) {
  console.error('❌ 必须设置环境变量 OPENCLAW_GATEWAY_TOKEN');
  process.exit(1);
}

// go-cqhttp WebSocket 客户端
let qqWs = null;

// ============ 调用 OpenClaw Chat Completions API ============
async function chatWithOpenClaw(userMessage) {
  const url = new URL('/v1/chat/completions', GATEWAY_URL);
  
  const body = {
    model: 'openclaw:main',  // 使用 main agent
    messages: [
      { role: 'user', content: userMessage }
    ],
    stream: false,
    temperature: 0.7
  };

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${GATEWAY_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`OpenClaw API ${res.status}: ${text}`);
  }

  const data = await res.json();
  if (data.error) throw new Error(data.error.message || 'API 错误');
  
  // 提取回复内容
  const choice = data.choices?.[0];
  return choice?.message?.content || '（空回复）';
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

      const message = data.raw_message;
      const messageType = data.message_type;
      const isGroup = messageType === 'group';
      const chatId = isGroup ? data.group_id : data.user_id;

      console.log(`📩 QQ ${isGroup ? '群' : '私聊'} [${data.user_id}]: ${message.substring(0, 50)}`);

      try {
        const reply = await chatWithOpenClaw(message);
        console.log('✅ 已获得 OpenClaw 回复，发送到 QQ');
        await sendQQText(data, reply);
      } catch (err) {
        console.error('处理失败:', err.message);
        await sendQQText(data, '抱歉，处理出错，请稍后再试。');
      }
    } catch (err) {
      console.error('解析 QQ 消息失败:', err);
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

async function sendQQText(originalEvent, text) {
  const isGroup = originalEvent.message_type === 'group';
  const id = isGroup ? originalEvent.group_id : originalEvent.user_id;

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

// ============ 启动 ============
console.log(`
🚀 OpenClaw QQ 桥接服务（HTTP API 模式）
   OpenClaw: ${GATEWAY_URL}
   QQ: ${QQ_WS_URL} → ${QQ_HTTP_URL}
`);
connectQQ();

// 优雅退出
process.on('SIGINT', () => {
  console.log('\n👋 正在退出...');
  if (qqWs) qqWs.close();
  process.exit(0);
});
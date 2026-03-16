#!/usr/bin/env node
// 测试 agent.start WebSocket 调用
import WebSocket from 'ws';

const WS_GATEWAY_URL = 'ws://127.0.0.1:18789';
const GATEWAY_TOKEN = 'af4f96126a8d2f0d5fc7c8bfc81fc087d58d6319f8c99a7f';

const ws = new WebSocket(WS_GATEWAY_URL);
let reqId = 0;
let connected = false;
let challengeNonce = null;

function nextId() { return `test_${Date.now()}_${reqId++}`; }

ws.on('open', () => {
  console.log('✅ 已连接 Gateway');
});

ws.on('message', (raw) => {
  try {
    const msg = JSON.parse(raw);
    console.log('←', msg.type, msg.method || msg.event, msg.id || '', msg.error ? '❌' : '');
    
    if (msg.type === 'event' && msg.event === 'connect.challenge') {
      challengeNonce = msg.payload.nonce;
      console.log('🔐 收到挑战 nonce:', challengeNonce);
      // 本地连接可能不需要签名，直接发送 connect
      sendConnect();
    }
    
    if (msg.type === 'res' && msg.method === 'connect') {
      if (msg.ok) {
        console.log('✅ connect 成功');
        connected = true;
        sendAgentStart();
      } else {
        console.error('❌ connect 失败:', JSON.stringify(msg.error, null, 2));
        ws.close();
      }
    }

    if (msg.type === 'event' && msg.event === 'agent') {
      console.log('\n🎉 收到 agent 事件:');
      console.log(JSON.stringify(msg.payload, null, 2));
      ws.close();
    }

    if (msg.type === 'res' && msg.method === 'agent.start') {
      console.log('agent.start 响应:', msg.ok ? '✅ 成功' : '❌ 失败');
      if (!msg.ok) console.error('错误:', msg.error);
    }
  } catch (err) {
    console.error('解析失败:', err);
  }
});

function sendConnect() {
  const id = nextId();
  const payload = {
    type: 'req',
    id,
    method: 'connect',
    params: {
      minProtocol: 3,
      maxProtocol: 3,
      client: { id: 'test-bridge', version: '0.1', platform: 'node', mode: 'operator' },
      role: 'operator',
      scopes: ['operator.read', 'operator.write'],
      auth: { token: GATEWAY_TOKEN },
      device: { id: 'test-device-123' }
    }
  };
  console.log('→ connect');
  ws.send(JSON.stringify(payload));
}

function sendAgentStart() {
  if (!connected) {
    console.error('Gateway 未连接');
    return;
  }
  const id = nextId();
  const payload = {
    type: 'req',
    id,
    method: 'agent.start',
    params: {
      sessionKey: 'main',
      message: { role: 'user', content: '这是一条来自桥接测试的消息' }
    }
  };
  console.log('→ agent.start');
  ws.send(JSON.stringify(payload));
}

ws.on('error', (e) => console.error('WebSocket 错误:', e.message));
ws.on('close', () => console.log('连接关闭'));

setTimeout(() => {
  console.log('\n⏰ 超时退出（20秒）');
  ws.close();
  process.exit(0);
}, 20000);
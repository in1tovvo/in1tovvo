/**
 * OpenClaw QQ 桥接服务 - 使用子进程调用 openclaw agent 命令
 *
 * 这种方法避免了实现复杂的 WebSocket 协议和 device identity
 * 直接通过 CLI 与 OpenClaw 交互，简单可靠。
 */

import { spawn } from 'child_process';
import fetch from 'node-fetch';
import { URL } from 'url';

// 配置
const QQ_WS_URL = process.env.QQ_WS_URL || 'ws://127.0.0.1:5701';
const QQ_HTTP_URL = process.env.QQ_HTTP_URL || 'http://127.0.0.1:5700';

// go-cqhttp WebSocket 客户端
let qqWs = null;

// 主会话 ID（通过 openclaw sessions --json 获取）
let MAIN_SESSION_ID = null;

// ============ 获取主会话 ID ============
async function getMainSessionId() {
  try {
    const result = await execOpenClaw(['sessions', '--json']);
    const parsed = JSON.parse(result);
    if (parsed.sessions && parsed.sessions.length > 0) {
      return parsed.sessions[0].sessionId;
    }
  } catch (err) {
    console.error('获取会话列表失败:', err.message);
  }
  return null;
}

// ============ 执行 openclaw 命令 ============
function execOpenClaw(args) {
  return new Promise((resolve, reject) => {
    const proc = spawn('openclaw', args, {
      stdio: ['ignore', 'pipe', 'pipe'],
      env: { ...process.env }
    });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', (data) => { stdout += data.toString(); });
    proc.stderr.on('data', (data) => { stderr += data.toString(); });

    proc.on('close', (code) => {
      if (code === 0) {
        resolve(stdout.trim());
      } else {
        reject(new Error(`openclaw 退出码 ${code}: ${stderr.trim()}`));
      }
    });

    proc.on('error', (err) => reject(err));
  });
}

// ============ 通过 openclaw agent 发送消息 ============
async function sendToOpenClaw(userMessage) {
  if (!MAIN_SESSION_ID) {
    MAIN_SESSION_ID = await getMainSessionId();
    if (!MAIN_SESSION_ID) throw new Error('无法获取主会话 ID');
  }

  try {
    // 这里我们使用 openclaw agent 命令，但需要等待结果
    // 由于要实时等待，我们可以用管道方式，但最简单是调用 agent 并等待输出
    const result = await execOpenClaw([
      'agent',
      '--session-id', MAIN_SESSION_ID,
      '--message', userMessage,
      '--thinking', 'off',
      '--json'
    ]);

    const parsed = JSON.parse(result);
    // agent 命令的输出格式需要确认，通常包含 reply 或 result 字段
    // 这里我们简单返回 stdout
    return parsed;
  } catch (err) {
    console.error('agent 调用失败:', err.message);
    // 失败时，尝试重新获取会话 ID 再试一次
    MAIN_SESSION_ID = null;
    throw err;
  }
}

// ============ QQ 连接 ============
function connectQQ() {
  console.log(`🔗 连接 go-cqhttp: ${QQ_WS_URL}`);
  qqWs = new (require('ws'))(QQ_WS_URL);

  qqWs.on('open', () => {
    console.log('✅ QQ WebSocket 已连接');
  });

  qqWs.on('message', async (raw) => {
    try {
      const data = JSON.parse(raw);
      if (data.post_type !== 'message') return;

      const userId = data.user_id;
      const message = data.raw_message;
      const messageType = data.message_type;
      const isGroup = messageType === 'group';
      const chatId = isGroup ? data.group_id : userId;

      console.log(`📩 QQ ${isGroup ? '群' : '私聊'} [${userId}]: ${message.substring(0, 50)}`);

      // 转发到 OpenClaw
      try {
        const result = await sendToOpenClaw(message);
        console.log('✅ OpenClaw 已处理');
        
        // 提取回复文本
        let replyText = '';
        if (typeof result === 'string') {
          replyText = result;
        } else if (result?.message) {
          replyText = result.message;
        } else if (result?.text) {
          replyText = result.text;
        } else {
          replyText = '（空回复）';
        }

        // 发送回 QQ
        await sendQQText(data, replyText);
      } catch (err) {
        console.error('处理失败:', err.message);
        // 可选：发送错误提示给 QQ
        await sendQQText(data, '抱歉，处理您的消息时出错了。');
      }
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
🚀 OpenClaw QQ 桥接服务（子进程模式）
   QQ: ${QQ_WS_URL} → ${QQ_HTTP_URL}
`);

connectQQ();

// 优雅退出
process.on('SIGINT', () => {
  console.log('\n👋 正在退出...');
  if (qqWs) qqWs.close();
  process.exit(0);
});
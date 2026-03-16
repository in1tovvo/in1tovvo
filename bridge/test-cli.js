import { exec } from 'child_process';
import { promisify } from 'util';
const execAsync = promisify(exec);

async function test() {
  try {
    const { stdout } = await execAsync('openclaw sessions --json');
    const parsed = JSON.parse(stdout);
    console.log('Sessions:', JSON.stringify(parsed, null, 2));
    
    if (parsed.sessions && parsed.sessions.length > 0) {
      const sessionId = parsed.sessions[0].sessionId;
      console.log('使用会话 ID:', sessionId);
      
      const result = await execAsync(`openclaw agent --session-id ${sessionId} --message "桥接 CLI 测试" --json`);
      console.log('Agent 输出:', result.stdout.substring(0, 500));
    }
  } catch (err) {
    console.error('错误:', err.message);
  }
}

test();

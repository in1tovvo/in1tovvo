#!/usr/bin/env python3
import json
import sys
import shutil
from datetime import datetime

path = '/home/in1t/.openclaw/openclaw.json'
bak = f'{path}.bak-{int(datetime.now().timestamp())}'

try:
    # 备份
    shutil.copy2(path, bak)
    print(f'已备份: {bak}')

    # 读取
    with open(path, 'r') as f:
        config = json.load(f)

    # 添加 channels.feishu 配置
    config.setdefault('channels', {})['feishu'] = {
        "enabled": True,
        "appId": "YOUR_APP_ID_HERE",
        "appSecret": "YOUR_APP_SECRET_HERE",
        "encryptKey": "",
        "dmPolicy": "pairing",
        "groupPolicy": "allowlist",
        "mediaMaxMb": 10
    }

    # 写回（保持格式整洁）
    with open(path, 'w') as f:
        json.dump(config, f, indent=2)
        f.write('\n')  # 末尾换行

    print('✅ 已添加 Feishu 频道配置')
    print('📝 请编辑 ~/.openclaw/openclaw.json')
    print('   将 YOUR_APP_ID_HERE 和 YOUR_APP_SECRET_HERE 替换为真实凭据')
    print('⚠️  需要申请 feishu appSecret / appSecret')

except Exception as e:
    print(f'❌ 错误: {e}', file=sys.stderr)
    sys.exit(1)
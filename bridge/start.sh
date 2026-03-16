#!/bin/bash
# 启动 OpenClaw QQ 桥接服务

# 设置环境变量（根据实际情况修改）
export OPENCLAW_GATEWAY_TOKEN="af4f96126a8d2f0d5fc7c8bfc81fc087d58d6319f8c99a7f"
export OPENCLAW_GATEWAY_URL="http://127.0.0.1:18789"
export QQ_WS_URL="ws://127.0.0.1:5701"
export QQ_HTTP_URL="http://127.0.0.1:5700"

# 确保 node_modules 已安装
if [ ! -d "node_modules" ]; then
  echo "📦 安装依赖..."
  npm install
fi

# 启动桥接服务
echo "🚀 启动桥接服务..."
node bridge.js
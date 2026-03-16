#!/bin/bash
# Wedding Planner - 启动脚本
cd "$(dirname "$0")"

# 使用虚拟环境
if [ -d "venv" ]; then
    VENV_PYTHON="venv/bin/python"
    VENV_PIP="venv/bin/pip"
else
    VENV_PYTHON="python3"
    VENV_PIP="pip3"
fi

# 检查Python
if ! command -v $VENV_PYTHON &> /dev/null; then
    echo "❌ 需要安装 Python 3.8+"
    exit 1
fi

# 安装依赖（如果未安装）
$VENV_PIP install flask werkzeug --quiet

# 初始化数据库（首次运行）
if [ ! -f "data/wedding.db" ]; then
    echo "📦 初始化数据库..."
    $VENV_PYTHON app.py &
    PID=$!
    sleep 3
    kill $PID 2>/dev/null
    echo "✅ 数据库初始化完成"
fi

echo "🚀 启动 Wedding Planner..."
echo "📍 访问地址: http://localhost:5000"
echo "💡 提示: 首次使用请设置婚礼日期（可后续在仪表盘操作）"
echo ""
$VENV_PYTHON app.py

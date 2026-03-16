#!/bin/bash
# 使用国内镜像安装 go-cqhttp

set -e

ARCH="amd64"
if [ "$(uname -m)" = "aarch64" ] || [ "$(uname -m)" = "arm64" ]; then
  ARCH="arm64"
fi

echo "📦 架构: $ARCH"
echo "尝试从国内镜像下载..."
echo ""

# 国内镜像源（按优先级）
MIRRORS=(
  "https://github.com.cnpmjs.org/mrs4s/go-cqhttp/releases/latest/download/go-cqhttp-linux-${ARCH}.tar.gz"
  "https://mirror.ghproxy.com/https://github.com/Mrs4s/go-cqhttp/releases/latest/download/go-cqhttp-linux-${ARCH}.tar.gz"
  "https://github.com.mirror.sgl.hk/mrs4s/go-cqhttp/releases/latest/download/go-cqhttp-linux-${ARCH}.tar.gz"
  "https://raw.githubusercontent.com.cnpmjs.org/mrs4s/go-cqhttp/releases/latest/download/go-cqhttp-linux-${ARCH}.tar.gz"
  "https://gitclone.com/github.com/mirrors/go-cqhttp/releases/latest/download/go-cqhttp-linux-${ARCH}.tar.gz"
)

TMPDIR=$(mktemp -d)
cd "$TMPDIR"

for url in "${MIRRORS[@]}"; do
  echo "尝试: $url"
  # 检查链接是否可用
  if wget -q --spider --tries=1 --timeout=5 "$url" 2>/dev/null; then
    echo "✅ 链接有效，下载中..."
    if wget -q -O go-cqhttp.tar.gz "$url"; then
      echo "✅ 下载完成"
      break
    else
      echo "❌ 下载失败，继续下一个..."
      rm -f go-cqhttp.tar.gz
    fi
  else
    echo "❌ 链接无效"
  fi
done

if [ ! -f go-cqhttp.tar.gz ]; then
  echo ""
  echo "⚠️  所有镜像均失败"
  echo ""
  echo "请尝试以下方法："
  echo ""
  echo "1. 手动访问镜像站浏览器下载："
  echo "   https://github.com.cnpmjs.org/mrs4s/go-cqhttp/releases"
  echo "   或 https://gitee.com/mirrors/go-cqhttp/releases"
  echo ""
  echo "2. 使用代理（如果可用）："
  echo "   export https_proxy=http://127.0.0.1:7890"
  echo "   wget https://github.com/Mrs4s/go-cqhttp/releases/latest/download/go-cqhttp-linux-amd64.tar.gz"
  echo ""
  echo "3. 使用 Docker（如果以后安装 Docker）"
  echo ""
  exit 1
fi

# 解压
tar xzf go-cqhttp.tar.gz
if [ ! -f go-cqhttp ]; then
  echo "❌ 解压后未找到 go-cqhttp 可执行文件"
  ls -la
  exit 1
fi

# 安装
sudo mv go-cqhttp /usr/local/bin/
sudo chmod +x /usr/local/bin/go-cqhttp

echo ""
echo "✅ 安装成功！"
echo "  位置: /usr/local/bin/go-cqhttp"
echo "  版本: $(/usr/local/bin/go-cqhttp --version 2>&1 | head -1 || echo 'unknown')"
echo ""
echo "下一步："
echo "  mkdir -p ~/.config/go-cqhttp"
echo "  cp /home/in1t/.openclaw/workspace/bridge/config-template.yml ~/.config/go-cqhttp/config.yml"
echo "  # 编辑 config.yml，填写 QQ 号"
echo "  go-cqhttp  # 首次运行扫码登录"
echo ""

rm -rf "$TMPDIR"
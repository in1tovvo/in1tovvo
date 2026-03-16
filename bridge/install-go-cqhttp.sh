#!/bin/bash
# 安装 go-cqhttp - 多种方案尝试

set -e

ARCH="amd64"
if [ "$(uname -m)" = "aarch64" ] || [ "$(uname -m)" = "arm64" ]; then
  ARCH="arm64"
fi

echo "📦 架构: $ARCH"
echo ""

# 方案 1: 尝试从 GitHub 下载（支持代理）
echo "=== 方案 1: 从 GitHub 下载 ==="
URLS=(
  "https://github.com/Mrs4s/go-cqhttp/releases/latest/download/go-cqhttp-linux-${ARCH}.tar.gz"
  "https://ghproxy.com/https://github.com/Mrs4s/go-cqhttp/releases/latest/download/go-cqhttp-linux-${ARCH}.tar.gz"
  "https://mirror.ghproxy.com/https://github.com/Mrs4s/go-cqhttp/releases/latest/download/go-cqhttp-linux-${ARCH}.tar.gz"
  "https://download.fastgit.org/Mrs4s/go-cqhttp/releases/latest/download/go-cqhttp-linux-${ARCH}.tar.gz"
)

TMPDIR=$(mktemp -d)
cd "$TMPDIR"

for url in "${URLS[@]}"; do
  echo "尝试: $url"
  if wget -q --spider "$url" 2>/dev/null; then
    echo "✅ 链接有效，下载中..."
    wget -q -O go-cqhttp.tar.gz "$url" && break || echo "下载失败"
  fi
done

if [ -f go-cqhttp.tar.gz ]; then
  tar xzf go-cqhttp.tar.gz
  if [ -f go-cqhttp ]; then
    echo "✅ 下载并解压成功"
    sudo mv go-cqhttp /usr/local/bin/
    sudo chmod +x /usr/local/bin/go-cqhttp
    echo "✅ 已安装到 /usr/local/bin/go-cqhttp"
    rm -rf "$TMPDIR"
    exit 0
  fi
fi

echo ""
echo "⚠️  所有在线下载方案均失败"
echo ""
echo "请选择以下方案之一："
echo ""
echo "【方案 A】手动下载上传（推荐）"
echo "1. 在能上网的电脑访问："
echo "   https://github.com/Mrs4s/go-cqhttp/releases"
echo "2. 下载 go-cqhttp-linux-${ARCH}.tar.gz"
echo "3. 上传到本服务器，运行以下命令："
echo "   tar xzf go-cqhttp-linux-${ARCH}.tar.gz"
echo "   sudo mv go-cqhttp /usr/local/bin/"
echo "   sudo chmod +x /usr/local/bin/go-cqhttp"
echo ""
echo "【方案 B】使用 Docker（如果已安装 Docker）"
echo "docker run -d \\"
echo "  --name cqhttp \\"
echo "  -p 5700:5700 -p 5701:5701 \\"
echo "  -v ~/.local/share/go-cqhttp:/data \\"
echo "  -e UIN=你的QQ号 \\"
echo "  -e PASSWORD=\"\" \\"
echo "  --restart unless-stopped \\"
echo "  registry.cn-hangzhou.aliyuncs.com/go-cqhttp/go-cqhttp:latest"
echo ""
echo "【方案 C】从国内镜像站下载（如果可访问）"
echo "wget https://gitee.com/mirrors/go-cqhttp/releases/download/v1.0.0/go-cqhttp-linux-${ARCH}.tar.gz"
echo "（版本号需要替换为最新）"
echo ""
echo "一旦 go-cqhttp 安装完成，运行:"
echo "  mkdir -p ~/.config/go-cqhttp"
echo "  cp /home/in1t/.openclaw/workspace/bridge/config-template.yml ~/.config/go-cqhttp/config.yml"
echo "  # 编辑 config.yml，填写 QQ 号"
echo "  go-cqhttp  # 首次运行扫码登录"
echo ""

rm -rf "$TMPDIR"
exit 1
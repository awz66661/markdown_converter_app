#!/bin/bash

# Markdown 转换器快速部署脚本
#
# 使用方法:
#   chmod +x deploy.sh
#   ./deploy.sh

set -e

echo "🚀 开始部署 Markdown 转换器..."

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

echo "✅ Docker 环境检查通过"

# 停止现有服务
echo "🛑 停止现有服务..."
docker-compose down 2>/dev/null || true

# 清理旧镜像（可选）
read -p "是否清理旧的Docker镜像？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 清理旧镜像..."
    docker system prune -f
fi

# 构建和启动服务
echo "🔨 构建并启动服务..."
docker-compose up --build -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 检查服务状态..."
docker-compose ps

# 测试API连接
echo "🔍 测试API连接..."
if curl -s -f --noproxy localhost http://localhost:80/api/convert \
   -H "Content-Type: application/json" \
   -X POST \
   -d '{"markdown_text":"# 测试"}' > /dev/null; then
    echo "✅ API 测试通过"
else
    echo "❌ API 测试失败"
    echo "📋 查看日志:"
    docker-compose logs --tail=20
    exit 1
fi

# 获取服务器IP（如果是远程部署）
if [ -n "$SSH_CLIENT" ] || [ -n "$SSH_TTY" ]; then
    SERVER_IP=$(hostname -I | awk '{print $1}')
    echo ""
    echo "🎉 部署成功！"
    echo "📱 访问地址:"
    echo "   本地访问: http://localhost"
    echo "   远程访问: http://$SERVER_IP"
else
    echo ""
    echo "🎉 部署成功！"
    echo "📱 访问地址: http://localhost"
fi

echo ""
echo "📚 使用说明:"
echo "   - 查看服务状态: docker-compose ps"
echo "   - 查看日志: docker-compose logs -f"
echo "   - 停止服务: docker-compose down"
echo "   - 重启服务: docker-compose restart"
echo ""
echo "✨ 享受使用 Markdown 转换器！"
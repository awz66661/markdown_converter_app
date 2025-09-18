# Markdown 转换器部署教程

## 目录
- [系统要求](#系统要求)
- [本地开发部署](#本地开发部署)
- [生产环境部署](#生产环境部署)
- [服务器部署详细步骤](#服务器部署详细步骤)
- [域名配置](#域名配置)
- [SSL证书配置](#ssl证书配置)
- [维护和监控](#维护和监控)
- [故障排除](#故障排除)

## 系统要求

### 最低配置
- **CPU**: 1核心
- **内存**: 1GB RAM
- **存储**: 10GB 可用空间
- **网络**: 公网IP或域名（生产环境）

### 推荐配置
- **CPU**: 2核心或以上
- **内存**: 2GB RAM或以上
- **存储**: 20GB 可用空间或以上

### 软件要求
- Docker 20.10+
- Docker Compose 2.0+
- Git（用于代码部署）

## 本地开发部署

### 1. 克隆项目
```bash
git clone <your-repository-url>
cd markdown_converter_app
```

### 2. 构建和启动
```bash
# 构建并启动所有服务
docker-compose up --build -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 3. 访问应用
- 前端界面: http://localhost
- 后端API: http://localhost:5000

### 4. 停止服务
```bash
docker-compose down
```

## 生产环境部署

### 准备工作

1. **更新系统**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

2. **安装Docker**
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **验证安装**
```bash
docker --version
docker-compose --version
```

## 服务器部署详细步骤

### 步骤1: 上传代码

**方法1: 使用Git（推荐）**
```bash
# 在服务器上克隆项目
git clone <your-repository-url>
cd markdown_converter_app
```

**方法2: 直接上传**
```bash
# 使用scp上传项目文件
scp -r /local/path/markdown_converter_app user@server:/home/user/
```

### 步骤2: 配置环境变量（可选）

如果需要自定义配置，创建环境文件：
```bash
# 复制环境配置文件
cp .env.example .env

# 编辑配置
nano .env
```

### 步骤3: 构建和启动服务

```bash
# 确保在项目根目录
cd markdown_converter_app

# 拉取最新镜像并构建
docker-compose pull
docker-compose up --build -d

# 查看服务状态
docker-compose ps
```

### 步骤4: 验证部署

```bash
# 检查容器状态
docker ps

# 查看应用日志
docker-compose logs -f

# 测试API连接
curl -X POST http://localhost:80/api/convert \
  -H "Content-Type: application/json" \
  -d '{"markdown_text":"# 测试标题"}'
```

### 步骤5: 配置防火墙

```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --reload
```

## 域名配置

### 1. DNS设置
在您的域名提供商处添加A记录：
```
类型: A
名称: @ (或www)
值: 您的服务器IP地址
TTL: 300
```

### 2. 更新Nginx配置（如需要）
如果使用自定义域名，可能需要修改nginx配置：

创建 `nginx-custom.conf`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## SSL证书配置

### 使用Let's Encrypt免费证书

1. **安装Certbot**
```bash
# Ubuntu/Debian
sudo apt install certbot

# CentOS/RHEL
sudo yum install certbot
```

2. **获取证书**
```bash
# 停止现有服务
docker-compose down

# 获取证书
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

3. **配置HTTPS**
创建 `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    container_name: markdown-converter-backend
    networks:
      - app-network
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    container_name: markdown-converter-frontend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /etc/letsencrypt:/etc/letsencrypt:ro
      - ./nginx-ssl.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - backend
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
    driver: bridge
```

4. **启动HTTPS服务**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 维护和监控

### 日常维护命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 更新应用
git pull
docker-compose up --build -d

# 清理旧镜像
docker system prune -f
```

### 备份策略

1. **定期备份代码**
```bash
# 创建备份脚本
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_$DATE.tar.gz --exclude='.git' --exclude='node_modules' .
mv backup_$DATE.tar.gz /backup/
find /backup/ -name "backup_*.tar.gz" -mtime +7 -delete
EOF

chmod +x backup.sh
```

2. **设置定时任务**
```bash
# 添加到crontab
echo "0 2 * * * /path/to/backup.sh" | crontab -
```

### 监控脚本

创建简单的健康检查脚本：
```bash
cat > health_check.sh << 'EOF'
#!/bin/bash
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:80)
if [ $RESPONSE != 200 ]; then
    echo "$(date): Application is down, restarting..."
    docker-compose restart
    echo "$(date): Restart completed"
fi
EOF

chmod +x health_check.sh
```

## 故障排除

### 常见问题及解决方案

1. **容器无法启动**
```bash
# 查看详细错误信息
docker-compose logs [service-name]

# 检查端口占用
netstat -tlnp | grep :80
```

2. **API无法访问**
```bash
# 检查网络连接
docker network ls
docker network inspect markdown_converter_app_app-network

# 测试后端连接
docker exec -it markdown-converter-backend curl localhost:5000
```

3. **前端页面无法加载**
```bash
# 检查nginx配置
docker exec -it markdown-converter-frontend nginx -t

# 重新构建前端
docker-compose up --build frontend
```

4. **内存不足**
```bash
# 查看系统资源使用
free -h
df -h

# 清理Docker资源
docker system prune -a
```

5. **权限问题**
```bash
# 修复文件权限
sudo chown -R $USER:$USER .
chmod +x *.sh
```

### 性能优化

1. **启用nginx gzip压缩**
2. **配置适当的worker进程数**
3. **使用CDN加速静态资源**
4. **启用HTTP/2**

### 安全建议

1. **定期更新系统和依赖**
2. **使用非root用户运行服务**
3. **配置fail2ban防护**
4. **限制不必要的端口访问**
5. **定期检查日志异常**

## 生产环境检查清单

部署前确认：
- [ ] 服务器满足最低配置要求
- [ ] Docker和Docker Compose已正确安装
- [ ] 防火墙已配置允许HTTP/HTTPS端口
- [ ] 域名DNS已正确配置
- [ ] SSL证书已配置（如需要）
- [ ] 备份策略已建立
- [ ] 监控脚本已配置

部署后验证：
- [ ] 所有容器正常运行
- [ ] 前端页面可正常访问
- [ ] API接口响应正常
- [ ] 文件上传功能正常
- [ ] 转换功能正常工作
- [ ] 错误处理正常
- [ ] 日志记录正常

---

如有任何问题，请查看项目README文件或检查应用日志获取更多信息。
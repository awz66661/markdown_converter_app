# 📝 Markdown 转换器

> 一个专为博客内容创作设计的Markdown格式转换工具，将AI生成的Markdown文档转换为适合博客系统使用的格式。

![应用预览](https://img.shields.io/badge/Status-Production%20Ready-brightgreen) ![Docker](https://img.shields.io/badge/Docker-Supported-blue) ![Vue.js](https://img.shields.io/badge/Vue.js-3.2-green) ![Python](https://img.shields.io/badge/Python-3.9-blue)

## ✨ 功能特性

- 🎯 **专业转换**: 将Markdown格式精确转换为博客系统特定格式
- 📁 **拖拽上传**: 支持直接拖拽.md文件进行转换
- ⚡ **实时转换**: 输入即时转换，所见即所得
- 📋 **一键复制**: 转换结果一键复制到剪贴板
- 📱 **响应式设计**: 完美支持桌面和移动设备
- 🐳 **Docker部署**: 一键部署，开箱即用
- 🔧 **现代技术栈**: Vue.js 3 + Flask + Docker

## 🎮 在线演示

访问 [你的域名](https://awz66661.top) 体验在线版本

## 📖 转换规则

| Markdown语法 | 转换结果 | 说明 |
|--------------|----------|------|
| `# 标题` | `[h1]标题[/h1]` | 一级标题 |
| `## 标题` | `[h2]标题[/h2]` | 二级标题 |
| `### 标题` | `[h3]标题[/h3]` | 三级标题 |
| `####+ 标题` | `标题` | 四级及以上标题转为普通文本 |
| `**加粗**` | `<strong>加粗</strong>` | 粗体文本 |
| `*斜体*` | `<em>斜体</em>` | 斜体文本 |
| `- 列表项` | `<ul><li>列表项</li></ul>` | 无序列表 |
| `1. 列表项` | `<ol><li>列表项</li></ol>` | 有序列表 |
| 表格语法 | `<table><tr><td>...</td></tr></table>` | 表格转换 |

## 🚀 快速开始

### 方法1: Docker部署（推荐）

确保已安装 Docker 和 Docker Compose，然后执行：

```bash
# 克隆项目
git clone <your-repository-url>
cd markdown_converter_app

# 一键启动
docker-compose up -d

# 访问应用
open http://localhost
```

### 方法2: 本地开发

**后端启动**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**前端启动**
```bash
cd frontend
npm install
npm run dev
```

## 📁 项目结构

```
markdown_converter_app/
├── 📁 backend/              # Flask后端服务
│   ├── 🐍 app.py            # 主应用文件
│   ├── 📝 requirements.txt  # Python依赖
│   └── 🐳 Dockerfile        # 后端Docker配置
├── 📁 frontend/             # Vue.js前端应用
│   ├── 📁 src/              # 源代码目录
│   │   ├── 🎨 App.vue       # 主组件
│   │   └── 🚀 main.js       # 应用入口
│   ├── 📝 package.json      # 前端依赖
│   ├── ⚙️ vite.config.js   # Vite配置
│   └── 🐳 Dockerfile        # 前端Docker配置
├── 🐳 docker-compose.yml    # 容器编排配置
├── 📖 README.md             # 项目文档
├── 🚀 DEPLOYMENT.md         # 部署教程
└── 🚫 .gitignore            # Git忽略规则
```

## 🛠️ 技术栈

### 后端技术
- **框架**: Flask 2.0.1
- **跨域**: Flask-Cors 3.0.10
- **文本处理**: 自定义Markdown解析器
- **运行环境**: Python 3.9

### 前端技术
- **框架**: Vue.js 3.2
- **构建工具**: Vite 2.5
- **样式**: 原生CSS3 + 现代设计
- **HTTP客户端**: Fetch API

### 部署技术
- **容器化**: Docker + Docker Compose
- **Web服务器**: Nginx (前端静态文件服务)
- **反向代理**: 内置API代理配置

## 📦 部署指南

### 生产环境部署

详细的部署教程请参考 [DEPLOYMENT.md](./DEPLOYMENT.md)

**快速部署命令**:
```bash
# 1. 克隆项目
git clone <your-repository-url>
cd markdown_converter_app

# 2. 启动服务
docker-compose up --build -d

# 3. 检查状态
docker-compose ps
docker-compose logs -f
```

### 环境配置

**端口配置**:
- 前端服务: `80` (可在docker-compose.yml中修改)
- 后端API: `5000` (容器内部)

**自定义端口**:
```yaml
# docker-compose.yml
services:
  frontend:
    ports:
      - "8080:80"  # 修改为自定义端口
```

## 🔧 开发指南

### 本地开发环境

1. **安装依赖**
```bash
# 后端依赖
cd backend && pip install -r requirements.txt

# 前端依赖
cd frontend && npm install
```

2. **启动开发服务**
```bash
# 后端开发服务 (端口5000)
cd backend && python app.py

# 前端开发服务 (端口3000)
cd frontend && npm run dev
```

3. **代码规范**
- 后端: 遵循PEP 8规范
- 前端: 使用Vue.js 3组合式API
- 提交: 使用语义化提交信息

### API接口

**转换接口**
```http
POST /api/convert
Content-Type: application/json

{
  "markdown_text": "# 示例标题\n**粗体文本**"
}
```

**响应格式**
```json
{
  "converted_text": "[h1]示例标题[/h1]\n<strong>粗体文本</strong>"
}
```

## 🐛 故障排除

### 常见问题

**1. 端口被占用**
```bash
# 查看端口使用情况
netstat -tlnp | grep :80

# 修改docker-compose.yml中的端口映射
ports:
  - "8080:80"
```

**2. 容器启动失败**
```bash
# 查看容器日志
docker-compose logs [service-name]

# 重新构建
docker-compose up --build --force-recreate
```

**3. API请求失败**
```bash
# 检查后端服务状态
curl http://localhost:5000/convert

# 检查网络连接
docker network inspect markdown_converter_app_app-network
```

**4. 前端页面空白**
- 检查浏览器控制台错误信息
- 确认静态文件正确构建
- 验证nginx配置

### 日志查看

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f frontend
docker-compose logs -f backend
```

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork本项目
2. 创建feature分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

### 开发规范

- 代码风格: 遵循项目现有风格
- 提交信息: 使用清晰的描述性信息
- 测试: 确保新功能有相应测试
- 文档: 更新相关文档

## 📄 开源协议

本项目采用 MIT 协议 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [Flask](https://flask.palletsprojects.com/) - 轻量级Python Web框架
- [Docker](https://www.docker.com/) - 容器化平台
- [Vite](https://vitejs.dev/) - 下一代前端构建工具

## 📧 联系方式

- 作者: [您的名字]
- 邮箱: [您的邮箱]
- 博客: [https://awz66661.top](https://awz66661.top)
- 项目地址: [GitHub仓库链接]

## 🔄 更新日志

### v1.0.0 (2025-09-18)
- ✨ 首次发布
- 🎯 完整的Markdown转换功能
- 🐳 Docker化部署支持
- 📱 响应式用户界面
- ⚡ 实时转换功能

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请考虑给它一个Star！**

Made with ❤️ by [您的名字]

</div>
# Markdown Converter App

这是一个将 Markdown 格式文本转换为特定格式的 Web 应用程序。该应用专门用于将 AI 生成的 Markdown 内容转换为适合博客系统使用的格式。应用程序使用 Vue.js 作为前端，Flask 作为后端，并通过 Docker 进行部署。

## 应用场景

这个工具专门用于我的博客内容![我的博客](awz66661.top)创作，可以将 AI 生成的 Markdown 文档转换为符合博客系统要求的格式，方便直接粘贴到博客编辑器中。

## 功能特性

- 拖拽上传 Markdown 文件
- 实时转换 Markdown 为博客格式
- 一键复制转换后的文本
- 响应式设计，支持移动端

## 转换规则

- `# 标题` → `[h1]标题[/h1]`
- `## 标题` → `[h2]标题[/h2]`
- `### 标题` → `[h3]标题[/h3]`
- `####及以上标题` → 去除#后作为文本
- `**加粗**` → `<strong>加粗</strong>`
- `*斜体*` → `<em>斜体</em>`
- 无序列表 (- 或 * 开头) → `<ul>`和`<li>`标签
- 有序列表 (数字. 开头) → `<ol>`和`<li>`标签
- 表格 → `<table>`和`<tr><td>`标签

## 项目结构

```
markdown_converter_app/
├── backend/                  # 后端 Flask 应用
│   ├── app.py                # Flask 应用和转换逻辑
│   ├── requirements.txt      # Python 依赖
│   └── Dockerfile            # 后端服务的 Dockerfile
│
├── frontend/                 # 前端 Vue.js 应用
│   ├── src/                  # Vue 组件和逻辑
│   ├── public/
│   ├── Dockerfile            # 前端服务的 Dockerfile
│   ├── package.json
│   └── .env                  # 环境变量
│
├── nginx/                    # Nginx 配置
│   └── nginx.conf            # Nginx 配置文件
│
├── docker-compose.yml        # Docker 服务编排
├── .gitignore                # Git 忽略文件
└── README.md                 # 项目说明文档
```


## 本地开发

### 启动后端服务

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端服务将在 `http://localhost:5000` 上运行。

### 启动前端服务

```bash
cd frontend
npm install
npm run dev
```

前端服务将在 `http://localhost:3000` 上运行。

## Docker 部署

### 构建和运行

```bash
docker-compose up --build -d
```

应用将在 `http://localhost` 上运行。

### 停止服务

```bash
docker-compose down
```

## 部署到服务器

1. 将整个项目文件夹上传到服务器
2. 在服务器上运行 `docker-compose up --build -d`
3. 确保服务器防火墙允许 80 端口的流量

## 环境变量

### 前端

- `VITE_BACKEND_API_URL` - 后端 API 地址，默认为 `/api`

## 依赖说明

### 后端依赖

- Flask==2.0.1
- Flask-Cors==3.0.10
- markdown2==2.4.3
- Werkzeug==2.0.3

### 前端依赖

- vue: ^3.2.0
- @vitejs/plugin-vue: ^1.6.0
- @vue/compiler-sfc: ^3.2.0
- vite: ^2.5.0

## 故障排除

### 转换失败

如果遇到"转换失败，请检查后端服务是否运行正常"的错误：

1. 检查后端服务是否正常运行：`docker-compose logs backend`
2. 检查 Nginx 配置是否正确代理请求：`docker-compose logs nginx`
3. 确认前端环境变量配置正确

### 端口冲突

如果 80 端口已被占用，可以修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "8080:80"  # 将 8080 替换为你想要的端口
```
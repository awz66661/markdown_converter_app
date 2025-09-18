# frontend/Dockerfile
# 阶段一：构建前端应用
FROM docker.1ms.run/node:20-alpine AS build-stage

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/. .

# 使用生产环境变量构建
RUN npm run build

# 阶段二：使用 Nginx 托管静态文件
FROM docker.1ms.run/nginx:alpine AS production-stage

# 从构建阶段拷贝前端的构建结果到 Nginx 的静态文件目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 复制自定义的 Nginx 配置
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
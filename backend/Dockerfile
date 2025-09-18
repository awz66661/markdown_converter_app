# Dockerfile.backend
FROM docker.1ms.run/python:3.9-slim-buster

# 配置 pip 使用国内镜像源
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app.py .

EXPOSE 5000

CMD ["python", "app.py"]
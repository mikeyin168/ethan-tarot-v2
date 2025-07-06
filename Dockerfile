FROM python:3.10-slim

# 補全 WeasyPrint 所有系統相依套件
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libssl-dev \
    libglib2.0-0 \
    libxml2 \
    libxslt1.1 \
    fonts-liberation \
    fonts-dejavu \
    fonts-noto-core \
    fonts-noto-cjk \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 建立工作資料夾
WORKDIR /app
COPY . /app

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 啟動主程式
CMD ["python", "main.py"]
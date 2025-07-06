FROM python:3.10-slim

# 安裝 WeasyPrint 所需的完整系統套件（含 libpangocairo）
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
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

# 設定工作目錄
WORKDIR /app
COPY . /app

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 啟動 Flask 主程式
CMD ["python", "main.py"]
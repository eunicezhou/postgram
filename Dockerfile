# 使用官方 python 3.11.3 鏡像作為基本映像，指定版本
FROM python:3.11.3

# 設定工作目錄，所有複製後的文件會在此資料夾下
WORKDIR /app

# 複製 package.json 與 package-lock.json 到容器中
COPY module_require.txt .
COPY .env .

# 安裝應用程式相依套件
RUN pip install -r module_require.txt

# 複製應用程式程式碼到容器中，複製全部程式碼
COPY . .

# 應用程式執行的預設指令
CMD ["python", "app.py"]
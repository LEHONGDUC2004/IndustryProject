# Sử dụng một base image của Python
FROM python:3.11-slim


# Đặt thư mục làm việc bên trong container
WORKDIR /app

# Copy file requirements vào trước để tận dụng cache
COPY requirements.txt .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# --- ✅ THÊM DÒNG NÀY ĐỂ CÀI ĐẶT GIT ---
RUN apt-get update && apt-get install -y git

# Copy toàn bộ code của ứng dụng vào
COPY . .

# Mở port 5000 để bên ngoài có thể truy cập
EXPOSE 5000

# Lệnh để chạy ứng dụng khi container khởi động
CMD ["python", "app.py"]

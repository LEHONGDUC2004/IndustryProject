# Sử dụng một base image của Python
FROM python:3.11-slim

# Đặt các biến môi trường để tránh các câu hỏi tương tác khi cài đặt
ENV DEBIAN_FRONTEND=noninteractive

# Cài đặt các công cụ cần thiết: git và openssh-client
RUN apt-get update && apt-get install -y git openssh-client

# Tạo một user riêng tên là 'appuser' để chạy ứng dụng (bảo mật hơn)
RUN useradd --create-home --shell /bin/bash appuser

# Chuyển sang làm việc với user 'appuser'
USER appuser
WORKDIR /home/appuser/app

# Copy file requirements vào trước để tận dụng cache
# --chown để đảm bảo file thuộc về user 'appuser'
COPY --chown=appuser:appuser requirements.txt .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code của ứng dụng vào
COPY --chown=appuser:appuser . .

# Mở port 5000 để bên ngoài có thể truy cập
EXPOSE 5000

# Lệnh để chạy ứng dụng khi container khởi động
CMD ["python", "app.py"]

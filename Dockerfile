# Sử dụng một base image của Python, loại slim để nhẹ hơn
FROM python:3.11-slim

# Đặt biến môi trường để các lệnh cài đặt không hỏi tương tác
ENV DEBIAN_FRONTEND=noninteractive

# --- BƯỚC 1: CÀI ĐẶT CÔNG CỤ VÀ CẤU HÌNH SSH ---
# Cài đặt git và openssh-client
RUN apt-get update && apt-get install -y git openssh-client

# Tạo một user không phải root để chạy ứng dụng (bảo mật hơn)
RUN useradd --create-home --shell /bin/bash appuser

# Chuyển sang user mới
USER appuser

# Tự động thêm public key của github.com vào danh sách host đáng tin cậy
# Đây là bước mấu chốt để sửa lỗi "Host key verification failed"
RUN mkdir -p /home/appuser/.ssh
RUN ssh-keyscan github.com >> /home/appuser/.ssh/known_hosts
RUN chmod 600 /home/appuser/.ssh/known_hosts

# --- BƯỚC 2: CÀI ĐẶT ỨNG DỤNG PYTHON ---
# Đặt thư mục làm việc
WORKDIR /home/appuser/app

# Copy và cài đặt các thư viện Python
# --chown để đảm bảo file thuộc về user 'appuser'
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code của ứng dụng vào
COPY --chown=appuser:appuser . .

# Mở port 5000 để bên ngoài có thể truy cập
EXPOSE 5000

# Lệnh để chạy ứng dụng khi container khởi động
CMD ["python", "app.py"]

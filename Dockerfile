FROM python:3.11-slim

# Đặt biến môi trường để các lệnh cài đặt không hỏi tương tác
ENV DEBIAN_FRONTEND=noninteractive

# Cài đặt git và openssh-client
RUN apt-get update && apt-get install -y git openssh-client

# Tạo 1 user không phải root để chạy ứng dụng
RUN useradd --create-home --shell /bin/bash appuser

# Chuyển sang user mới
USER appuser

# Tự động thêm public key của github.com vào danh sách host đáng tin cậy
# Đây là bước mấu chốt để sửa lỗi "Host key verification failed"
RUN mkdir -p /home/appuser/.ssh
RUN ssh-keyscan github.com >> /home/appuser/.ssh/known_hosts
RUN chmod 600 /home/appuser/.ssh/known_hosts

# Đặt thư mục làm việc
WORKDIR /home/appuser/app

# Copy và cài đặt các thư viện Python
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code của ứng dụng vào
COPY --chown=appuser:appuser . .

# Mở port 5000 để truy cập website local
EXPOSE 5000

# Lệnh để chạy ứng dụng
CMD ["python", "run.py"]
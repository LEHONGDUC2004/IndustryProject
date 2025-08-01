# IndustryProject - Automatic Deployment Platform
# Nền tảng triển khai tự động

## Overview / Tổng quan

This is a Flask web application that automates the deployment of other applications. Users can upload their source code (ZIP) and database (SQL) files, and the system will automatically process them, create Docker configurations, and trigger deployment through Jenkins.

Đây là ứng dụng web Flask tự động hóa việc triển khai các ứng dụng khác. Người dùng có thể tải lên mã nguồn (ZIP) và file cơ sở dữ liệu (SQL), hệ thống sẽ tự động xử lý, tạo cấu hình Docker và kích hoạt triển khai qua Jenkins.

## Features / Tính năng

- 🚀 **Automatic Application Deployment** / Triển khai ứng dụng tự động
- 📦 **Source Code Processing** / Xử lý mã nguồn
- 🗄️ **Database Setup** / Thiết lập cơ sở dữ liệu  
- 🐳 **Docker Configuration Generation** / Tạo cấu hình Docker
- 🔄 **Jenkins Integration** / Tích hợp Jenkins
- 🌐 **Vietnamese UI** / Giao diện tiếng Việt

## Development Setup / Thiết lập phát triển

### Quick Start / Bắt đầu nhanh

```bash
# Clone the repository / Clone repository
git clone <repository-url>
cd IndustryProject

# Run setup script / Chạy script thiết lập
./setup_dev.sh

# Start the application / Khởi động ứng dụng
python run.py
```

### Manual Setup / Thiết lập thủ công

```bash
# Install dependencies / Cài đặt dependencies
pip install -r requirements.txt

# Create local directories / Tạo thư mục local
mkdir -p local_data/uploaded local_data/extracted local_data/replaced

# Set development environment / Thiết lập môi trường phát triển
export FLASK_ENV=development

# Run the application / Chạy ứng dụng
python run.py
```

## Production Deployment / Triển khai production

For production, use Docker Compose:

```bash
docker-compose up -d
```

The application will use MySQL in production and SQLite in development.

## Application Structure / Cấu trúc ứng dụng

- `app/` - Main application code / Mã nguồn chính
- `app/routes/` - URL routes / Định tuyến URL
- `app/controller/` - Business logic / Logic nghiệp vụ
- `app/templates/` - HTML templates / Template HTML
- `app/static/` - Static files / File tĩnh
- `local_data/` - Development data directory / Thư mục dữ liệu phát triển

## Usage / Cách sử dụng

1. Access the application at http://localhost:5000
2. Upload your ZIP source code file
3. Upload your SQL database file  
4. Fill in database configuration
5. Click "Tải Lên và Triển Khai" to deploy

Visit http://localhost:5000 to see the deployment interface.
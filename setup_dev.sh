#!/bin/bash
# Development setup script for the deployment application
# Thiết lập môi trường phát triển cho ứng dụng triển khai

echo "Setting up development environment..."
echo "Thiết lập môi trường phát triển..."

# Create local data directories
mkdir -p local_data/uploaded
mkdir -p local_data/extracted  
mkdir -p local_data/replaced

# Set development environment
export FLASK_ENV=development

# Install dependencies
pip install -r requirements.txt

echo "Setup complete! Run 'python run.py' to start the application."
echo "Thiết lập hoàn thành! Chạy 'python run.py' để khởi động ứng dụng."
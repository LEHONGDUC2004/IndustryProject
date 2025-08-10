#!/bin/bash

set -e  # Dừng script nếu có lỗi
S3_KEY=$1  # Nhận tên file từ Jenkins

PROJECT_NAME=$(basename "$S3_KEY" .zip)

echo " Deploying project: $PROJECT_NAME from $S3_KEY"

# Dọn thư mục cũ (optional)
rm -rf /home/ubuntu/$PROJECT_NAME
mkdir -p /home/ubuntu/$PROJECT_NAME

# Tải file từ S3
aws s3 cp s3://your-bucket/$S3_KEY /home/ubuntu/$PROJECT_NAME.zip

# Giải nén
unzip /home/ubuntu/$PROJECT_NAME.zip -d /home/ubuntu/$PROJECT_NAME

# Build & run Docker (nếu là app Python/Django/Flask...)
cd /home/ubuntu/$PROJECT_NAME

# Nếu có Dockerfile
if [ -f Dockerfile ]; then
  docker build -t $PROJECT_NAME .
  docker stop $PROJECT_NAME || true
  docker rm $PROJECT_NAME || true
  docker run -d --name $PROJECT_NAME -p 80:80 $PROJECT_NAME
else
  echo " No Dockerfile found. Skipping docker build"
fi
echo "" Deploy completed for $PROJECT_NAME"

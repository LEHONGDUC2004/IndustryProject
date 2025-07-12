// Jenkinsfile
// File này sẽ ra lệnh cho Jenkins build Docker image và deploy lên VM2

pipeline {
    // Chỉ định nơi pipeline sẽ chạy, 'any' nghĩa là bất kỳ agent nào có sẵn
    agent any

    // Định nghĩa các biến môi trường để dễ quản lý
    environment {
        // Tên Docker image bạn muốn tạo. Thay 'your-dockerhub-username' bằng tên user của bạn trên Docker Hub
        DOCKER_IMAGE_NAME = "lehongduc3491/industry-project"
        // ID của credentials đã lưu trên Jenkins để đăng nhập Docker Hub
        DOCKER_HUB_CREDENTIALS_ID = "ockerhub-credentials"
        // Tên của SSH server đã cấu hình trong Jenkins để kết nối tới VM2
        VM2_SSH_SERVER_NAME = "vm2-ssh"
    }

    // Các giai đoạn (stages) của pipeline
    stages {
        // Giai đoạn 1: Lấy code từ Git
        stage('Checkout Code') {
            steps {
                echo 'Pulling code from Git repository...'
                // Jenkins sẽ tự động checkout nhánh đã kích hoạt pipeline (ví dụ: upload/...)
                checkout scm
            }
        }

        // Giai đoạn 2: Build Docker image
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${DOCKER_IMAGE_NAME}:${env.BUILD_ID}"
                    // Dùng Dockerfile có sẵn trong code để build image
                    // Gắn tag cho image với Build ID để có phiên bản duy nhất
                    def customImage = docker.build(DOCKER_IMAGE_NAME, "--tag ${DOCKER_IMAGE_NAME}:${env.BUILD_ID} .")
                }
            }
        }

        // Giai đoạn 3: Đẩy image lên Docker Hub (Nơi lưu trữ image)
        stage('Push to Docker Registry') {
            steps {
                script {
                    echo "Pushing image ${DOCKER_IMAGE_NAME}:${env.BUILD_ID} to Docker Hub..."
                    // Dùng credentials đã lưu trong Jenkins để đăng nhập và đẩy image
                    docker.withRegistry('https://registry.hub.docker.com', DOCKER_HUB_CREDENTIALS_ID) {
                        docker.image("${DOCKER_IMAGE_NAME}:${env.BUILD_ID}").push()
                    }
                }
            }
        }
        
        // Giai đoạn 4: Deploy ứng dụng lên VM2
        stage('Deploy to VM2') {
            steps {
                echo "Deploying new version to VM2..."
                // Dùng plugin Publish over SSH để kết nối và ra lệnh cho VM2
                sshPublisher(
                    publishers: [
                        sshPublisherDesc(
                            configName: VM2_SSH_SERVER_NAME,
                            // Ra lệnh cho VM2
                            command: """
                                # Dừng và xóa container cũ nếu có
                                docker stop industry-app || true
                                docker rm industry-app || true

                                # Kéo image mới nhất từ Docker Hub
                                docker pull ${DOCKER_IMAGE_NAME}:${env.BUILD_ID}

                                # Chạy container mới từ image vừa kéo
                                docker run -d --name industry-app -p 80:5000 ${DOCKER_IMAGE_NAME}:${env.BUILD_ID}
                            """
                        )
                    ]
                )
            }
        }
    }

    // Các hành động sẽ thực hiện sau khi pipeline kết thúc (dù thành công hay thất bại)
    post {
        always {
            echo 'Pipeline finished.'
            // Dọn dẹp workspace để tiết kiệm dung lượng
            cleanWs()
        }
    }
}

import os


def create_setup(setup_path):
        compose_path = os.path.join(setup_path, 'vm_setup.sh')

        with open(compose_path, 'w') as f:
            f.write("""
            #!/bin/bash

# Nội dung này sẽ được Jenkins gửi qua SSH (plink) sang máy VM2 để cài docker-compose nếu chưa có

if ! command -v docker-compose >/dev/null 2>&1; then
    echo "[INFO] docker-compose not found. Installing..."
    curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m) -o ~/docker-compose
    chmod +x ~/docker-compose
    echo 'export PATH=$HOME:$PATH' >> ~/.bashrc
    export PATH=$HOME:$PATH
else
    echo "[INFO] docker-compose already installed."
fi
            """)

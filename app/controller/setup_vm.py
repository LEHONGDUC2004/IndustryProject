import os


def create_setup(setup_path):
        compose_path = os.path.join(setup_path, 'vm_setup.sh')

        with open(compose_path, 'w') as f:
            f.write("""
            #!/bin/bash

echo "[INFO] Checking docker..."
if ! command -v docker >/dev/null 2>&1; then
    echo "[INFO] Installing Docker..."
    sudo apt update
    sudo apt install -y docker.io
fi

echo "[INFO] Checking docker-compose..."
if ! command -v docker-compose >/dev/null 2>&1; then
    echo "[INFO] Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
fi

# Test xem docker-compose đã sẵn sàng chưa
if docker-compose --version >/dev/null 2>&1; then
    echo "[✔] docker-compose ready"
else
    echo "[❌] docker-compose failed"
    exit 1
fi
            """)

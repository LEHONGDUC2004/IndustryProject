import os


def create_setup(setup_path):
        compose_path = os.path.join(setup_path, 'vm_setup.sh')

        with open(compose_path, 'w') as f:
            f.write("""
            #!/bin/bash
set -e

echo "[+] Đang kiểm tra Docker..."

if ! command -v docker &> /dev/null; then
    echo "[+] Cài đặt Docker..."
    curl -fsSL https://get.docker.com | bash
    sudo usermod -aG docker "$USER"
    echo "[+] Docker đã được cài đặt."
else
    echo "[=] Docker đã có sẵn."
fi

echo "[+] Đang kiểm tra Docker Compose..."

if ! command -v docker-compose &> /dev/null; then
    echo "[+] Cài đặt Docker Compose..."
    mkdir -p ~/.local/bin
    curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m) \
        -o ~/.local/bin/docker-compose
    chmod +x ~/.local/bin/docker-compose
    echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
    export PATH=$HOME/.local/bin:$PATH
    echo "[+] Docker Compose đã được cài đặt."
else
    echo "[=] Docker Compose đã có sẵn."
fi
            """)

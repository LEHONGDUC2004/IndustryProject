FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y git openssh-client

RUN useradd --create-home --shell /bin/bash appuser
USER appuser

RUN mkdir -p /home/appuser/.ssh
RUN ssh-keyscan github.com >> /home/appuser/.ssh/known_hosts
RUN chmod 600 /home/appuser/.ssh/known_hosts

WORKDIR /home/appuser/app

COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

# 💡 Thêm script chờ DB vào container
COPY --chown=appuser:appuser wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

EXPOSE 5000

# ❗ Dùng wait-for-it để đợi MySQL ở 'db:3306' sẵn sàng
CMD ["/wait-for-it.sh", "db:3306", "--timeout=30", "--strict", "--", "python", "run.py"]

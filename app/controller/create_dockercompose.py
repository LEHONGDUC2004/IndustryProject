import os

def create_compose(docker_path, name_database, name_user, host_db, passwd, filename_sql):
    compose_path = os.path.join(docker_path, 'docker-compose.yml')
    with open(compose_path, 'w') as f:
        f.write(f"""version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: host_app
    ports:
      - "5000:5000"
    depends_on:
      - {host_db}
    environment:
      - DB_HOST={host_db}
      - DB_USER={name_user}
      - DB_PASSWORD={passwd}
      - DB_NAME={name_database}

  {host_db}:
    image: mysql:8.0
    container_name: flask_mysql_host
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: {passwd}
      MYSQL_DATABASE: {name_database}
    ports:
      - "3306:3306"
    volumes:
      - ./{filename_sql}:/docker-entrypoint-initdb.d/{filename_sql}
volumes:
  db_data:
""")

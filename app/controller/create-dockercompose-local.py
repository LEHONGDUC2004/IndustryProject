import os

def create_compose(docker_path, name_database, name_user, host_db, passwd, filename_sql, index):
    compose_path = os.path.join(docker_path, 'docker-compose.yml')

    with open(compose_path, 'w') as f:
        if host_db.strip() == "":
            f.write(f"""version: '3.8'
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: host_app_{index}
    ports:
      - "{5000 + index}:5000"
    depends_on:
      - db_{index}
    environment:
      - DB_HOST=db_{index}
      - DB_USER={name_user}
      - DB_PASSWORD={passwd}
      - DB_NAME={name_database}

  db_{index}:
    image: mysql:8.4
    container_name: flask_mysql_host_{index}
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: {passwd}
      MYSQL_DATABASE: {name_database}
    ports:
      - "{3306 + index}:3306"
    volumes:
      - ./{filename_sql}:/docker-entrypoint-initdb.d/{filename_sql}
""")
        else:
            f.write(f"""version: '3.8'
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: host_app_cloud_{index}
    ports:
      - "{5000 + index}:5000"
    environment:
      - DB_HOST={host_db}
      - DB_USER={name_user}
      - DB_PASSWORD={passwd}
      - DB_NAME={name_database}
""")

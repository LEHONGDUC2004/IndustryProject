import os


def create_compose(docker_path, name_database, name_user, host_db, passwd):
    has_init_sql = os.path.exists(os.path.join(docker_path, "init.sql"))
    compose_path = os.path.join(docker_path, 'docker-compose.yml')
    with open(compose_path, 'w') as f:
        f.write(f"""\
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: host_app
    ports:
      - "5000:5000"
    depends_on:
      - db
    environment:
      - DB_HOST={name_database}
      - DB_USER={name_user}
      - DB_PASSWORD={passwd}
      - DB_NAME={host_db}

  db:
    image: mysql:5.7
    container_name: flask_mysql_host
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: {passwd}
      MYSQL_DATABASE: {host_db}
    ports:
      - "3306:3306"
""")
        if has_init_sql:
            f.write("    volumes:\n")
            f.write("      - ./init.sql:/docker-entrypoint-initdb.d/init.sql\n")

        f.write("""\
volumes:
  db_data:
""")

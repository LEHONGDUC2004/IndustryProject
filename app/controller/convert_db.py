import subprocess

def import_sql_to_mysql(sql_path, db_info):
    command = [
        'mysql',
        f"-h{db_info['DB_HOST']}",
        f"-u{db_info['DB_USER']}",
        f"-p{db_info['DB_PASSWORD']}",
        db_info['DB_NAME']
    ]


    docker_command = ['docker', 'exec', '-i', 'flask_app_container_name'] + command

    with open(sql_path, 'rb') as f:
        process = subprocess.Popen(docker_command, stdin=f)
        process.wait()

import subprocess

def import_sql_to_mysql(sql_path, db_info):
    """
    Import file .sql vào container MySQL bằng docker exec
    """
    command = [
        'mysql',
        f"-h{db_info['DB_HOST']}",
        f"-u{db_info['DB_USER']}",
        f"-p{db_info['DB_PASSWORD']}",
        db_info['DB_NAME']
    ]

    # Tên container MySQL đúng
    docker_command = ['docker', 'exec', '-i', 'flask_mysql_host'] + command

    try:
        with open(sql_path, 'rb') as f:
            process = subprocess.Popen(docker_command, stdin=f)
            process.wait()
            if process.returncode == 0:
                print("Import .sql thành công")
            else:
                print("Import thất bại với mã lỗi", process.returncode)
    except FileNotFoundError as e:
        print("Lệnh 'docker' không tồn tại. Có thể đang chạy trong container không có docker CLI.")

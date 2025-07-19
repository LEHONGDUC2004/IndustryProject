import subprocess

def import_sql_to_mysql(sql_path, db_info):
    cmd = [
        "mysql",
        f"-h{db_info['DB_HOST']}",
        f"-u{db_info['DB_USER']}",
        f"-p{db_info['DB_PASSWORD']}",
        db_info['DB_NAME']
    ]

    try:
        with open(sql_path, 'rb') as f:
            subprocess.run(cmd, stdin=f, check=True)
        print(f"Import {sql_path} thành công vào MySQL!")
    except subprocess.CalledProcessError as e:
        print(f"Lỗi import SQL: {e}")

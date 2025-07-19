import subprocess

def import_sql_to_mysql(sql_path, db_info):
    cmd = [
        "mysql",
        f"-h{db_info['DB_HOST']}",
        f"-u{db_info['DB_USER']}",
        f"-p{db_info['DB_PASSWORD']}",
        db_info['DB_NAME']
    ]

    print("CMD:", ' '.join(cmd))  # ⚠️ In ra để kiểm tra

    try:
        with open(sql_path, 'rb') as f:
            subprocess.run(cmd, stdin=f, check=True)
    except FileNotFoundError as e:
        print("❌ FileNotFoundError:", e)
        print("🔎 Có thể không tìm thấy chương trình 'mysql'.")
        raise

import pymysql

def create_database_if_not_exists(db_info):
    connection = None  # ✅ Khởi tạo để tránh lỗi UnboundLocalError
    try:
        connection = pymysql.connect(
            host=db_info['DB_HOST'],
            user=db_info['DB_USER'],
            password=db_info['DB_PASSWORD'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{db_info['DB_NAME']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )
        connection.commit()
        print(f"✅ Đã tạo hoặc xác nhận tồn tại database `{db_info['DB_NAME']}`.")
    except Exception as e:
        print(f"❌ Lỗi khi tạo database: {e}")
    finally:
        if connection:
            connection.close()

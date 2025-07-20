from app.controller.convert_db import import_sql_to_mysql  # Đổi theo tên thật
import os

db_info = {
    'DB_NAME': 'clinic_db',
    'DB_USER': 'root',
    'DB_PASSWORD': '123456',
    'DB_HOST': 'localhost'
}

sql_path = 'C:/init.sql'  # Đảm bảo đường dẫn đúng

# Gọi hàm
import_sql_to_mysql(sql_path, db_info)

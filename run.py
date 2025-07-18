from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
    print("Database và các bảng đã được khởi tạo!")
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

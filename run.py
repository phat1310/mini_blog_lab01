from app import create_app, db
from app.models import User, Post

# Khởi tạo instance ứng dụng từ factory
app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Hỗ trợ flask shell tự động nạp db và các models"""
    return {'db': db, 'User': User, 'Post': Post}


if __name__ == '__main__':
    # Chạy server ở chế độ debug để tự reload khi sửa code
    app.run(debug=True)

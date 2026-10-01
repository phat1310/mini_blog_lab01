import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Khoá bí mật dùng để mã hoá session và bảo vệ form CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Phatnt-PWD301-Lab01-SecretKey-2026'

    # Đường dẫn cơ sở dữ liệu SQLite theo đúng chuẩn Lab 01
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # Tắt thông báo thay đổi để tiết kiệm tài nguyên
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Bật bảo vệ CSRF cho toàn bộ ứng dụng
    WTF_CSRF_ENABLED = True

    # Cấu hình phân trang: 5 bài viết mỗi trang theo yêu cầu đề bài
    POSTS_PER_PAGE = 5

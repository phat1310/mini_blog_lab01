from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class User(UserMixin, db.Model):
    """
    Model Người Dùng (User)
    - Kế thừa UserMixin để cung cấp sẵn các thuộc tính/phương thức cần cho Flask-Login:
      is_authenticated, is_active, is_anonymous, get_id()
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Quan hệ 1 - N: Một user có thể viết nhiều post
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Băm mật khẩu an toàn bằng Werkzeug trước khi lưu trữ"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """So khớp mật khẩu người dùng nhập vào với chuỗi băm trong CSDL"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    """Hàm nạp user từ session cookie cho Flask-Login"""
    return db.session.get(User, int(user_id))



class Post(db.Model):
    """
    Model Bài Viết (Post)
    - Thuộc về một User thông qua user_id (Foreign Key)
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'
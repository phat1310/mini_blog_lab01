from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    """Form đăng ký tài khoản người dùng mới"""
    username = StringField(
        'Tên đăng nhập',
        validators=[
            DataRequired(message='Vui lòng nhập tên đăng nhập.'),
            Length(min=3, max=64, message='Tên đăng nhập phải từ 3 đến 64 ký tự.'),
            Regexp(
                r'^[A-Za-z][A-Za-z0-9_.]*$',
                message='Tên đăng nhập phải bắt đầu bằng chữ cái và chỉ chứa chữ cái, số, gạch dưới (_) hoặc dấu chấm (.).'
            )
        ]
    )
    email = StringField(
        'Địa chỉ Email',
        validators=[
            DataRequired(message='Vui lòng nhập địa chỉ email.'),
            Email(message='Địa chỉ email không đúng định dạng.'),
            Length(max=120, message='Email không được vượt quá 120 ký tự.')
        ]
    )
    password = PasswordField(
        'Mật khẩu',
        validators=[
            DataRequired(message='Vui lòng nhập mật khẩu.'),
            Length(min=8, message='Mật khẩu phải có độ dài tối thiểu 8 ký tự.')
        ]
    )
    password2 = PasswordField(
        'Xác nhận mật khẩu',
        validators=[
            DataRequired(message='Vui lòng xác nhận mật khẩu.'),
            EqualTo('password', message='Mật khẩu xác nhận không trùng khớp với mật khẩu đã nhập.')
        ]
    )
    submit = SubmitField('Đăng ký tài khoản')

    def validate_username(self, username):
        """Kiểm tra tên đăng nhập đã tồn tại trong CSDL chưa"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Tên đăng nhập này đã được sử dụng. Vui lòng chọn tên khác.')

    def validate_email(self, email):
        """Kiểm tra email đã tồn tại trong CSDL chưa"""
        user = User.query.filter_by(email=email.data.strip().lower()).first()
        if user is not None:
            raise ValidationError('Địa chỉ email này đã được đăng ký. Vui lòng sử dụng email khác.')


class LoginForm(FlaskForm):
    """Form đăng nhập hỗ trợ đăng nhập bằng Username hoặc Email"""
    username_or_email = StringField(
        'Tên đăng nhập hoặc Email',
        validators=[DataRequired(message='Vui lòng nhập tên đăng nhập hoặc email.')]
    )
    password = PasswordField(
        'Mật khẩu',
        validators=[DataRequired(message='Vui lòng nhập mật khẩu.')]
    )
    remember_me = BooleanField('Ghi nhớ đăng nhập (Remember me)')
    submit = SubmitField('Đăng nhập')


class PostForm(FlaskForm):
    """Form tạo mới và chỉnh sửa bài viết (CRUD Post)"""
    title = StringField(
        'Tiêu đề bài viết',
        validators=[
            DataRequired(message='Tiêu đề bài viết không được để trống.'),
            Length(min=3, max=140, message='Tiêu đề bài viết phải từ 3 đến 140 ký tự.')
        ]
    )
    body = TextAreaField(
        'Nội dung bài viết',
        validators=[
            DataRequired(message='Nội dung bài viết không được để trống.'),
            Length(min=5, message='Nội dung bài viết phải có ít nhất 5 ký tự.')
        ]
    )
    submit = SubmitField('Lưu bài viết')

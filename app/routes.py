from urllib.parse import urlsplit
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Post
from app.forms import RegistrationForm, LoginForm, PostForm

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Trang chủ hiển thị danh sách bài viết theo phân trang (5 bài/trang)"""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 5)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    posts = pagination.items
    return render_template('index.html', title='Trang chủ', pagination=pagination, posts=posts)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Đăng ký tài khoản người dùng mới (áp dụng PRG pattern & hash password)"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Đăng ký tài khoản thành công! Vui lòng đăng nhập để bắt đầu.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', title='Đăng ký tài khoản', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Đăng nhập bằng Username hoặc Email (hỗ trợ remember_me và next_url an toàn)"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.username_or_email.data.strip()
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier.lower())
        ).first()

        if user is None or not user.check_password(form.password.data):
            flash('Tên đăng nhập / Email hoặc mật khẩu không chính xác.', 'danger')
            return render_template('login.html', title='Đăng nhập', form=form)

        login_user(user, remember=form.remember_me.data)
        flash(f'Chào mừng trở lại, {user.username}!', 'success')

        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('login.html', title='Đăng nhập', form=form)


@bp.route('/logout')
@login_required
def logout():
    """Đăng xuất người dùng hiện tại"""
    logout_user()
    flash('Bạn đã đăng xuất tài khoản thành công.', 'info')
    return redirect(url_for('main.index'))


@bp.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Tạo bài viết mới (bắt buộc đăng nhập)"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data.strip(),
            body=form.body.data.strip(),
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Bài viết của bạn đã được đăng thành công!', 'success')
        return redirect(url_for('main.post_detail', post_id=post.id))

    return render_template('post_form.html', title='Tạo bài viết mới', form=form)


@bp.route('/posts/<int:post_id>')
def post_detail(post_id):
    """Xem chi tiết bài viết (công khai cho mọi người dùng)"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', title=post.title, post=post)


@bp.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Chỉnh sửa bài viết (chỉ tác giả mới có quyền, người khác bị 403 Forbidden)"""
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.body = form.body.data.strip()
        db.session.commit()
        flash('Bài viết đã được cập nhật thành công!', 'success')
        return redirect(url_for('main.post_detail', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body

    return render_template('post_form.html', title='Chỉnh sửa bài viết', form=form, post=post)


@bp.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Xóa bài viết (chỉ tác giả mới có quyền, người khác bị 403 Forbidden)"""
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Bài viết đã được xóa thành công!', 'info')
    return redirect(url_for('main.index'))


@bp.app_errorhandler(403)
def forbidden_error(error):
    """Xử lý lỗi 403 Forbidden khi người dùng truy cập trái quyền hạn"""
    return render_template('403.html', title='403 - Quyền truy cập bị từ chối'), 403


@bp.app_errorhandler(404)
def not_found_error(error):
    """Xử lý lỗi 404 Not Found khi đường dẫn không tồn tại"""
    return render_template('404.html', title='404 - Không tìm thấy trang'), 404
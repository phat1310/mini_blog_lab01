# Mini Blog - Lab 01 (PWD301)

Ứng dụng web Blog thu nhỏ được phát triển bằng Flask Framework, kết hợp Flask-WTF, Flask-SQLAlchemy, Flask-Migrate và Flask-Login theo mô hình **Application Factory**.

- **Sinh viên**: Nguyễn Tấn Phát
- **Mã số sinh viên**: SE173285
- **Tài khoản**: `Phatnt`
- **Môn học**: PWD301 - Python Web Development

---

## 1. Cấu Trúc Dự Án

```text
mini_blog/
│
├── app/
│   ├── __init__.py           # Application Factory khởi tạo app & extensions
│   ├── models.py             # User và Post data models (SQLAlchemy ORM)
│   ├── forms.py              # RegistrationForm, LoginForm, PostForm (Flask-WTF)
│   ├── routes.py             # Blueprint 'main' xử lý định tuyến & logic
│   └── templates/            # Giao diện Jinja2 (Bootstrap 5)
│       ├── base.html         # Khung giao diện dùng chung, Navbar, Flash messages
│       ├── index.html        # Trang chủ liệt kê bài viết & phân trang
│       ├── register.html     # Form đăng ký tài khoản
│       ├── login.html        # Form đăng nhập (Username/Email + Remember me)
│       ├── post_form.html    # Form tạo mới & chỉnh sửa bài viết
│       ├── post_detail.html  # Xem chi tiết bài viết & tác vụ của tác giả
│       ├── 403.html          # Trang lỗi 403 Forbidden
│       └── 404.html          # Trang lỗi 404 Not Found
│
├── migrations/               # Quản lý phiên bản CSDL sinh bởi Flask-Migrate
├── config.py                 # Cấu hình Secret Key, SQLite CSDL, phân trang
├── run.py                    # Entry point khởi chạy ứng dụng Flask
├── requirements.txt          # Danh sách thư viện cần thiết
└── README.md                 # Tài liệu hướng dẫn sử dụng
```

---

## 2. Các Tính Năng Đã Hoàn Thiện

1. **Quản lý Tài khoản (Authentication)**:
   - Đăng ký tài khoản mới: Kiểm tra regex tên đăng nhập, định dạng email, mật khẩu tối thiểu 8 ký tự, xác nhận mật khẩu, kiểm tra trùng lặp email/username.
   - Băm mật khẩu một chiều an toàn bằng Werkzeug (`generate_password_hash`, `check_password_hash`).
   - Đăng nhập linh hoạt bằng Tên đăng nhập HOẶC Email, hỗ trợ tùy chọn `Remember me`.
   - Đăng xuất an toàn và quản lý session cookie với `Flask-Login`.

2. **Quản lý Bài viết (Post CRUD)**:
   - **Create**: Người dùng đã đăng nhập có thể soạn thảo và đăng bài viết mới.
   - **Read**: Trang chủ phân trang tự động (5 bài viết mỗi trang), sắp xếp bài mới nhất lên đầu. Xem chi tiết bài viết ở trang riêng.
   - **Update / Delete**: Chỉ chính tác giả bài viết mới có quyền Chỉnh sửa hoặc Xóa bài viết.
   - **Authorization Check**: Bất kỳ người dùng nào cố tình truy cập link `/posts/<id>/edit` hoặc xóa bài của người khác sẽ bị trả về lỗi **403 Forbidden**.

3. **Bảo mật**:
   - Tích hợp **CSRF Protection** tự động trên toàn bộ các form POST qua Flask-WTF.
   - Áp dụng mẫu thiết kế **Post/Redirect/Get (PRG Pattern)** để chống gửi lặp dữ liệu khi refresh trình duyệt.

---

## 3. Hướng Dẫn Cài Đặt & Khởi Chạy

### Bước 1: Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### Bước 2: Khởi tạo và đồng bộ Cơ sở dữ liệu (Flask-Migrate)
Trong thư mục `mini_blog/`:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Bước 3: Chạy Server phát triển
```bash
python run.py
```
Truy cập trình duyệt tại địa chỉ: `http://127.0.0.1:5000`

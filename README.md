# Backend - Movie Recommendation System (Neo4j)

## Cài đặt môi trường (Setup)

### Bước 1: Khởi tạo và kích hoạt môi trường ảo (Tuỳ chọn nhưng khuyến nghị)
Sử dụng **venv** (mặc định của Python):
```bash
python -m venv venv
# CMD:
venv\Scripts\activate
```

### Bước 2: Cài đặt các thư viện phụ thuộc
Chạy lệnh sau để cài đặt các package cần thiết:
```bash
pip install -r requirements.txt
```

### Bước 3: Cấu hình biến môi trường
Mã nguồn sử dụng file `.env` để quản lý thông tin kết nối an toàn đến Neo4j.
Hãy tạo hoặc chỉnh sửa file `.env` nằm trong thư mục `BE` với nội dung tương tự như sau:
```ini
NEO4J_URI=neo4j+s://<your_database_id>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<your_password>
```
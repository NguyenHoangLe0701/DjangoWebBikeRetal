# Sử dụng image chính thức của Python
FROM python:3.12-slim

# Đặt thư mục làm việc trong container
WORKDIR /app
# Cài đặt các gói hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
    
# Sao chép file yêu cầu vào container
COPY requirements.txt /app/

# Cài đặt các gói yêu cầu
RUN pip install -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . /app/

# Chạy lệnh migrate và collectstatic
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Chạy server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
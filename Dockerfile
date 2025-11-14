# Dockerfile (simplified, reliable)
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# 1) 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) 소스 복사
COPY . .

# 3) 개발 서버 실행
EXPOSE 8000
CMD ["bash","-lc","python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
FROM python:3.10-slim-bookworm

WORKDIR /app

# OS 패키지 및 인증서 설치
RUN apt-get update && apt-get install -y ca-certificates curl && update-ca-certificates

COPY requirements.txt .

# pip SSL 문제 우회
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
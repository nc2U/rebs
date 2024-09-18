# 기본 nginx 이미지 사용
FROM nginx:1.27.1

# 패키지 목록 업데이트 및 netcat 설치 (하나의 RUN 명령으로 병합)
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN mkdir -pv /app/django
WORKDIR /app/django
COPY requirements.txt .
RUN apt update && apt upgrade -y \
    && pip install --upgrade pip && pip install --upgrade setuptools \
    && apt install python3-dev default-libmysqlclient-dev build-essential -y \
    && pip install --trusted-host pypi.python.org -r requirements.txt \
    && apt install -y locales \
    && locale-gen ko_KR.UTF-8 \
    && apt install fonts-nanum fonts-nanum-coding fonts-nanum-extra \
    && apt autoremove -y

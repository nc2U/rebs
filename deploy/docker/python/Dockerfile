FROM python:3.12
ENV PYTHONUNBUFFERED 1
RUN mkdir -pv /app/django
WORKDIR /app/django
COPY requirements.txt .
RUN apt update && apt upgrade -y && apt autoremove -y \
    && apt install python3-dev default-libmysqlclient-dev build-essential -y \
    && apt install -y locales && locale-gen ko_KR.UTF-8 \
    && apt install fonts-nanum fonts-nanum-coding fonts-nanum-extra \
    && pip install --upgrade pip && pip install --upgrade setuptools \
    && pip install --trusted-host pypi.python.org -r requirements.txt

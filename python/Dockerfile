FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN mkdir -pv /applications/django
WORKDIR /applications/django
COPY requirements.txt .
RUN apt update \
    && pip install --upgrade pip \
    && apt install python3-dev default-libmysqlclient-dev build-essential -y \
    && pip install --trusted-host pypi.python.org -r requirements.txt \
    && apt install -y locales \
    && locale-gen ko_KR.UTF-8 \
    && apt install fonts-nanum fonts-nanum-coding fonts-nanum-extra \
    && apt autoremove -y

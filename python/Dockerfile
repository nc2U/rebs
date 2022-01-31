FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN mkdir /applications && cd /applications && mkdir django
WORKDIR /applications/django
ADD requirements.txt /applications/django/
RUN apt update \
    && pip install --upgrade pip \
    && apt install python3-dev default-libmysqlclient-dev build-essential -y \
    && pip install --trusted-host pypi.python.org -r requirements.txt \
    && apt remove python3-dev default-libmysqlclient-dev build-essential -y \
    && apt autoremove -y \

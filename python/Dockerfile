FROM python
ENV PYTHONUNBUFFERED 1
RUN mkdir /applications && cd /applications && mkdir django
WORKDIR /applications/django
ADD requirements.txt /applications/django/
RUN apt update \
    && apt install default-libmysqlclient-dev build-essential -y \
    && pip install --upgrade pip \
    && pip install --trusted-host pypi.python.org -r requirements.txt \
    && apt install -y locales \
    && locale-gen ko_KR.UTF-8 \
    && apt install fonts-nanum fonts-nanum-coding fonts-nanum-extra \
    && apt remove default-libmysqlclient-dev build-essential -y
ENV LANG ko_KR.UTF-8

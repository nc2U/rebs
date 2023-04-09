[![CodeQL](https://github.com/austin-kho/Rebs/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/austin-kho/Rebs/actions/workflows/codeql-analysis.yml)

# Django 4.1 + Vue3 + Svelte using Nginx + MariaDB (deploy as Docker or Kubernetes)

## Deploy Using Docker

#### Requirement in your system

- docker
- docker-compose
- node (with yarn)

### Usage

#### 1. Clone this Repository

```bash
clone https://github.com/nc2U/Rebs
cd Rebs
```

#### 2. Copy docker-compose.yml

```bash
cd deploy
cp docker-compose.yml.tmpl docker-compose.yml
```

#### 3. Write environments in docker-compose.yml

Check what must be defined in docker-compose.yml file.

- required:
    - MYSQL_DATABASE
    - MYSQL_ROOT_PASSWORD
    - MYSQL_USER
    - MYSQL_PASSWORD
    - DATABASE_NAME
    - DATABASE_USER
    - DATABASE_PASSWORD
    - DJANGO_SETTINGS_MODULE
    - SERVER_NAME

Enter the actual data for your environment as described in the following items.

- master:
    - MYSQL_DATABASE: my-db-name # **mysql database information**
    - MYSQL_USER: my-db-user # **mysql database information**
    - MYSQL_PASSWORD: my-db-password # **mysql database information**
    - MYSQL_ROOT_PASSWORD: my-db-root-password # **mysql database information**
    - TZ: Asia/Seoul # **mysql database information**
- web:
    - DATABASE_NAME: my-db-name # **mysql database information**
    - DATABASE_USER: my-db-user # **mysql database information**
    - DATABASE_PASSWORD: my-db-password # **mysql database information**
    - AWS_ACCESS_KEY_ID: aws-access-key-id # **your amazon s3 setup information**
    - AWS_SECRET_ACCESS_KEY: aws-secret-access-key # **your amazon s3 setup information**
    - DJANGO_SETTINGS_MODULE: app.settings.prod # **settings mode -> app.settings.prod** or **app.settings.local**
- nginx:
    - SERVER_NAME: example.com # **server hostname**
    - BACKEND_HOST: web:8000
    - WORKER_PROCESSES: 1
    - WORKER_CONNECTIONS: 1024
    - KEEPALIVE_TIMEOUT: 65
    - BACKEND_MAX_FAILS: 3
    - BACKEND_MAX_TIMEOUT: 10s
    - LOG_STDOUT: "true"
    - ADMIN_EMAIL: admin@example.com # **edit with real data**

#### 4. Django setting

To develop in local mode set docker-compose.yml -> web -> DJANGO_SETTINGS_MODULE: app.settings.local

To develop in production mode, create a prod.py file with the following command:

```bash
cd app/django/app/settings
cp local.py prod.py
```

In production mode, configure the **prod.py** file according to your needs. If not modified, it is the same as local
mode.

#### Build and run

```bash
docker-compose up -d --build
```

#### Migrations & Migrate settings (After build to db & web)

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

#### Create Superuser => your username & email & password settings

```bash
docker-compose exec web python manage.py createsuperuser
```

#### Data Seeding

```
docker-compose exec web python manage.py loaddata rebs/fixtures/seeds-data.json 
```

#### Static file Setting

```
docker-compose exec web python manage.py collectstatic
```

※ Place your Django project in the **django** directory and develop it.

#### Vue (Single Page Application) Development

```bash
cd ..
cd app/vue3
yarn
```

Vue application development -> webpack dev server on.

```bash
yarn serve
```

or Vue application deploy -> yarn build

```bash
yarn build
```

## Or Deploy Using Kubernetes

#### Requirement

- kubernetes cluster with helm installed
- nfs server(ip)
- domain(to deploy)
- GitHub account(for using GitHub Actions)

### Usage

#### 1. Building a deployment environment

... update coming soon

#### 2. Create a GitHub account

... update coming soon

#### 3. Source fork & Create secret data

... update coming soon

#### 4. deploy

... update coming soon

#### Reference

- [Python](https://www.python.org)
- [Docker](https://www.docker.com)
- [Docker compose](https://docs.docker.com/compose)
- [Django](https://www.djangoproject.com)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [MariaDB](https://mariadb.org)
- [Nginx](https://www.nginx.com/)
- [Node](https://nodejs.org/ko/)
- [Yarn](https://yarnpkg.com/)
- [kubernetes](https://kubernetes.io/docs/home/)
- [helm](https://helm.sh/docs/)

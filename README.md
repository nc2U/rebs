[![CodeQL](https://github.com/austin-kho/Rebs/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/austin-kho/Rebs/actions/workflows/codeql-analysis.yml)

# Django 5.0 + Vue3 + Svelte using Nginx + MariaDB (deploy as Docker or Kubernetes)

## Deploy Using Docker

#### Requirement in your system

- docker
- docker-compose
- node (with pnpm)

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
    - DJANGO_SETTINGS_MODULE: app.settings.prod # **settings mode -> app.settings.prod** or **app.settings.local**

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

#### Static file Setting

```
docker-compose exec web python manage.py collectstatic
```

※ Place your Django project in the **django** directory and develop it.

#### Vue (Single Page Application) Development

```bash
cd ..
cd app/vue3
pnpm i    # npm i (or) yarn
```

Vue application development -> node dev server on.

```bash
pnpm dev    # npm run dev (or) yarn dev
```

or Vue application deploy -> node build

```bash
pnpm build    # npm run build (or) yarn build
```

#### Svelte (Single Page Application) Development

```bash
cd ..
cd app/svelte
pnpm i      # npm i (or) yarn
```

Svelte application development -> node dev server on.

```bash
pnpm dev    # npm run dev (or) yarn dev
```

or Svelte application deploy -> node build

```bashpnpm build # npm run build (or) yarn build```

## Or Deploy Using Kubernetes

#### Requirement

- Kubernetes cluster
- CI/CD server with helm installed
- NFS Storage server(ip)
- domain(to deploy)
- GitHub account(for using GitHub Actions)
- Docker hub account
- Slack incoming url

### Usage

#### 1. Preparation

###### Kubernetes cluster

Configure a Kubernetes cluster by setting up the required number of nodes.

##### CI/CD server

The ci/cd server uses the master node of the Kubernetes cluster or a separate server or PC.

If you use the master node in the cluster as a ci/cd server, set up external access through ssh and install helm on the
master node.

If you are using a server or PC outside the cluster, configure it to connect via ssh from outside, install helm, and
then copy and configure the kubeconfig file to the user's home directory to access and control the master node.

Check the IP or domain that can access the ci/cd server.

##### NFS storage server

For the nfs storage server, it is recommended to prepare a separate server if a large amount of data will be used in the
future, but you can also use the cluster's master node or ci/cd server.

Install the necessary packages according to the operating system on the server to be used as a storage server, run it as
an NFS server, and connect it to the Kubernetes cluster nodes.

Also, enable connection via ssh and check the accessible IP or domain.

##### Domain & DNS setting

Secure the domain to be used for this project and connect each cluster node to the domain.

##### GitHub & DockerHub account, Slack incoming url

Use an existing GitHub account or create a new one and fork this project.

Afterward, go to the Settings > Secrets and variables > Actions menu and click the 'New repository secret' button to
create Repository secrets with the keys and values below.

- CICD_HOST: # cicd server host(ip or domain)
- CICD_PASS: # cicd server user password
- CICD_USER: # cicd server user
- CICD_PATH: # cicd helm chart & volume path
- DATABASE_USER: # db & db user name
- DATABASE_PASS: # root & db user password
- NFS_HOST:  # nfs storage server host(ip or domain)
- NFS_PASS:  # nfs storage server user password
- NFS_PATH:  # nfs storage server path (absolute path)
- NFS_USER:  # nfs storage server user
- DOMAIN_NANE: # domain address (for ingress)
- SLACK_INCOMING_URL: # slack incoming url

#### 2. Deploy

Go to the action tab in the GitHub repository.

Click 'Show more workflows...' at the bottom of all workflows, click `_initial [Prod Step1]`, and then use the
Kubernetes `watch` command on the cicd server to check whether the relevant PODs are created and operating normally.

When all database pods operate normally,
Click `_initial [Prod Step2]` at the bottom of all workflows in the action tab.

#### Reference

- [Python](https://www.python.org)
- [Docker](https://www.docker.com)
- [Docker compose](https://docs.docker.com/compose)
- [kubernetes](https://kubernetes.io/docs/home/)
- [helm](https://helm.sh/docs/)
- [Nginx](https://www.nginx.com/)
- [MariaDB](https://mariadb.org)
- [Django](https://www.djangoproject.com)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Node](https://nodejs.org/ko/)
- [pnpm](https://pnpm.io/)

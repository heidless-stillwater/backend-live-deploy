

# Deploy & Run Django on the App Engine standard environment
https://cloud.google.com/build/docs/deploying-builds/deploy-appengine

--- 

### 'local' install
Firstly, setup using local install.

This uses local assets for DB & Static files.

We will then migrate both to using Google Cloud assets.

### DB
```
sudo service postgresql restart
psql -U postgres
-
postgres
-

# create db
CREATE DATABASE  portfolio;

# create user
CREATE USER arjuna11 WITH PASSWORD 'havana11';

```

### create/configure app engine
#### new project
```
'New Project'
Project: heidless-pfolio-deploy-8	
ID: heidless-pfolio-deploy-8	

```

## inialize cli (vsCode)
```
# home dir
cd /home/heidless/LIVE/pfolio/


```

## install/init python & venv

- ### [Managing Python](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-python.html)


- ### Python Installation

    - ### [Pipenv: Python Dev Workflow for Humans](https://pipenv.pypa.io/en/latest/)
        - ### [pipenv installation](https://pipenv.pypa.io/en/latest/installation.html)


## prep environment
```
# Clone a sample app
#git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
#cd python-docs-samples/appengine/standard_python3/django

# github load raw Application
git clone https://github.com/heidless-stillwater/backend-LIVE-WORKING.git

cd /home/heidless/LIVE/pfolio/backend-LIVE-WORKING

#pipenv shell	# activate shell

cd app
pip install -r requirements.txt

```

## Download Cloud SQL Auth proxy to connect to Cloud SQL from your local machine
```
# Authenticate and acquire credentials for the API:
gcloud auth application-default login
--
heidlessemail04@gmail.com
--

# init proxy
cd config
curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.6.1/cloud-sql-proxy.linux.amd64
```

## PostgreSQL instance
```
##################################################
# if on LOCAL
# restart server

sudo service postgresql restart

# check process running
ps aux | grep '[b]in/postgres

##################################################
# if on GAE


#####################################
# ENV Settings

GCP_PROJECT=heidless-pfolio-deploy-8
GCP_REGION=europe-west2
GCP_DB_VERSION=POSTGRES_15
GCP_INSTANCE=pfolio-backend-instance-1
GCP_DB_NAME=pfolio-backend-db-1
GCP_DB_USER=pfolio-backend-user-1
GCP_DB_URL=postgres://pfolio-backend-user-1:Havana111965@//cloudsql/heidless-pfolio-deploy-8:europe-west2:pfolio-backend-instance-1/pfolio-backend-db-1
GCP_USER_PWD=Havana111965
GCP_BUCKET=$GCP_PROJECT-bucket-1
GCP_SECRET_SETTINGS=pfolio-backend-secret
GCP_SVC_ACCOUNT=heidless-pfolio-deploy-8@appspot.gserviceaccount.com	


# DB URL
# assemble link from the above info
postgres://<USER>:<PWD>@//cloudsql/<PROJECT ID>:<REGION>:<INSTANCE>/<DB>
--
postgres://pfolio-backend-user-1:Havana111965@//cloudsql/heidless-pfolio-deploy-8:europe-west2:pfolio-backend-instance-1/pfolio-backend-db-1

--

#####################################

# initialize to ensure working with correct project & ID
gcloud init

# initialise App Engine
gcloud app create
--
heidless-pfolio-deploy-8@appspot.gserviceaccount.com	
--

# initialise DB Instance (takes some time  - take a break and let it process)
gcloud sql instances create $GCP_INSTANCE \
    --project $GCP_PROJECT \
    --database-version $GCP_DB_VERSION \
    --tier db-f1-micro \
    --region $GCP_REGION

gcloud sql databases create $GCP_DB_NAME \
    --instance $GCP_INSTANCE

gcloud sql users create $GCP_DB_USER \
    --instance $GCP_INSTANCE \
    --password $GCP_USER_PWD

# check status of instance
gcloud sql instances describe --project $GCP_PROJECT $GCP_INSTANCE
--
state: RUNNABLE
--

##################### TIPS/TRICKS ############################
###

### If need to REBUILD SQL Instance

# disable deletion protection
https://console.cloud.google.com/sql/instances/pfolio-instance-0/edit?project=heidless-pfolio-deploy-7&supportedpurview=project

DataProtecrtion->Enable DeletionProtection

# delete instance - if it exisrs
gcloud sql instances delete pfolio-instance-0
##############################################################
```

## storage bucket
```
# initialise BUCKET
gsutil mb -l europe-west2 gs://$GCP_BUCKET

```

### service account(s)
```
'IAM & ADMIN'->Service Accounts

```
heidless-pfolio-deploy-8@appspot.gserviceaccount.com	

```
-
edit principal
-

# add ROLES to allow access to DB & 'secrets'
--
Secret Manager Secret Accessor
Cloud SQL Admin
Storage Admin
--
```

generate & install KEY file
```
'IAM & ADMIN'->Service Accounts->'3 dots'->Manage Keys
'ADD KEY'->JSON

# Download & install json file
' copy to local project/app/config directory'
/home/heidless/projects/backend-live/app/config

---
export GCP_CREDENTIALS=heidless-pfolio-deploy-8-2caf1618650c.json
---

```

## secrets setup
```
# setup local environment

cd config

echo DEBUG=True >> .env
echo DATABASE_URL=$GCP_DB_URL >> .env
echo GS_BUCKET_NAME=pfolio-deploy-bucket-0 >> .env
echo SECRET_KEY=$(cat /dev/urandom | LC_ALL=C tr -dc '[:alpha:]'| fold -w 50 | head -n1) >> .env
echo FRONTEND_URL=https://pfolio-frontend-2-bun63gfm5a-nw.a.run.app/ >> .env

# store in secret manager
# enable secretmanager.googleapis.com if asked
gcloud secrets delete $GCP_SECRET_SETTINGS

gcloud secrets create $GCP_SECRET_SETTINGS --data-file .env

gcloud secrets describe $GCP_SECRET_SETTINGS

# Grant access to the secret to the App Engine standard service account
gcloud secrets add-iam-policy-binding $GCP_SECRET_SETTINGS \
    --member serviceAccount:$GCP_SVC_ACCOUNT \
    --role roles/secretmanager.secretAccessor

# test - retrieve content of '$GCP_SECRET_SETTINGS'
gcloud secrets versions access latest --secret $GCP_SECRET_SETTINGS && echo ""

```

# SECRET - RESET
```
## ensure you are in the right PROJECT
gcloud config set project heidless-pfolio-deploy-7

## remove existing SECRET
gcloud secrets delete $GCP_SECRET_SETTINGS

## create new SECRET file
gcloud secrets create $GCP_SECRET_SETTINGS --data-file .env

## Grant access to the secret to the App Engine standard service account
gcloud secrets add-iam-policy-binding $GCP_SECRET_SETTINGS \
    --member serviceAccount:$GCP_SVC_ACCOUNT \
    --role roles/secretmanager.secretAccessor
```

### settings.py
Need to link to the 'key' file you downloaded earlier.
set GS_CREDENTIALS
```
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(BASE_DIR, 'config/heidless-pfolio-deploy-8-2caf1618650c.json.json')
)

GS_BUCKET_NAME = 'pfolio-bucket-0'

settings_name = os.environ.get('SETTINGS_NAME', '$GCP_SECRET_SETTINGS')

STATIC_URL = 'https://storage.cloud.google.com/pfolio-bucket-0/'

```

disable local settings to force use of Google Secrets
```
mv config/.env config/.env-gae
```


## configure access
https://console.cloud.google.com/sql/instances/pfolio-instance-0/connections/networking?project=heidless-pfolio-deploy-7
```
pfolio-instance-0 -> Connections -> Networking -> Add a Network
--
rob-laptop
2.99.19.9
--
```

## check if can access DB directly
```
gcloud sql connect pfolio-backend-instance-1 --database $GCP_DB_NAME --user=pfolio-backend-user-1 --quiet

gcloud sql connect $GCP_INSTANCE --database pfolio-backend-db-1 --user=$GCP_DB_USER --quiet
--
password:
Havana111965

```

### ESSENTIAL: set CLOUD vars
```
export GOOGLE_CLOUD_PROJECT=$GCP_PROJECT
export USE_CLOUD_SQL_AUTH_PROXY=true
export CLOUDRUN_SERVICE_URL=https://$GCP_SVC_ACCOUNT

```

### enable cloud proxy

```
./cloud-sql-proxy --credentials-file ./$GCP_CREDENTIALS \
--port 1234 $GCP_PROJECT:$GCP_REGION:$GCP_INSTANCE

# kill & restart - IF address already in use
sudo lsof -i -P -n | grep LISTEN
kill -9 <PID>

```

### init & run backend
```
python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser
-
heidless
rob.lockhart@yahoo.co.uk
sdfsdgasgTHW66GDGdfdff
-

# init 'static' directory
mkdir app/build/static
python manage.py collectstatic

python manage.py runserver 8080

# view site
http://localhost:8080

# view site/admin
http://localhost:8080/admin
```

## Deploy the app to the App Engine standard environment

```
# initialze app - creates 'app.yaml'
vi app/app.yaml
--
runtime: python39
env: standard
entrypoint: gunicorn -b :$PORT config.wsgi:application

handlers:
- url: /.*
  script: auto

runtime_config:
  python_version: 3
--

################################################
# deploy to app engine
gcloud app deploy

# display APP URL
gcloud app describe --format "value(defaultHostname)"
-
https://heidless-pfolio-deploy.nw.r.appspot.com
-

# monitor logs
gcloud app logs tail -s default
-
target url: https://pfolio-backend-2.ew.r.appspot.com
target service account: pfolio-backend-2@appspot.gserviceaccount.com
-

# Open app.yaml and update the value of APPENGINE_URL with your deployed URL:
vi app.yaml
-
env_variables:
	APPENGINE_URL: https://pfolio-backend-2.ew.r.appspot.com/

-

# BACKUPS
pg_dump \
-U pfolio-user-0	 \
--format=custom \
--no-owner \
--no-acl \
pfolio-db-0	 > pfolio-db-0.dmp



# re-deploy
gcloud app deploy

```

## Updating the application
To update your application, make changes to the code, then run the gcloud app deploy command again.

# pgadmin

## Create pgadmin dir
```
mkdir <project root>/pgadmin
cd !$
```

## Dockerfile
Create
```
FROM dpage/pgadmin4

ENV PGADMIN_DEFAULT_EMAIL=rob.lockhart@yahoo.co.uk

ENV PGADMIN_DEFAULT_PASSWORD=havana111965

ENV PGADMIN_LISTEN_PORT=8080
```


Builld
```
gcloud builds submit --tag=gcr.io/heidless-pfolio-deploy-4/pgadmin4
```

Deploy
```
gcloud run deploy --image=gcr.io/heidless-pfolio-deploy-4/pgadmin4 --platform=managed
```

## Access
https://pgadmin4-um4b6gn3cq-nw.a.run.app

## [Connecting to GCP’s Cloud SQL (PostgresSQL) from PgAdmin — 3 simple steps](https://cshiva.medium.com/connecting-to-gcps-cloud-sql-postgressql-from-pgadmin-3-simple-steps-2f4530488a4c)

## [pgAdmin Backup Database in PostgreSQL Simplified 101](https://hevodata.com/learn/pgadmin-backup-database/#11)

## [Backup Dialog](https://www.pgadmin.org/docs/pgadmin4/development/backup_dialog.html)

## [Why pgAdmin 4 is so slow](https://stackoverflow.com/questions/62186945/why-pgadmin-4-is-so-slow)

#### LOGIN CREDENTIALS (See contents of Dockerfile)

## access locally
http://127.0.0.1/pgadmin4

# phpMyAdmin
https://cloud.google.com/sql/docs/mysql/phpmyadmin-on-app-engine



dropdb --if-exists --username postgres hpfolio

psql -U postgres postgres
CREATE DATABASE pfolio_db_local;
CREATE USER arjuna11 WITH SUPERUSER PASSWORD 'havana11';
\l
\du
\q
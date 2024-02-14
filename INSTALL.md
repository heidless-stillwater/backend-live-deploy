![abba-1974-billboard-1548.webp](:/f95dff06bf7846dab8b816b01b7fe4fc)
# Learn 'phonetically'
When ABBA had their first hits in the English Language - they did not speak English.

They learned their own songs phonetically and achieved huge success.

Subsequently, they mastered English and went on to further success & achieve iconic status.

Sadly, I cannot guarantee international fame & fortune!

However, If you're new to Google Cloud then it is feasible to learn by doing.

Might I humbly suggest, 'It's the Name of the Game' ;-)

My aim here it to enable a Google Cloud newbie to walk through the steps below to deploy an app to Google App Engine.

By focusing on the 'how' you learn the 'what' and so gain foundational knowlege upon which to build & re-enforce.

J.F.D.I 

One Love

===============================================================

# target audience

By new to Google Cloud I do NOT mean new to IT.

Pre-requisites:
- vScode
	- Linux via WSL (Ubuntu 22.04)
- Linux terminal
	- file system
		- navigation
		- modification
- Python (basic)
	- focus is on 'scripting'
		- variable creation & assignment
		- conditional statements

## shaving 'yaks'

Yak shaving refers to a task, that leads you to perform another related task and so on, and so on — all distracting you from your original goal. This is sometimes called “going down the rabbit hole.”

ORIGIN: 

https://americanexpress.io/yak-shaving/#:~:text=%E2%80%9CYak%20shaving%E2%80%9D%20(or%20%E2%80%9C,The%20Ren%20%26%20Stimpy%20Show.%E2%80%9D

![Yak_shaving.jpg](:/9c0d9861931d42d588501ca1283c27af)

If you're unsure whether you fulfill these pre-requisites I'd suggest - Just Do It.

Start the Walkthrough.

Whenever you hit a gap in your knowledge - take some time to research the gap.

The amount of Yak Shaving is an excellent calibration of your actual skills as opposed to your own opinion of your skills - they rarely match!

Gaining 'new' knowledge builds on your accumulated knowledge. 

This can confirm your expertise AND it can also expose areas where you are NOT as expert as you believed yourself to be.

Diplomatically put - You Don't Know What You Don't Know.

This is a clinically researched phenomenon known as the Dunig-Kruger Effect.

Duning-Kruger should be your spirit guide. We ALL suffer from it! - Including YOU.

Duning-Kruger: https://www.youtube.com/watch?v=y50i1bI2uN4

Some Yak Shaving is inevitable & even beneficial in refining your expertise.

When learning - Yak-shaving is useful to calibrate where your at. 

If you're doing none & in the learning phase then I'd suggest you are not challenging yourself and tipping into procrastination.

However, if you spend most of your time doing so - you likely should focus on achieving the pre-requisites before resuming this tutorial.

Bottom line: Humility is HUGELY valuable.

**'Humility is not thinking Less of Yourself, It is Thinking of Yourself Less'**

Okay, enough cod-wisdom & jabber from me. Let's crack on!
...

# Deploy & Run Django on the App Engine standard environment
https://cloud.google.com/build/docs/deploying-builds/deploy-appengine

## GOAL
Deploy a dJango backend to Google App Engine.

## PURPOSE
Learn the mechanism(s) required to deploy an existing dJango app to Google App Engine.

### View Example
You can find an example of the fully deployed app here:

<span style="color: #ff00ff"># < link to live app></span>

Check it out.

```
# Open the deployed website:
gcloud app browse
-
https://pfolio-backend-2.ew.r.appspot.com/
-
# Alternatively, display the URL and open manually:
gcloud app describe --format "value(defaultHostname)"

```

Next time you see this - YOU will have deployed your own version of the same.

--- 

# create/configure app engine
## new project
```
'New Project'
Project: cloud-run-install
ID: cloud-run-install
```

## enable billing

### WARNING!!: 
Be VERY careful that you understand the cost implications of the resources we will be using.

If new to Google Cloud then you are able to sign up with a generous 'FREE' period along with with a very useful Credit towards the use of PAID resources.

 MORE INFO: 
 - https://cloud.google.com/billing/docs
 - https://cloud.google.com/billing/docs/how-to/verify-billing-enabled
 
 ENABLE:
 - https://console.cloud.google.com/billing/linkedaccount?project=pfolio-live

## 'local' install
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





## inialize cli (vsCode)
```
# home dir
cd /home/heidless/LIVE/pfolio/

# initialize to ensure working with correct project & ID
gcloud init
'Create a new configuration'
pfolio-backend-2
dreamseedambience...
pfolio-backend-2

# initialise App Engine
gcloud app create
REGION: europe-west2
```

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
-
ambientuplift@gmail.com
-

# enable Google Auth Library
-
-

# init proxy

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

# ensure correct project
gcloud config set project heidless-pfolio-deploy

# initialise DB Instance (takes some time  - take a break and let it process)
gcloud sql instances create pfolio-instance-0 \
    --project heidless-pfolio-deploy-0 \
    --database-version POSTGRES_13 \
    --tier db-f1-micro \
    --region europe-west2
-                                                       
Created [https://sqladmin.googleapis.com/sql/v1beta4/projects/heidless-pfolio-deploy/instances/pfolio-instance-0].
NAME               DATABASE_VERSION  LOCATION        TIER         PRIMARY_ADDRESS  PRIVATE_ADDRESS  STATUS
pfolio-instance-0  POSTGRES_13       europe-west2-b  db-f1-micro  35.197.253.39    -                RUNNABLE
-
	
# if asked - enable API [sqladmin.googleapis.com]
	
gcloud sql databases create pfolio-db-0 \
    --instance pfolio-instance-0
	
gcloud sql users create pfolio-user-0 \
    --instance pfolio-instance-0 \
    --password Havana111965

# check status of instance
gcloud sql instances describe --project heidless-pfolio-deploy pfolio-instance-0
-
-

# DB URL
# assemble link from the above info
postgres://<USER>:<PWD>@//cloudsql/<PROJECT ID>:<REGION>:<INSTANCE>/<DB>
--
postgres://pfolio-user-0:Havana111965//cloudsql/heidless-pfolio-deploy:europe-west2:pfolio-instance-0/pfolio-db-0
--

##################### TIPS/TRICKS ############################
###

### If need to REBUILD SQL Instance

# disable deletion protection
https://console.cloud.google.com/sql/instances/pf-pg-instance-0/edit?project=xenon-pier-390513&supportedpurview=project
EDIT->DeletionProtection

# delete instance - if it exisrs
gcloud sql instances delete pfolio-instance-2
##############################################################
```

## storage bucket
```
# PROJECT: pfolio-
gcloud config set project heidless-pfolio-deploy

# initialise BUCKET
gsutil mb -l europe-west2 gs://h_pfolio_deploy_0
```

### service account(s)
```
PROJECT: heidless-pfolio-deploy
ID: heidless-pfolio-deploy

'IAM & ADMIN'->Service Accounts

```
api-svc@cloud-run-install.iam.gserviceaccount.com
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
```

## secrets setup
```
# setup local environment - TEMPORARILY
# 
<!-- echo DATABASE_URL=postgres://DATABASE_USERNAME:DATABASE_PASSWORD@//cloudsql/PROJECT_ID:REGION:INSTANCE_NAME/DATABASE_NAME > .env
echo GS_BUCKET_NAME=PROJECT_ID_MEDIA_BUCKET >> .env
echo SECRET_KEY=$(cat /dev/urandom | LC_ALL=C tr -dc '[:alpha:]'| fold -w 50 | head -n1) >> .env
 -->


cd config
echo DATABASE_URL=postgres://pfolio-user-0:Havana111965@//cloudsql/heidless-pfolio-deploy:europe-west2:pfolio-instance-0/pfolio-db-0 > .env
echo GS_BUCKET_NAME=h_pfolio_deploy_0 >> .env
echo SECRET_KEY=$(cat /dev/urandom | LC_ALL=C tr -dc '[:alpha:]'| fold -w 50 | head -n1) >> .env
echo FRONTEND_URL=https://pfolio-frontend-v2xr7nz45q-nw.a.run.app/ >> .env

# store in secret manager
# enable secretmanager.googleapis.com if asked
gcloud secrets create django_settings --data-file .env

gcloud secrets describe django_settings

# Grant access to the secret to the App Engine standard service account
gcloud secrets add-iam-policy-binding django_settings \
    --member 
    serviceAccount:pfolio-0@heidless-pfolio-deploy.iam.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor
		
# test - retrieve content of 'django_settings'
gcloud secrets versions access latest --secret django_settings && echo ""

###############################
# when reseting - delete SECRET
gcloud secrets delete django_settings
-
enable Secret Mgr API if asked
-
```

## WARNING

Now you have setup your Cloud Secrets based on you .env file you now have 2 SOURCES OF TRUTH.

Not good.

In the heat of battle you'll likely find yourself modifying one while using the other.

WASTE of Time & Effort. Demoralising. 

My recommendation at this stage is to disable your local .env. to force use of your shiny new Google Secret (django_settings).

DELETE or RENAME app/config/.env file. i.e. ``rm ./config/.env``

## revise secrets
RECOMMENDATION: When debugging, only change ONE thing at a time - then test.
- Otherwise you will NOT KNOW the impact of any individual change or their combination
- These settings are foundational to your app.
- BOTH accuracy & understanding is vital
- Rushing will cost you significantly MORE TIME
- Make One Chane. Test It. Repeat.

It's likely that you will be refining & modifying the definitions in your SECRETS settings i.e. 'django_settings'.
- You'll likely want to test different settings - particularly when refining/debugging/hardening
- This will involve your REPLACING  you current SECRETS - i.e. django_settings.

```
# ensure you are in the right PROJECT
gcloud config set project heidless-pfolio-deploy

edit the config/.env file as needed.

# remove existing SECRET
gcloud secrets delete django_settings

# create new SECRET file
gcloud secrets create django_settings --data-file .env

# Grant access to the secret to the App Engine standard service account
gcloud secrets add-iam-policy-binding django_settings \
    --member serviceAccount:pfolio-0@heidless-pfolio-deploy.iam.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor
```


# Run the app via your local computer
We will use your local installation but hook into the Google Cloud Resources.

The Goal here is to switch from using local definitions to using those you have configured on App Engine.

A key one is where your SECRETS are stored.

The settings.py priorities local '.env' over your Google Secrets.

AFTER we've updated the following in settings.py we will be 'disabling' local definitions.

### settings.py
Need to link to the 'key' file you downloaded earlier.
set GS_CREDENTIALS
```
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(BASE_DIR, 'config/heidless-pfolio-deploy-f5ccc52a65af.json')
)
```

set STATIC_URL
```
STATIC_URL = 'https://storage.cloud.google.com/pfolio-bucket-0/'
```

disable local settings to force use of Google Secrets
```
mv config/.env config/.env-gae
```

### on localhost - run in dedicated shell - <span style="color: #ff807f">DELETE!!!</span>
```
# configure access
https://console.cloud.google.com/sql/instances/pfolio-instance-0/connections/networking?project=heidless-pfolio-deploy

pfolio-backend-db-instance-0 -> connections -> add network
-
rob-laptop
78.149.229.160
-
# check if can access DB directly
gcloud sql connect pfolio-instance-0 --database pfolio-db-0 --user=pfolio-user-0 --quiet

password:
Havana111965
```

### ESSENTIAL: set CLOUD vars

### run & access app from localhost
```

```

##########################################

```
export GOOGLE_CLOUD_PROJECT=heidless-pfolio-deploy-0
export USE_CLOUD_SQL_AUTH_PROXY=true
export CLOUDRUN_SERVICE_URL=https://heidless-pfolio-deploy@appspot.gserviceaccount.com

```

### enable cloud proxy
```
./cloud-sql-proxy --credentials-file ./heidless-pfolio-deploy-0-b97b8a94c2ba.json \
--port 1234 heidless-pfolio-deploy-0:europe-west2:pfolio-instance-0
  

<!-- ./cloud-sql-proxy --credentials-file heidless-pfolio-deploy-f5ccc52a65af.json --port 1234 heidless-pfolio-deploy:europe-west2:pfolio-instance-0 -->

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

ENV PGADMIN_DEFAULT_PASSWORD=havana11

ENV PGADMIN_LISTEN_PORT=8080
```


Builld
```
gcloud builds submit --tag=gcr.io/cloud-run-install/pgadmin4
```

Deploy
```
gcloud run deploy --image=gcr.io/cloud-run-install/pgadmin4 --platform=managed
```

## Access
https://pgadmin4-njepcfc3la-nw.a.run.app/login?next=%2F

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
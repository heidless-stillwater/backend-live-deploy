[Export and import using SQL dump files](https://cloud.google.com/sql/docs/postgres/import-export/import-export-sql)

gsutil mb -l europe-west2 gs://sqldump-bucket-3

gcloud sql instances describe pfolio-instance-0 # get service accout email

<!-- p575011123703-ko74ca@gcp-sa-cloud-sql.iam.gserviceaccount.com -->

<!-- gsutil -m iam set -r iam.txt gs://dogs -->

<!-- gsutil iam ch user:john.doe@example.com:objectCreator gs://ex-bucket -->

gsutil iam ch serviceAccount:p575011123703-ko74ca@gcp-sa-cloud-sql.iam.gserviceaccount.com:objectAdmin gs://sqldump-bucket-3

# backup db instance
gcloud sql export sql pfolio-instance-0 gs://sqldump-bucket-3/sqldumpfile.gz \
--database=pfolio-db-0 \
--offload
  
# restore db instance
gcloud sql instances describe pfolio-instance-0

gsutil iam ch serviceAccount:p575011123703-ko74ca@gcp-sa-cloud-sql.iam.gserviceaccount.com:objectAdmin \
gs://sqldump-bucket-3

gcloud sql import sql pfolio-instance-0 gs://sqldump-bucket-3/sqldumpfile.gz \
--database=pfolio-db-0
  


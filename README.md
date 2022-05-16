# Taiga.io Backup

Create backup for all projects of a user

## Configuration

Upload to S3 or copying to file server location is supported.

env vars:

* `TAIGA_USER`: the taiga user (has to be a real user, not a social login)
* `TAIGA_PASSWORD`: the password
* `S3_KEY`: a s3 key
* `S3_SECRET`: corresponding secret
* `S3_REGION`: the region (e.g. `eu-central-1`)
* `S3_BUCKET`= the target bucket
* `FILE_SERVER_LOCATION`: a directory to copy the backup to

If `FILE_SERVER_LOCATION` is defined, S3 will be ignored.

## Running

`docker-compose up` or `python backup-taiga.py`

## Usage with K8s CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: taiga-backup
spec:
  schedule: "0 18 * * 5"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: taiga-backup
            image: 52north/taiga-backup:latest
            imagePullPolicy: Always
            env:
            - name: TAIGA_USER
              value: user
            - name: TAIGA_PASSWORD
              value: pw
            - name: S3_KEY
              value: s3key
            - name: S3_SECRET
              value: s3secret
            - name: S3_REGION
              value: eu-central-1
            - name: S3_BUCKET
              value: target-bucket
          restartPolicy: OnFailure
```
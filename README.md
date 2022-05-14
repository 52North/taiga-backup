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

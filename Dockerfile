FROM python:alpine3.15

RUN pip install requests
RUN mkdir -p /opt/taiga-backup/backups
COPY backup-taiga.py /opt/taiga-backup/

WORKDIR /opt/taiga-backup/

CMD [ "python", "backup-taiga.py" ]
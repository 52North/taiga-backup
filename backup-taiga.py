from requests import get, post
import os
import time
from datetime import datetime
import shutil

user = os.environ.get("TAIGA_USER", "user")
password = os.environ.get("TAIGA_PASSWORD", "password")

# login
x = post("https://api.taiga.io/api/v1/auth", json={
        "password": password,
        "type": "normal",
        "username": user
    })
user_json = x.json()
print(user_json)

if "auth_token" in user_json:
    bearer_token = user_json["auth_token"]

if "id" in user_json:
    member_id = user_json["id"]

projects_url = "https://api.taiga.io/api/v1/projects?member=%s&order_by=user_order&slight=true" % member_id


# retrieve projects
x = get(projects_url, headers={"Authorization": "Bearer %s" % bearer_token})
projects_json = x.json()

requested_projects = []

def upload_file(file_name):
    print("Uploading file: %s" % file_name, flush=True)
    # TODO upload to file server or S3

def download_export(r, target_folder):
    print("Working on project: %s" % r["slug"], flush=True)
    
    download_url = "https://media-protected.taiga.io/exports/%s/%s-%s.json" % (r["id"], r["slug"], r["export_id"])

    x = get(download_url, headers={"Authorization": "Bearer %s" % bearer_token})
    
    while x.status_code > 300 or ("Content-Length" in x.headers and x.headers["Content-Length"] == "0"):
        print("download not yet available: %s" % x.status_code, flush=True)
        time.sleep(10)
        x = get(download_url, headers={"Authorization": "Bearer %s" % bearer_token})
    
    file_name = download_url[download_url.rindex("/") + 1:]
    
    
    target_file = "./" + target_folder +"/" + file_name
    with open(target_file, "wb") as file:
        # write to file
        file.write(x.content)
    print("file written: %s" % target_file, flush=True)

print("Starting backup at: %s" % datetime.now(), flush=True)

# init backups
backup_date = datetime.today().strftime("%Y-%m-%d")
target_folder = "backups/" + backup_date
os.makedirs(target_folder, exist_ok=True)
for p in projects_json:
    export_url = "https://api.taiga.io/api/v1/exporter/%s" % p["id"]
    x = get(export_url, headers={"Authorization": "Bearer %s" % bearer_token})
    project_json = x.json()
    
    k = 0
    while "export_id" not in project_json:
        print("export still throttled: %s" % project_json, flush=True)
        time.sleep(15)
        x = get(export_url, headers={"Authorization": "Bearer %s" % bearer_token})
        project_json = x.json()
        
        k = k+1
        if (k > 10):
            raise Exception("Unknown issue with taiga API: %s" % x.text())
   
    r = {"id": p["id"], "slug": p["slug"], "export_id": project_json["export_id"]}
    download_export(r, target_folder)
    


shutil.make_archive("backups/taiga-backup_" + backup_date, 'zip', target_folder)
upload_file("backups/taiga-backup_" + backup_date + ".zip")
print("backup finished at: %s" % datetime.now(), flush=True)
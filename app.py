from flask import Flask, render_template, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from git import Repo
import os
import shutil

def download_private_repo(access_token, repo_url, target_folder):
    try:
        if os.path.exists(target_folder):
            shutil.rmtree(target_folder)
        url_with_token = f'https://{access_token}@{repo_url}'
        Repo.clone_from(url_with_token, target_folder)
    except Exception as e:
        print("Error with the download")
        exit(84)

def scheduled_download():
    print("Scheduled download started...")
    download_private_repo(github_access_token, repo_url, target_folder)
    print("Scheduled download completed.")

github_access_token = "YOUR_ACCESS_TOKEN"
repo_url = "YOUR_REPO_URL"
target_folder = "content"
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

download_private_repo(github_access_token, repo_url, target_folder)

app = Flask(__name__)

content_folder = "content"
allowed_extensions = {"jpg", "jpeg", "png", "gif", "mp4", "webm"}

def get_files():
    files = []
    websites_file_path = os.path.join(content_folder, "websites.txt")

    for file in os.listdir(content_folder):
        if is_allowed_file(file):
            files.append(file)
            
    if os.path.exists(websites_file_path):
        with open(websites_file_path, 'r') as websites_file:
            websites = websites_file.read().splitlines()
            files.extend(websites)
            
    return files

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def scheduled_job():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_download, 'interval', minutes=30)
    scheduler.start()

@app.route('/')
def index():
    files = get_files()
    return render_template('index.html', files=files)

@app.route('/favicon.ico')
def icon():
    return send_from_directory("static", "favicon.ico")

@app.route('/content/<path:filename>')
def serve_file(filename):
    return send_from_directory(content_folder, filename)

if __name__ == '__main__':
    scheduled_job()
    app.run(debug=True)

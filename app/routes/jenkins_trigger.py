from flask import Blueprint, render_template
import requests, logging
from urllib.parse import urljoin
from app.controller.config import JENKINS_BASE_URL, JENKINS_USER, JENKINS_API_TOKEN
upload_bp = Blueprint('upload', __name__)
logger = logging.getLogger(__name__)


session = requests.session()
session.auth = (JENKINS_USER, JENKINS_API_TOKEN)
session.headers.update({"User-Agent": "upload-service/1.0", "Accept": "application/json"})

def get_crumb():
    # /crumbIssuer/api/json trả về {"crumbRequestField":"Jenkins-Crumb","crumb":"..."}
    url = urljoin(JENKINS_BASE_URL + "/", "crumbIssuer/api/json")
    r = session.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    return {data["crumbRequestField"]: data["crumb"]}

# Trigger build with ZIP_NAME + S3_KEY
def trigger_jenkins_build(zip_filename, s3_key):
    payload = {
        "ZIP_NAME": zip_filename,
        "S3_KEY": s3_key
    }
    r = session.post(JENKINS_JOB_URL, params=payload, timeout=10)
    logger.info(
        "Trigger Jenkins: ZIP_NAME=%s S3_KEY=%s -> %s",
        zip_filename, s3_key, r.status_code
    )
    return r.status_code



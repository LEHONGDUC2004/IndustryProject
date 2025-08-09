from flask import Blueprint, render_template
import requests, logging

upload_bp = Blueprint('upload', __name__)
logger = logging.getLogger(__name__)

# Jenkins config
JENKINS_BASE_URL = 'http://34.238.48.211/'
JENKINS_JOB_URL = f"{JENKINS_BASE_URL}/job/download-code-from-s3/buildWithParameters"
JENKINS_VIEW_URL = f"{JENKINS_BASE_URL}/view/MyView"
JENKINS_USER = 'lehongduc3491'
JENKINS_API_TOKEN = '1190c9794884b4fd7a5b110cbd41571209'

session = requests.session()
session.auth = (JENKINS_USER, JENKINS_API_TOKEN)
session.headers.update({"User-Agent": "upload-service/1.0"})


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



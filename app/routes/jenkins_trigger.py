from flask import Blueprint, render_template
import requests, logging

upload_bp = Blueprint('upload', __name__)
logger = logging.getLogger(__name__)

# Jenkins config
JENKINS_BASE_URL = 'http://3.212.74.20:8080'
JENKINS_JOB_URL = f"{JENKINS_BASE_URL}/job/build-web-static/buildWithParameters"
JENKINS_VIEW_URL = f"{JENKINS_BASE_URL}/view/MyView"
JENKINS_USER = 'lehongduc3491'
JENKINS_API_TOKEN = '11e592530e49b4dde7bdf44ee65b6e9685'


# Trigger build with ZIP_NAME param
def trigger_jenkins_build(zip_filename):
    payload = {
        'ZIP_NAME': zip_filename
    }
    response = requests.post(
        JENKINS_JOB_URL,
        auth=(JENKINS_USER, JENKINS_API_TOKEN),
        params=payload
    )
    logger.info(f"Triggered Jenkins build with ZIP_NAME={zip_filename}, status={response.status_code}")
    return response.status_code


from flask import Blueprint
import os, zipfile, shutil, requests, logging

upload_bp = Blueprint('upload', __name__)
logger = logging.getLogger(__name__)


JENKINS_URL = 'http://192.168.202.1:8081/job/build-web-static/buildWithParameters'
JENKINS_USER = 'lehongduc3491'
JENKINS_API_TOKEN = '110eaba63ed58b2bf4c17121b75c764984'

def trigger_jenkins_build(zip_filename):
    payload = {
        'ZIP_NAME': zip_filename  # Truyền tên file, không phải path
    }
    response = requests.post(
        JENKINS_URL,
        auth=(JENKINS_USER, JENKINS_API_TOKEN),
        params=payload
    )
    logger.info(f" Jenkins Triggered with ZIP_NAME={zip_filename}, status={response.status_code}")
    return response.status_code

# app/controller/config.py
import os
JENKINS_BASE_URL = os.getenv("JENKINS_BASE_URL")
JENKINS_USER = os.getenv("JENKINS_USER")
JENKINS_API_TOKEN = os.getenv("JENKINS_API_TOKEN")
JENKINS_GENERIC_TOKEN = os.getenv("JENKINS_GENERIC_TOKEN")
KEY_SERVER = os.getenv("KEY_SERVER")


import boto3
import os
from datetime import datetime

s3 = boto3.client('s3')
S3_BUCKET = 'duckou-myproject'

def upload_to_s3(file_path, filename, user_id, project_id):
    # Tạo prefix theo user và ngày giờ để tránh trùng
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    s3_key = f"uploads/user-{user_id}/project-{project_id}/{filename}"

    s3.upload_file(file_path, S3_BUCKET, s3_key)
    return s3_key

def get_old_version(bucket, key, version_id, dest):
    s3.download_file(bucket, key, dest, ExtraArgs={"VersionId": version_id})

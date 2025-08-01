import os

def count_uploaded_zips(upload_dir):
    return len([f for f in os.listdir(upload_dir) if f.endswith('.zip')])
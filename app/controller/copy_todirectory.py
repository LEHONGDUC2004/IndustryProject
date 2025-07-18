import shutil
import os
def copy_docker_files(destination_dir):
    base_dir = os.path.join(os.getcwd(), 'base_templates')
    dockerfile_src = os.path.join(base_dir, 'Dockerfile')
    compose_src = os.path.join(base_dir, 'docker-compose.yml')
    dockerfile_dst = os.path.join(destination_dir, 'Dockerfile')
    compose_dst = os.path.join(destination_dir, 'docker-compose.yml')

    shutil.copyfile(dockerfile_src, dockerfile_dst)
    shutil.copyfile(compose_src, compose_dst)

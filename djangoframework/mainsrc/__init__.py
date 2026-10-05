from .celery import app as celery_app
import yaml
import os
__all__ = ('celery_app',)


root_dir = os.getcwd()
yaml_file_path = os.path.join(root_dir, "configure.yaml")


with open(yaml_file_path, "r") as f:
    config = yaml.safe_load(f)

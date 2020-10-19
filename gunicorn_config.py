from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

command = BASE_DIR / 'venv/bin/gunicorn'
pythonpath = BASE_DIR
bind = os.getenv('EXTERNAL_HOST')
workers = 2
user = 'www'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=config.settings'
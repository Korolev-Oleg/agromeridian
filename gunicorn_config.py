from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

command = BASE_DIR / 'venv/bin/gunicorn'
pythonpath = BASE_DIR
bind = '127.0.0.1:8001'
workers = 2
user = 'www'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=config.settings.production'

if __name__ == '__main__':
    print(BASE_DIR)

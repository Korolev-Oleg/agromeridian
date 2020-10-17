# Agromeridian
Automation of the business process "Issuance of cargo passes" for the company "Agro Meridian"
>django/python

### Logic scheme
![project scheme](docs/scheme.png)

### Quick start
Install requirements
```shell script
pip install requirements.txt
```

Migrate models to database
```shell script
python manage.py migrate
```

Collect static files
```shell script
python manage.py collectstatic
```

Make and setup SECRET.py
``` python
# SECURITY WARNING: keep this file secret!
SECRET_KEY = ''

# Smtp settings
EMAIL_HOST = ''
EMAIL_PORT = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_SSL: bool

ALLOWED_HOSTS = [
    'localhost'
]
```

Run gunicorn in .
```shell script
gunicorn -w 2 config.wsgi 
```
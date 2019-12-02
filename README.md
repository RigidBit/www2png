# www2png

This is the primary codebase for the www2png web application.

## Development Prerequisites

* RigidBit
* PostgreSQL
* Beanstalkd
* Apache or Nginx with WSGI/UWSGI capability.
* Selenium server with Chrome webdriver.

## Development Setup

### Using a venv is recommended.
```
python -m venv init venv
source venv/bin/activate
```

### Installing dependencies:
```
pip install -r requirements.txt
```

### Starting the development server:
```
FLASK_APP=web.py FLASK_DEBUG=1 python -m flask run -h 0.0.0.0
```

## Basic Webserver Setup Procedure
* Create a web directory and create an initialized venv within it.
* Install dependencies within the venv.
* Populate .env with secrets and settings.
* Configure webserver to use WSGI with the venv and serve static content from the static and data directories.

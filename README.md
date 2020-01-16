# WWW2PNG

This is the primary codebase for the www2png web application.

WWW2PNG is a free webpage screenshot service API with blockchain anchoring using RigidBit and Ethereum.

## Development Prerequisites

Before developing on this application you should have working knowledge of the following technologies and toolchains:

* HTML 5 / CSS 3 / Javascript (ECMAScript 6)
* SASS (https://sass-lang.com/)
* Npm (https://www.npmjs.com/)
* Python3 (https://www.python.org/)
* Selenium (https://selenium.dev/)
* Webpack (https://webpack.js.org/)

You should also have working experience with the following frameworks and libraries:

* jQuery (http://jquery.com/)

You must have the following installed in your development environment to properly build:

* Node.js (Via NVM is recommended: https://github.com/creationix/nvm#install-script)
* Npm (Automatically installed by nvm.)
* Npx (Automatically installed by nvm.)

## Development Server Prerequisites

* Beanstalkd (https://beanstalkd.github.io/)
* PostgreSQL (https://www.postgresql.org/)
* RigidBit (https://www.rigidbit.com/)
* Selenium Server (https://selenium.dev/)
* Chrome Webdriver (https://chromedriver.chromium.org/)

## Production Server Prerequisites

* Apache or Nginx with WSGI/UWSGI capability.
* Beanstalkd (https://beanstalkd.github.io/)
* PostgreSQL (https://www.postgresql.org/)
* RigidBit (https://www.rigidbit.com/)
* Selenium Server (https://selenium.dev/)
* Chrome Webdriver (https://chromedriver.chromium.org/)

## Development Setup

### Supported Platforms

Ubuntu Linux 18.04 is the official development environment, however it may also work with other environments.

## Basic Webserver Setup Procedure
* Configure all server prerequisites.
* Create a web directory and create an initialized venv directory within it.
* Install dependencies within the venv.
* Populate .env with secrets and settings.
* Configure PostgreSQL server with a new database, user, and install the tables from `dev/sql/create_tables.sql`.
* Configure webserver to use WSGI with the venv and serve static content from the static directory.

## Developing

The steps below outline how to setup and start the development environment. This is different than production!

### Using a venv is highly recommended.
```
python -m venv init venv
source venv/bin/activate
```

### Installing dependencies from requirements.txt:
```
pip install -r requirements.txt
```

### Saving dependencies to requirements.txt:
Using `pipreqs` is recommended over `pip`. While in an active venv use the following to regenerate `requirements.txt`.
```
pipreqs --ignore node_modules --force
```

### Setting up the .env file:

See `README_ENV.md` for a basic template.

### Creating symbolic links:
Symbolic links will need to be setup from the src directory to the corresponding folders in the project root.
```
ln -s ../data src/data
ln -s ../static src/static
```

### Starting the development server:
```
npm run flask
```
or
```
FLASK_APP=src/web.py FLASK_DEBUG=1 python -m flask run -h 0.0.0.0 -p 5000
```

### Starting the development CSS builder:
```
npm start
```

### Starting the pruning service:
```
python3 pruner.py
```

### Starting the processing service:
```
python3 processor.py
```

### Starting the aciton processing service:
```
python3 action_processor.py
```

## Deploying to Production

### Building static assets for production:
This builds all static CSS assets and puts them in the `static` folder.
```
npm build
```

### Web:
Copy the following files and folders to the remote server.
```
src/*.py
src/templates/*
static/*
requirements.txt
uwsgi.ini
```
Create the following empty folders.
```
data
venv
```
Create symbolic links.
```
ln -s ../data src/data
ln -s ../static src/static
```
Create a venv and install the requirements.
```
python -m venv init venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuring the web server:

Setup your webserver to serve static content from the `static` folder. All other requests should be sent to the uWSGI handler.

See `README_NGINX.md` for a basic Nginx configuration example.

### Setting up services:
You will need to also setup services for:
- action_processor.py
- processor.py
- pruner.py
- uwsgi.py

You can use any service manager, but `systemd` is recommended. See `README_SERVICES.md` for a basic configuration examples.

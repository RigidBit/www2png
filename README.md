# www2png

This is the primary codebase for the www2png web application.

## Development Prerequisites

Before developing on this application you should have working knowledge of the following technologies and toolchains:

* HTML 5 / CSS 3 / Javascript (ECMAScript 6)
* SASS (https://sass-lang.com/)
* Npm (https://www.npmjs.com/)
* Webpack (https://webpack.js.org/)

You should also have working experience with the following frameworks and libraries:

* jQuery (http://jquery.com/)

You must have the following installed in your development environment to properly build:

* Node.js (Via NVM is recommended: https://github.com/creationix/nvm#install-script)
* Npm (Automatically installed by nvm.)
* Npx (Automatically installed by nvm.)

## Development Server Prerequisites

* RigidBit
* PostgreSQL
* Beanstalkd
* Apache or Nginx with WSGI/UWSGI capability.
* Selenium server with Chrome webdriver.

## Basic Webserver Setup Procedure
* Create a web directory and create an initialized venv directory within it.
* Install dependencies within the venv.
* Populate .env with secrets and settings.
* Configure webserver to use WSGI with the venv and serve static content from the static and data directories.

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

### Starting the development CSS builder:
```
npm start
```

### Starting the development server:
```
FLASK_APP=web.py FLASK_DEBUG=1 python -m flask run -h 0.0.0.0
```

### Building static assets for production:
```
npm build
```

# www2png

This is the primary codebase for the www2png web application.

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

* Apache or Nginx with WSGI/UWSGI capability.
* Beanstalkd (https://beanstalkd.github.io/)
* PostgreSQL (https://www.postgresql.org/)
* RigidBit (https://www.rigidbit.com/)
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
source venv/bin/activate
pip install -r requirements.txt
```

### Saving dependencies:
Using `pipreqs` is recommended over `pip`. While in an active venv use the following to regenerate `requirements.txt`.
```
pipreqs --ignore node_modules --force
```

### Starting the development server:
```
source venv/bin/activate
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
source venv/bin/activate
python3 pruner.py
```

### Starting the processing service:
```
source venv/bin/activate
python3 processor.py
```

### Starting the aciton processing service:
```
source venv/bin/activate
python3 action_processor.py
```

### Building static assets for production:
```
npm build
```

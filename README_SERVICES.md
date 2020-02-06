# WWW2PNG Services

## action_processor.py
The action processor handles events such as the sending of emails.
```
[Unit]
Description=WWW2PNG Action Processor
After=syslog.target

[Service]
Type=simple
ExecStart=/var/www/www2png.com/venv/bin/python3 /var/www/www2png.com/www2png/action_processor.py
WorkingDirectory=/var/www/www2png.com
User=www-data
Group=www-data
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

## processor.py
The processor handles the most important tasks, such as the actual creation of screenshots.
```
[Unit]
Description=WWW2PNG Processor
After=syslog.target

[Service]
Type=simple
ExecStart=/var/www/www2png.com/venv/bin/python3 /var/www/www2png.com/www2png/processor.py
WorkingDirectory=/var/www/www2png.com
User=www-data
Group=www-data
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

## pruner.py
The pruner removes expired records and files.
```
[Unit]
Description=WWW2PNG Pruner
After=syslog.target

[Service]
Type=simple
ExecStart=/var/www/www2png.com/venv/bin/python3 /var/www/www2png.com/www2png/pruner.py
WorkingDirectory=/var/www/www2png.com
User=www-data
Group=www-data
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

## uwsgi
The UWSGI server handles execution of Python scripts for the web server. UWSGI is just one of several possible ways to run Python scripts with a webserver.
```
[Unit]
Description=Www2png uWSGI
After=syslog.target

[Service]
ExecStart=/usr/bin/uwsgi --ini /var/www/www2png.com/uwsgi.ini
Restart=always
RestartSec=5
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

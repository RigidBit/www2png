# WWW2PNG Services

## action_processor.py
```
[Unit]
Description=WWW2PNG Action Processor
After=syslog.target

[Service]
Type=simple
ExecStart=/var/www/www2png.com/venv/bin/python3 /var/www/www2png.com/src/action_processor.py
WorkingDirectory=/var/www/www2png.com
User=www-data
Group=www-data
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

## processor.py
```
[Unit]
Description=WWW2PNG Processor
After=syslog.target

[Service]
Type=simple
ExecStart=/var/www/www2png.com/venv/bin/python3 /var/www/www2png.com/src/processor.py
WorkingDirectory=/var/www/www2png.com
User=www-data
Group=www-data
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

## pruner.py
```
[Unit]
Description=WWW2PNG Pruner
After=syslog.target

[Service]
Type=simple
ExecStart=/var/www/www2png.com/venv/bin/python3 /var/www/www2png.com/src/pruner.py
WorkingDirectory=/var/www/www2png.com
User=www-data
Group=www-data
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

## uwsgi
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

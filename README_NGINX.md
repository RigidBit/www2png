# WWW2PNG Nginx Setup

The following is an example configuration for an Nginx vhost.

This serves static content and pass all other requests to the uwsgi handler.

```
server {
        listen 80;
        server_name www2png.com;

        access_log /var/log/nginx/access-www2png.com.log combined;
        error_log /var/log/nginx/error-www2png.com.log warn;

        location /static/ {
                root /var/www/www2png.com;
        }

        location / {
                uwsgi_pass 127.0.0.1:9090;
                include uwsgi_params;
        }
}

```
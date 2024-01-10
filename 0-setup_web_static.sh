#!/usr/bin/env bash
#Bash script that sets up your web servers for the deployment of web_static
sudo apt-get -y update
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
echo "Task 0" |sudo tee /data/web_static/releases/test/index.html
if [ -L "data/web_static/current" ]; then
    sudo rm -r data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sudo tee "/etc/nginx/sites-available/default" > /dev/null <<EOF
server {
    listen 80;
    listen [::]:80;

    root /var/www/html;
    index index.html;

    location /redirect_me {
        return 301 http://localhost/new_page;
    }
    error_page 404 /404.html;
    location = /404.html {
        internal;
    }
           location / {
      add_header X-Served-By "$(hostname)";
    }
    location /hbnb_static/{
        alias /data/web_static/current/;
    }
}
EOF
sudo service nginx restart

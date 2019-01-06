#!/usr/bin/env sh
# sudo chmod u+x

sudo cp -R flask-pymongo-api /var/www/flask-pymongo-api &&
sudo chown -R root:root /var/www/flask-pymongo-api &&
sudo chmod -R 755 /var/www &&

sudo  mkdir -p /etc/httpd/sites-available &&
sudo mkdir -p /etc/httpd/sites-enabled &&

sudo cp flask-pymongo-api/app.main.conf /etc/httpd/sites-available &&

sudo ln -s /etc/httpd/sites-available/app.main.conf /etc/httpd/sites-enabled/app.main.conf &&
sudo systemctl restart httpd.service &&

curl localhost

# sudo rm -Rf /var/www/flask-pymongo-api &&
# sudo rm -Rf /etc/httpd/sites-available/app.main.conf &&
# sudo rm -Rf /etc/httpd/sites-enabled/app.main.conf &&
# sudo systemctl restart httpd.service
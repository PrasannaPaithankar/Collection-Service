#!/usr/bin/bash
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
cd /var/www/html
sudo git clone https://github.com/PrasannaPaithankar/Collection-Service.git collection-service
sudo chmod -R a+rwx collection-service
sudo mv /collection-service/collection-service.conf /etc/apache2/sites-available
sudo a2ensite collection-service.conf
sudo a2dissite 000-default.conf
sudo service apache2 restart
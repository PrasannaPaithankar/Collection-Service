#!/usr/bin/bash
cd /var/www/html/collection-service
sudo git pull
sudo mv /collection-service/collection-service.conf /etc/apache2/sites-available/collection-service.conf
sudo service apache2 restart
#!/usr/bin/bash
cd /var/www/html/collection-service
sudo git pull
sudo service apache2 restart
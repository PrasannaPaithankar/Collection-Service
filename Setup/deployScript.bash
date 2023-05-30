#!/usr/bin/bash
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
sudo apt-get install python3-venv
sudo apt-get install git
sudo apt-get install python3-pip
cd /var/www/html
sudo git clone https://github.com/PrasannaPaithankar/Collection-Service.git collection-service
sudo chmod -R a+rwx collection-service
sudo python3 -m venv venv
source venv/bin/activate
pip3 install -r /collection-service/requirements.txt
deactivate
sudo mv /collection-service/collection-service.conf /etc/apache2/sites-available
sudo a2ensite collection-service.conf
sudo a2dissite 000-default.conf
sudo service apache2 restart
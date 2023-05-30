#!/usr/bin/bash
sudo apache2ctl configtest
sudo cat /var/log/apache2/error.log
sudo service apache2 restart
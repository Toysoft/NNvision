#!/bin/bash

service ddclient start
service cron start
service postgresql start
service apache2 start
tail -F /var/log/apache2/error.log

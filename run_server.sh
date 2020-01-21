#!/bin/bash
docker run --name nnvision -p 80:80 -p 443:443 -v nn_data:/NNvision/media_root -v nn_settings:/NNvision/django/projet -v nn_db:/var/lib/postgresql/10/main -v nn_migrate1:/NNvision/django/app1/migrations \
            -v nn_migrate2:/NNvision/django/app2/migrations -v nn_cron:/var/spool/cron/crontabs --rm nnvision_server:0.2 &

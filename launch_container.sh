docker run --name nnvision -p 80:80 -e NVIDIA_VISIBLE_DEVICES=all -e NVIDIA_DRIVER_CAPABILITIES=compute,utility,video -v nnvision_data:/NNvision/media_root -v nnvision_settings:/NNvision/django/projet -v nnvision_db:/NNvision/django/database -v nnvision_migrate1:/NNvision/django/app1/migrations -v nnvision_migrate2:/NNvision/django/app2/migrations -v nnvision_cron:/var/spool/cron/crontabs -v /etc/localtime:/etc/localtime  --runtime=nvidia --rm nnvision:1.0.4 &

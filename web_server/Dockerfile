FROM nnvision_server_base

WORKDIR /NNvision
COPY . /NNvision

# Activate postgresql
USER postgres
RUN    /etc/init.d/postgresql start &&\
       psql --command "CREATE USER djdb WITH PASSWORD 'protecia';" && \
       psql --command "CREATE DATABASE protecia WITH OWNER djdb;" && /etc/init.d/postgresql stop

USER root
# Activate django
RUN cd django && python3 manage.py collectstatic && /etc/init.d/postgresql start &&\
    python3 manage.py makemigrations && python3 manage.py migrate && \
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@protecia.com', 'protecia')" | python3 manage.py shell && \
    python3 manage.py loaddata delay.json && /etc/init.d/postgresql stop

RUN django/change_right.sh && a2enmod  wsgi && rm Dockerfile* && rm build.sh
 

CMD ["/NNvision/start2.sh"]

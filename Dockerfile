# fnoc Docker modified for the fnoc flask application
#
# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# forked from https://github.com/fnocci/fnoc

FROM ubuntu:14.04

maintainer https://github.com/dave00galloway

RUN apt-get update

RUN apt-get install -y --no-install-recommends \
    python-software-properties \
    python-setuptools \
    build-essential \
    python-dev \
    python \
    supervisor \
    nginx \
    git 

RUN easy_install pip
RUN pip install uwsgi
RUN pip install flask

# install fibonics code from this repo
ADD . /home/fibonemc/fnoc/

# and have it be owned by same user that runs nginx
RUN chown www-data:www-data /home/fibonemc/fnoc/

#setup the nginx configs more cleanly 
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN cp /home/fibonemc/fnoc/nginx.conf /etc/nginx/sites-available/nginx-fnoc.conf
RUN ln -s /etc/nginx/sites-available/nginx-fnoc.conf /etc/nginx/sites-enabled/nginx-fnoc.conf

# since we've installed uwsgi with pip, need to give it an upstart file 
# and put its initialization file in the appropriate location
RUN cp /home/fibonemc/fnoc/uwsgi.conf /etc/init/uwsgi.conf

RUN mkdir -p /etc/uwsgi/sites
RUN cp /home/fibonemc/fnoc/uwsgi.ini /etc/uwsgi/sites/uwsgi-fnoc.ini
RUN ln -s /home/fibonemc/fnoc/supervisor-app.conf /etc/supervisor/conf.d/

EXPOSE 80

CMD ["supervisord", "-n"]

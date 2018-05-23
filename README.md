
# fnoc calculates the fibonacci sequence up to n on a web service 

...in reasonable time where n <= 999999; where n > 999999 it truncates the sequence;
where n < 0 it reports an error.  where the URL is totally malformed it reports an error.

The input is provided in a parameter on the URL; the output is JSON 

## Super Quick functional test:
* git clone https://github.com/dave00galloway/fnoc
* pip install flask
* cd into the directory fnoc
* run 'python fnoc.py'
* curl localhost:5000
* curl localhost:5000/fibonacci?n=-1
* curl localhost:5000/fibonacci?n=10
* curl localhost:5000/last?n=9999

## Quick Deploy and Test With Docker
* docker pull dave00galloway/fnocci:latest
* docker run dave00galloway/fnocci:latest

## Build and Deploy with Docker:
* git clone https://github.com/dave00galloway/fnoc
* cd into top level directory
* docker build -t fnoc .
* docker run fnoc 

## Some Quick tests on the Docker container 
* run docker network (to find out the container's IP)
* curl IP
* curl IP/fibonacci
* curl IP/fibonacci?n=10
* curl IP/fibonacci?n=10000
* curl IP/

## Deployment technology:
* Flask, uWSGI and Nginx in a single Ubuntu 14.01 LTS  Docker container
* Docker to build and deploy containerized application
* Ubuntu 14.01 LTS because it will have maintenance support until 2019
* Nginx is a fast standard web server with built in uWSGI protocol support
* uWSGI benchmarks as the fastest WSGI application container 
* Flask is a web services development platform with less baggage than Django or Pyramid

## Maintenance methodology:

If the OS, uWSGI or Nginx need, e.g. security patches applied, you can re-build the docker image from scratch

### re-build from scratch and tag the image
* modify the application fnoc.py
* modify the configuration files
* modify the Dockerfile
* docker build -t fnoc .
* docker run fnoc

and redeploy the docker image to the server of choice through, for example, salt

References:
[https://github.com/dockerfiles/django-uwsgi-nginx](https://github.com/dockerfiles/django-uwsgi-nginx)

[http://flask.pocoo.org/docs/deploying/uwsgi/#configuring-nginx](http://flask.pocoo.org/docs/deploying/uwsgi/#configuring-nginx)


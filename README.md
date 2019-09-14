# employees-memory

This is a simple flask app that implements a REST API, with 3 endpoints

No DB, all storage is in memory

### Installation no docker
1) Create a virtual env
2) On console
```sh
cd /code/folder/
pip install -U pip
pip install -r requirements.txt
python -u -m flask run
```

### Deploying for prod in docker
The prod should use nginx or apache, but for this exercise I will just set the prod environment variable for flask

1) Install docker on your system
2) On console
```sh
cd /code/folder/
docker build -t employees-memory:prod -f Dockerfile.prod .
docker run --name emprod --rm -d -p someport:5000 employees-memory:prod
```
The -p flag on the last command is to set the port of the app, change "someport"


### Deploying for dev in docker
The prod should use nginx or apache, but for this exercise I will just set the prod environment variable for flask

1) Install docker on your system
2) On console
```sh
cd /code/folder/
docker build -t employees-memory:dev -f Dockerfile.dev .
docker run --name emdev --rm -d -p someport:5000 -v $(pwd):/opt/project -w /opt/project employees-memory:dev python -u -m flask run
```
The -p flag on the last command is to set the port of the app, change "someport"
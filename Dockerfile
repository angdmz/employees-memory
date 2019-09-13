FROM python:3.6.7-alpine
RUN apk add --no-cache git \
    build-base
RUN mkdir -p /opt/project
WORKDIR /opt/project
ADD requirements.txt /opt/project
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install ipython
RUN pip install coverage
ADD . /opt/project
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
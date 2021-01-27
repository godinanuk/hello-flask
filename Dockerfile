FROM ubuntu:16.04

MAINTAINER "justsayraj@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev python-mysqldb

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "hello_flask.py" ]

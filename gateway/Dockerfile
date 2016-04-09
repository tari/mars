# Env vars:
# * SENSOR_ENDPOINT: host:port to connect to sensor at
# * GC_ENDPOINT: host:port to connect to game controller at
# Base image
FROM ubuntu

# Maintainer info
MAINTAINER Peter Marheine <peter@taricorp.net>

# Get the project
RUN apt-get update &&\
  apt-get install -y git-core python python-pip python-dev

RUN pip install websocket-client

RUN cd /opt &&\
  git clone https://github.com/tari/mars && \
  cd /opt/mars/gateway

# Set the default directory where CMD will execute
WORKDIR /opt/mars/gateway/

CMD python gateway-python.py

# Base image
FROM golang:1.4.2

# Maintainer info
MAINTAINER Peter Marheine <peter@taricorp.net>

COPY ./ /opt/sensor

WORKDIR /opt/sensor

# Get the project
RUN go get github.com/emccode/mars-challenge/sensor-client

# Expose port
EXPOSE 8080

# Run Game Controller
CMD go run *.go

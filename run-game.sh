#!/bin/sh

start_containers() {
    # Dashboard WEB PAGE communicates with the controller. We must expose it.
    docker run -d --name=controller -p 8000:8080 -e ADMIN_TOKEN=1234 emccode/mars-challenge-controller
    sleep 1
    # WS_ENDPOINT is a public URL
    docker run --link=controller:controller -d --name=dashboard -p 80:80 -e WS_ENDPOINT=localhost:8000/ws emccode/mars-challenge-dashboard
    #docker run -d --name=sensor emccode/mars-challenge-client
    #docker run --link=controller --link=sensor -d --name=gateway -e SENSOR_ENDPOINT=sensor:8080 -e GC_ENDPOINT=controller:8080 emccode/mars-challenge-gateway-py
}

stop_containers() {
    docker kill sensor controller dashboard gateway
    docker rm sensor controller dashboard gateway
}

case $1 in
    start)
        start_containers
        ;;

    stop)
        stop_containers
        ;;

    restart)
        stop_containers
        start_containers
        ;;
esac


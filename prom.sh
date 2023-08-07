#!/bin/bash
if [ "$1" == "run" ]; then
podman	run \
    --name prom \
    -d \
    -p 9090:9090 \
    -v ./prometheus.yml:/etc/prometheus/prometheus.yml:Z \
    prom/prometheus
elif [ "$1" == "stop" ]; then
    podman stop prom
    podman rm prom
else
    echo "Usage: ./prom run or stop"
fi

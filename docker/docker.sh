#!/bin/bash

docker run -d --rm --name prometheus -p 9090:9090 -v $(pwd)/prometheus.yaml:/etc/prometheus/prometheus.yml:ro prom/prometheus

docker run -d --rm --name grafana -p 3000:3000 -e GF_SECURITY_ADMIN_PASSWORD=admin -v grafana-storage:/var/lib/grafana grafana/grafana

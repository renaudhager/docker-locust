# Docker Locust

[![Docker Pulls](https://img.shields.io/docker/pulls/renaudhager/locust.svg)](https://hub.docker.com/r/renaudhager/locust)

## Description
This repository contains a Docker file to build a docker image that runs [Locust](https://locust.io/).

## Environment variables

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| URL_HOST | Hostname to query, needs to contain the schema (HTTP or HTTPS). | string | | yes |
| URL_PATH | Path to query. | string | | yes |
| CLIENTS | Number of client to emulate. | int | `100` | no |
| HATCHING_RATE | Rate to spawn the number of client to reach `CLIENTS`. | int | `10` | no |
| OPTIONS | Options to pass to Locust. Don't pass `-r` or `-c` as these options are already used by `CLIENTS` and `HATCHING_RATE`. | string | `--no-web --print-stats` | no |

## Build
To build this image, run the following command:
```
make build
```

## Run
To run this Docker image, run the following command:
```
docker run -d \
  --name locust \
  -e HOST=https://example.com \
  -e URL_PATH=/ \
  -e CLIENT=10 \
  -e HATCHING_RATE=1 \
  renaudhager/locust:latest
```

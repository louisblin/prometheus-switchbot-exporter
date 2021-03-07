# Prometheus Switchbot Exporter [![Image Version]][DockerHub] [![Image Size]][DockerHub] [![Release badge]][Release status]

A Prometheus exporter for [SwitchBot Meter] devices.

## Usage

The simplest way to deploy this exporter is on Kubernetes, using the Helm chart
provided.

First, add this repository to your Helm client:
```sh
helm repo add prometheus-switchbot-exporter https://louisblin.github.io/prometheus-switchbot-exporter
```

Then, deploy the chart to Kubernetes:
```sh
helm install switchbot-exporter prometheus-switchbot-exporter/prometheus-switchbot-exporter
```

[DockerHub]: https://hub.docker.com/r/louisleblin/prometheus-switchbot-exporter/tags
[Image Size]: https://img.shields.io/docker/image-size/louisleblin/prometheus-switchbot-exporter?sort=date
[Image Version]: https://img.shields.io/docker/v/louisleblin/prometheus-switchbot-exporter?sort=date
[Release badge]: https://github.com/louisblin/prometheus-switchbot-exporter/actions/workflows/release.yaml/badge.svg
[Release status]: https://github.com/louisblin/prometheus-switchbot-exporter/actions/workflows/release.yaml
[SwitchBot Meter]: https://www.switch-bot.com/products/switchbot-meter
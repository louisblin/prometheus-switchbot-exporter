# Prometheus Switchbot Exporter [![Release badge]][Release status]

A Prometheus exporter for [SwitchBot Meter] devices.

## Usage

The simplest way to deploy this exporter is on Kubernetes, using the Helm chart
provided.

```sh
$ helm repo add prometheus-switchbot-exporter https://louisblin.github.io/prometheus-switchbot-exporter
$ helm install switchbot-exporter prometheus-switchbot-exporter/prometheus-switchbot-exporter
```

[Release badge]: https://github.com/louisblin/prometheus-switchbot-exporter/actions/workflows/release.yaml/badge.svg
[Release status]: https://github.com/louisblin/prometheus-switchbot-exporter/actions/workflows/release.yaml
[SwitchBot Meter]: https://www.switch-bot.com/products/switchbot-meter
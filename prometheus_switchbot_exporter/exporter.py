import json
import time
import logging
from dataclasses import asdict, dataclass
from datetime import datetime

import click
from bluepy import btle
from prometheus_client import Gauge, start_http_server

gauge_rssi = Gauge("switchbot_rssi", "The Received Signal Strength Indicator (RSSI) of the device", ["device"])
gauge_battery = Gauge("switchbot_battery", "The battery percentage of the device", ["device"])
gauge_humidity = Gauge("switchbot_humidity", "The humidity percentage measured by the device", ["device"])
gauge_temperature = Gauge("switchbot_temperature", "The temperature in celsius measured by the device", ["device"])


@dataclass
class Measurement:
    battery: int
    temperature: float
    humidity: int


class ScanProcessor(btle.DefaultDelegate):
    def __init__(self, mac_address):
        self.mac_address = mac_address

    def handleDiscovery(self, device: btle.ScanEntry, is_new_device: bool, is_new_data: bool):
        try:
            if device.addr == self.mac_address.lower():
                logging.debug(
                    "Device: %s (%s), %d dBm %s (new device: %s) (new data: %s)",
                    device.addr,
                    device.addrType,
                    device.rssi,
                    ("" if device.connectable else "(not connectable)"),
                    is_new_device,
                    is_new_data,
                )
                measurement = parse_device_data(device)
                if measurement is not None:
                    publish_measurement(device, measurement)
        except:
            logging.exception("Error occured while handling discovery")


def parse_device_data(device: btle.ScanEntry):
    if not device.scanData:
        logging.debug("Device %s had no data", device.addr)

    for index, (sdid, desc, value) in enumerate(device.getScanData()):
        logging.debug("%s: %s, %s, %s", index, sdid, desc, value)

        if desc != "16b Service Data":
            continue
        elif not value.startswith("000d"):
            logging.debug("Ignoring incorrect 16b Service Data of length %s", value.len())
        else:
            byte2 = int(value[8:10], 16)
            battery = byte2 & 127

            byte3 = int(value[10:12], 16)
            byte4 = int(value[12:14], 16)
            temperature = float(byte4 - 128) + float(byte3 / 10.0)

            byte5 = int(value[14:16], 16)
            humidity = byte5

            return Measurement(battery, temperature, humidity)


def publish_measurement(device: btle.ScanEntry, measurement: Measurement):
    logging.info("Published: %s", json.dumps(asdict(measurement)))
    gauge_rssi.labels(device=device.addr).set(device.rssi)
    gauge_battery.labels(device=device.addr).set(measurement.battery)
    gauge_humidity.labels(device=device.addr).set(measurement.humidity)
    gauge_temperature.labels(device=device.addr).set(measurement.temperature)


def configure_logging(verbose, quiet, default_level=logging.INFO):
    level = default_level + (quiet - verbose) * 10
    logging.basicConfig(format="[%(levelname)-8s] %(message)s", datefmt="[%X]", level=level)


@click.command()
@click.argument("mac-address")
@click.option("-p", "--metrics-port", default=8080, help="Expose metrics as a Prometheus target")
@click.option("-v", "--verbose", count=True, help="Increase logging verbosity")
@click.option("-q", "--quiet", count=True, help="Decrease verbosity")
def main(mac_address, metrics_port, verbose, quiet):
    """Runs a Prometheus exporter scraping metrics from the Switchbot thermometer at the given MAC address"""
    configure_logging(verbose, quiet)
    start_http_server(metrics_port)

    logging.debug("Started Prometheus exporter on ':%s' for Swichbot thermometer at '%s'", metrics_port, mac_address)
    scanner = btle.Scanner().withDelegate(ScanProcessor(mac_address))
    while True:
        try:
            scanner.scan(30)
        except btle.BTLEDisconnectError as ex:
            logging.debug("Ignoring disconnection error: %s", ex)


if __name__ == "__main__":
    main()

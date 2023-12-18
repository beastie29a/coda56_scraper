#!/usr/bin/env python3
from datetime import datetime

from coda56_scraper import Coda56Scrapper
from coda56_dataclass import (
    DownstreamInfo,
    DownstreamOfdmInfo,
    UpstreamInfo,
    UpstreamOfdmInfo,
)

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "REPLACE_ME"
org = "REPLACE_ME"
bucket = "REPLACE_ME"
url = "REPLACE_ME"

coda56_write_params = {
    "downstream_info": {
        "record_tag_keys": ["portId", "channelId", "modulation"],
        "record_field_keys": [
            "frequency",
            "signalStrength",
            "snr",
            "dsoctets",
            "correcteds",
            "uncorrect",
        ],
    },
    "downstream_ofdm_info": {
        "record_tag_keys": ["receive", "ffttype", "plclock", "ncplock", "mdc1lock"],
        "record_field_keys": [
            "Subcarr0freqFreq",
            "plcpower",
            "SNR",
            "dsoctets",
            "correcteds",
            "uncorrect",
        ],
    },
    "upstream_info": {
        "record_tag_keys": ["portId", "modtype", "scdmaMode", "channelId"],
        "record_field_keys": ["frequency", "bandwidth", "signalStrength"],
    },
    "upstream_ofdm_info": {
        "record_tag_keys": ["uschindex", "state", "fftVal"],
        "record_field_keys": [
            "frequency",
            "digAtten",
            "digAttenBo",
            "channelBw",
            "repPower",
            "repPower1_6",
        ],
    },
}

assert token != "REPLACE_ME"
assert url != "REPLACE_ME"

coda56_scraper = Coda56Scrapper()
coda56_metrics = coda56_scraper.get_metrics()
cur_time = datetime.utcnow()

with InfluxDBClient(
    url=url, token=token, org=org
) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)
    for metric in coda56_metrics.keys():
        for signal_info in coda56_metrics[metric]:
            print(signal_info)
            if metric == "downstream_info":
                ds_signal = DownstreamInfo(**signal_info)
            elif metric == "downstream_ofdm_info":
                if signal_info["ffttype"] == "NA":
                    continue
                ds_signal = DownstreamOfdmInfo(**signal_info)
            elif metric == "upstream_info":
                ds_signal = UpstreamInfo(**signal_info)
            elif metric == "upstream_ofdm_info":
                if signal_info["state"] != "OPERATE":
                    continue
                ds_signal = UpstreamOfdmInfo(**signal_info)
            else:
                raise Exception
            print(ds_signal)
            write_api.write(
                bucket=bucket,
                record=ds_signal,
                record_time_key=cur_time,
                record_measurement_name=metric,
                **coda56_write_params[metric],
            )

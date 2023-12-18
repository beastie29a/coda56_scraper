import json
import urllib.request as urlreq
import ssl

MODULATION_TABLE = {
    "0": "16QAM",
    "1": "64QAM",
    "2": "256QAM",
    "3": "1024QAM",
    "4": "32QAM",
    "5": "128QAM",
    "6": "QPSK",
}

class Decoder(json.JSONDecoder):
    def decode(self, s):
        result = super().decode(s)
        return self._decode(result)

    def _decode(self, o):
        if isinstance(o, bytes) or isinstance(o, str):
            o = o.strip()
            if "." in o:
                try:
                    return float(o)
                except ValueError:
                    return o
            if "2e32" in o:
                try:
                    return eval(o.replace("e", " ** "))
                except:
                    return o
            try:
                return int(o)
            except ValueError:
                return o
        elif isinstance(o, dict):
            kv_decode = {}
            for k, v in o.items():
                if k == "modulation":
                    kv_decode.update({k: MODULATION_TABLE.get(v, "Unknown")})
                else:
                    kv_decode.update({k: self._decode(v)})
            return kv_decode
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o


class Coda56Scrapper:

    def __init__(self) -> None:
        self.context = ssl._create_unverified_context()
        self.ip = "192.168.100.1"
        self.api_url = f"https://{ self.ip }/data"
        self.modem_pages = {
            "sys_info": "getSysInfo.asp",
            "system_model": "system_model.asp",
            "cm_init": "getCMInit.asp",
            "cm_docsis_wan": "getCmDocsisWan.asp",
            "downstream_info": "dsinfo.asp",
            "downstream_ofdm_info": "dsofdminfo.asp",
            "upstream_info": "usinfo.asp",
            "upstream_ofdm_info": "usofdminfo.asp",
            "status_log": "status_log.asp",
            "link_status": "getLinkStatus.asp",
        }
        self.modem_status = ["sys_info", "cm_init", "cm_docsis_wan", "link_status"]
        self.ds_metrics = ["downstream_info", "downstream_ofdm_info"]
        self.us_metrics = ["upstream_info", "upstream_ofdm_info"]
        self.metric_units = {
            "frequency": "Hz",
            "snr": "dB",
            "Subcarr0freqFreq": "Hz",
            "plcpower": "dBmv",
            "bandwidth": "Hz",
            "signalStrength": "dBmV",
        }

    def __query_api__(self, endpoint: str) -> dict:
        api_endpoint = f"{ self.api_url}/{ endpoint }"

        request = urlreq.Request(api_endpoint)
        try:
            data = urlreq.urlopen(request, context=self.context).read().decode("utf-8")
        except Exception as ex:
            return {"error": str(ex)}
        try:
            return json.loads(data, cls=Decoder)
        except Exception as ex:
            return {"error": str(ex)}

    def get_endpoints(self) -> list:
        return list(self.modem_pages.values())

    def describe_modem(self) -> dict:
        modem_info = {}
        for k, _ in self.modem_pages.items():
            modem_info.update(self.get_endpoint_data(k))
        return modem_info

    def get_metrics(self) -> dict:
        metrics = {}
        stream_metrics = set(self.ds_metrics + self.us_metrics)
        for metric in stream_metrics:
            metrics.update(self.get_endpoint_data(metric))
        return metrics

    def to_json(self) -> str:
        return "{}"

    def get_endpoint_data(self, key_name: str) -> dict:
        response = self.__query_api__(self.modem_pages[key_name])

        return {key_name: response}


if __name__ == '__main__':
    # Sample Run
    modem_scraper = Coda56Scrapper()

    # print out the DS and US metrics
    resp = modem_scraper.get_metrics()
    print(json.dumps(resp))
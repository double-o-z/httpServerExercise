import requests
import time
import logging

logger = logging.getLogger("ReportLog")

API_KEY = "106b233ec0c0cd966f63c6e28fca35c36e1f916e1ccc3838e9dc2f21f5ed9ae0"


def file_report(file_name, file_path):
    r = Report(file_name, file_path)
    r.report()
    return r.report_json


class Report:
    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = file_path
        self.virus_total_api = "https://www.virustotal.com/vtapi/v2/file/{action}"
        self.done = False

    def scan(self):
        with open(self.file_path, "rb") as f:
            scan_response = requests.post(self.virus_total_api.format(action="scan"),
                                          params={"apikey": API_KEY},
                                          files={"file": (self.file_name, f)})
            self.scan_json = scan_response.json()
            self.resource = self.scan_json.get('scan_id')

    def _report(self):
        report_response = requests.post(self.virus_total_api.format(action="report"),
                                        params={"apikey": API_KEY, 'resource': self.resource})
        self.report_json = report_response.json()
        if self.report_json.get('response_code', 0) == 1:
            self.done = True
            logger.info("Got Full Report")

    def report(self):
        logger.info("Scanning File")
        self.scan()
        while not self.done:
            logger.info("Fetching Report")
            time.sleep(1)
            self._report()

from dotenv import load_dotenv
from datetime import datetime
import requests
import json
import os

load_dotenv()

API_URL = os.environ.get("HABITAT_URL")


# There is no reason for this other than it is easier to use
class APITools:
    def current_reading(self):
        return self.get("/reading/current/")

    def add_reading(self, temp=None, hum=None):
        return self.post("/reading/add/", dict(temp=temp, hum=hum))

    def list_readings(self):
        return self.get("/reading/list/")

    def find_reading_by_period(self, unit=None, time=None):
        return self.get("/reading/find/period/", data=dict(unit=unit, time=time))

    def find_reading_by_range(self, dateFrom=None, dateTo=None):
        return self.get(
            "/reading/find/range/", data=dict(dateFrom=dateFrom, dateTo=dateTo)
        )

    def get_config(self):
        return self.get("/config/get/")

    def new_config(self):
        return self.get("/config/new/")

    def get(self, url, data=None):
        if data is not None:
            data = json.dumps(data)

        return requests.get(
            f"{API_URL}{url}",
            json=data,
        ).json()

    def post(self, url, data):
        return requests.post(f"{API_URL}{url}", json=json.dumps(data)).json()


def pretty_datetime(string):
    dt = datetime.strptime(string, "%a, %d %b %Y %H:%M:%S GMT")
    return dt.timestamp()

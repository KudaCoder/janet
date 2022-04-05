from datetime import datetime, time
import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.environ.get("HABITAT_URL")


def convert_dt_to_iso(data: dict):
    for k, v in data.items():
        if isinstance(v, datetime) or isinstance(v, time):
            data[k] = v.isoformat()
    return data


class APITools:
    def current_reading(self):
        return self.get("/reading/current/")

    def add_reading(self, temp=None, hum=None):
        return self.post("/reading/add/", {"temp": temp, "hum": hum})

    def list_readings(self):
        return self.get("/reading/list/")

    def find_reading_by_period(self, unit=None, time=None):
        return self.get("/reading/find/period/", data={"unit": unit, "time": time})

    def find_reading_by_range(self, dateFrom=None, dateTo=None):
        return self.get(
            "/reading/find/range/", data={"dateFrom": dateFrom, "dateTo": dateTo}
        )

    def get_config(self):
        return self.get("/config/get/")

    def new_config(self):
        return self.get("/config/new/")

    def set_config(self, form_data):
        data = form_data
        data = convert_dt_to_iso(data)
        return self.post("/config/set/", data=data)

    def get(self, url, data=None):
        if data is not None:
            data = json.dumps(data)

        return requests.get(
            f"{API_URL}{url}",
            json=data,
        ).json()

    def post(self, url, data):
        return requests.post(f"{API_URL}{url}", json=json.dumps(data)).json()

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

    def set_config(self, form_data):
        data = form_data
        data["lights_on_time"] = data["lights_on_time"].isoformat()
        data["lights_off_time"] = data["lights_off_time"].isoformat()
        # This data is not needed as his will create new config with new
        # created on date, but how best to remove?
        data["created"] = data["created"].isoformat()
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


def iso_to_timestamp(string):
    dt = datetime.fromisoformat(string)
    return dt.timestamp()

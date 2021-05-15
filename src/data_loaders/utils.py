import datetime
import json
import time

import requests
from bs4 import BeautifulSoup


def get_beauiful_soup_object_from_base_url(base_url):
    try:
        page = requests.get(base_url)
        soup = BeautifulSoup(page.content, 'html.parser')
    except ConnectionResetError:
        print("Connection Reset Error! Wait before next request.")
        time.sleep(120)
        page = requests.get(base_url)
        soup = BeautifulSoup(page.content, 'html.parser')

    return soup


def pretty_print(vehicle_rides):
    def converter(obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()

        raise TypeError(f"{type(obj)} not datetime")

    print(json.dumps(vehicle_rides, indent=2, default=converter))

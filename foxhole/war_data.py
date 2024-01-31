import logging
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List

import pytz
import requests
from db import MinutelyDynamicData
from requests import Response

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(levelname)-5s [%(name)-16s]  %(message)s (%(filename)s:%(lineno)d)",
    level=logging.INFO,
    stream=sys.stdout,
)
ROOT_ENDPOINT = "https://war-service-live.foxholeservices.com/api"
WAR_STATE = "/worldconquest/war"
DYNAMIC_MAP_DATA = "/dynamic/public"
MAP_NAMES = "/worldconquest/maps/"
MAP_WAR_REPORT = "/worldconquest/warReport/"
STATIC_MAP_DATA = "/static"


@dataclass
class WarDataEtl:
    map_names: List[str]
    static_map_data: object  # Dict

    def __init__(self) -> None:
        self.map_names = self.fetch_map_names()
        self.static_map_data = self.fetch_static_map_data()

    def run(self) -> None:
        for map in self.map_names:
            to_create = list(self.fetch(map))
            MinutelyDynamicData.bulk_create(to_create)

    def fetch(self, map: str) -> Iterable[MinutelyDynamicData]:
        dynamic_data = self.fetch_dynamic_map_data(map)
        war_report = self.fetch_map_war_report(map)
        yield MinutelyDynamicData(
            map=map.replace("Hex", ""),
            time=datetime.utcnow().replace(tzinfo=pytz.UTC),
            dynamic_data=dynamic_data,
            report=war_report,
        )

    def fetch_war_state(self) -> object:
        logger.info("Fetching data about the current state of the war")
        resp: Response = requests.get(ROOT_ENDPOINT + WAR_STATE)
        assert resp.ok, f"Request error: {resp.status_code!r} - {resp.content!r}"
        return resp.json()

    def fetch_map_names(self) -> List[str]:
        logger.info("Fetching the list of the active World Conquest map names")
        resp: Response = requests.get(ROOT_ENDPOINT + MAP_NAMES)
        assert resp.ok, f"Request error: {resp.status_code!r} - {resp.content!r}"
        return list(resp.json())

    def fetch_map_war_report(self, map: str) -> object:
        logger.info("Fetching map war report")
        resp: Response = requests.get(ROOT_ENDPOINT + MAP_WAR_REPORT + str(map))
        assert resp.ok, f"Request error: {resp.status_code!r} - {resp.content!r}"
        return resp.json()

    def fetch_static_map_data(self) -> object:
        data = {}
        for map in self.map_names:
            logger.info(f"Fetching static map data for {map}")
            resp: Response = requests.get(ROOT_ENDPOINT + MAP_NAMES + map + STATIC_MAP_DATA)
            assert resp.ok, f"Request error: {resp.status_code!r} - {resp.content!r}"
            data[map] = resp.json()
        return data

    def fetch_dynamic_map_data(self, map: str) -> object:
        logger.info(f"Fetching dynamic map data for {map}")
        resp: Response = requests.get(ROOT_ENDPOINT + MAP_NAMES + map + DYNAMIC_MAP_DATA)
        assert resp.ok, f"Request error: {resp.status_code!r} - {resp.content!r}"
        return resp.json()


if __name__ == "__main__":
    WarDataEtl().run()

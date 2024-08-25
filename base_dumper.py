from abc import ABC, abstractmethod
import os
import json
import sys


def is_bluearchive_api(url):
    return is_global_server(url) or is_japan_server(url)


def is_japan_server(url):
    return "prod-game.bluearchiveyostar.com" in url


def is_global_server(url):
    return "bagl.nexon.com" in url


def get_root_path():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(__file__)


class BlueArchiveDumper(ABC):

    def response(self, flow):
        if not is_bluearchive_api(
            flow.request.pretty_url
        ) or not self.is_target_endpoint(flow.request.pretty_url):
            return
        payload = json.loads(flow.response.content)
        if not self.is_target_protocol(payload["protocol"]):
            return
        response = self.transform(json.loads(payload["packet"]))
        ROOT_DIR = get_root_path()
        output_path = os.path.join(ROOT_DIR, "output", f"{self.file_name()}.json")
        self.save_response(response, output_path)

    def save_response(self, response, output_path):
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(response, f, indent=4, ensure_ascii=False)

    @abstractmethod
    def file_name(self):
        pass

    @abstractmethod
    def is_target_endpoint(self, url):
        pass

    @abstractmethod
    def is_target_protocol(self, protocol):
        pass

    @abstractmethod
    def transform(self, protocol, packet):
        pass

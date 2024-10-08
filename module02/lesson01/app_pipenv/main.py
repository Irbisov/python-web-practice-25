from abc import ABC, abstractmethod

import requests
import xmltodict


class Connection(ABC):
    @abstractmethod
    def get_data(self, url):
        pass


class RequestConnection(Connection):
    def __init__(self, request: requests):
        self.request = request

    def get_data(self, url):
        return self.request.get(url)


class ApiClient:
    def __init__(self, fetch: Connection):
        self.fetch = fetch

    def get_xml(self, url):
        response = self.fetch.get_data(url)
        return response.text


def parse_usd(data):
    exc = data.get("exchangerates", None)
    if exc:
        return exc.get("row")[0].get("exchangerate").get("@buy")
    return None


def xml_adapter(xml):
    return dict(xmltodict.parse(xml))


def add(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    client = ApiClient(RequestConnection(requests))
    data = client.get_xml(
        "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11"
    )
    print(parse_usd(xml_adapter(data)))
    print(add(5, 10))

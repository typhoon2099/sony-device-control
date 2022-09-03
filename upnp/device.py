import requests
import urllib
from lxml import etree


class Device:
    NAMESPACES = {
        "u": "urn:schemas-upnp-org:device-1-0",
    }

    def __init__(self, location):
        print(location)
        self.location = location
        self.services = self.__services

    def __services(self):
        output = {}
        try:
            response = requests.get(self.location)
            xml = etree.fromstring(bytes(response.text, encoding="utf8"))
            services = xml.findall(
                "u:device/u:serviceList/u:service",
               namespaces=self.NAMESPACES,
            )

            for service in services:
                service_type = service.find("u:serviceType", namespaces=self.NAMESPACES).text
                domain = service_type.split(":")[1]

                service_name = service.find("u:serviceId", namespaces=self.NAMESPACES).text.split(":")[-1]

                if domain not in service:
                    output[domain] = {}

                control_url = service.find("u:controlURL", namespaces=self.NAMESPACES).text

                output[domain][service_name] = {
                    "url": urllib.parse.urljoin(self.location, control_url),
                }

        except etree.XMLSyntaxError as e:
            print(e)

        return output

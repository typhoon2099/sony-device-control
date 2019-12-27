import requests
import urllib.parse
from lxml import etree


class Ircc(object):
    def __init__(self, host, device_id, device_name):
        self._host = "http://{}".format(host)
        self._device_id = device_id
        self._device_name = device_name
        self._commands = {}
        self.get_remote_command_list()

    def get_remote_command_list(self):
        path = "{}:50002/getRemoteCommandList".format(self._host)
        response = requests.get(path, headers=self.headers())

        for command in etree.fromstring(bytes(response.text, encoding='utf8')).findall("command"):
            if command.attrib["type"] == "ircc":
                self._commands[command.attrib["name"]] = command.attrib["value"]

    def send(self, command):
        try:
            ircc_value = self._commands[command]
        except KeyError:
            print('Command "{}" not found'.format(command))
            raise ValueError


        nsmap = {
            "s": "http://schemas.xmlsoap.org/soap/envelope/",
        }

        root = etree.Element("{%s}Envelope" % nsmap["s"], {
            "{%s}encodingStyle" % nsmap["s"]: "http://schemas.xmlsoap.org/soap/encoding/",
        }, nsmap=nsmap)
        body = etree.SubElement(root, "{%s}Body" % nsmap["s"])
        send_ircc = etree.SubElement(body, "{%s}X_SendIRCC" % "urn:schemas-sony-com:service:IRCC:1", nsmap={
            "u": "urn:schemas-sony-com:service:IRCC:1",
        })
        etree.SubElement(send_ircc, "IRCCCode").text = ircc_value

        xml = str.encode("<?xml version=\"1.0\"?>") + etree.tostring(root)

        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPACTION": '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"',
        }

        response = requests.post(self.__control_url(), headers=headers, data=xml)

        return response.status_code == 200

    def __control_url(self):
        path = "{}:50001/Ircc.xml".format(self._host)
        response = requests.get(path)
        xml = etree.fromstring(bytes(response.text, encoding='utf8'))
        control_url_element = xml.xpath(
            ".//u:serviceType[.='urn:schemas-sony-com:service:IRCC:1']/following-sibling::u:controlURL",
            namespaces={'u': 'urn:schemas-upnp-org:device-1-0'},
        )

        return urllib.parse.urljoin(path, control_url_element[0].text)

    def headers(self):
        return {
            "User-Agent": "Sony Device Control",
            "X-CERS-DEVICE_INFO": self._device_name,
            "X-CERS-DEVICE-ID": self._device_id
        }

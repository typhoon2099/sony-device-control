import requests
import xml.etree.ElementTree as ET


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

        for command in ET.fromstring(response.text).findall("command"):
            if command.attrib["type"] == "ircc":
                name = command.attrib["name"]
                value = command.attrib["value"]
                self._commands[name] = value

    def send(self, command):
        ircc_value = self._commands[command]
        path = "{}:50001/upnp/control/IRCC".format(self._host)

        root = ET.Element("s:Envelope", {
            "xmlns:s": "http://schemas.xmlsoap.org/soap/envelope/",
            "s:encodingStyle": "http://schemas.xmlsoap.org/soap/encoding/",
        })
        body = ET.SubElement(root, "s:Body")
        sendIRCC = ET.SubElement(body, "u:X_SendIRCC", {
            "xmlns:u": "urn:schemas-sony-com:service:IRCC:1",
        })
        irccCode = ET.SubElement(sendIRCC, "IRCCCode")
        irccCode.text = ircc_value

        xml = str.encode("<?xml version=\"1.0\"?>") + ET.tostring(root)

        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPACTION": '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"',
        }

        requests.post(path, headers=headers, data=xml)

    def headers(self):
        return {
            "User-Agent": "Sony Device Control",
            "X-CERS-DEVICE_INFO": self._device_name,
            "X-CERS-DEVICE-ID": self._device_id
        }

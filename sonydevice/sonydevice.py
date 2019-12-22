import requests
import xml.etree.ElementTree as ET


class SonyDevice(object):
    def __init__(self, host, device_id, device_name):
        self._host = "http://{}".format(host)
        self._device_id = device_id
        self._device_name = device_name

    def action_list(self):
        path = "{}:50002/actionList".format(self._host)

        response = requests.get(path, headers=self.headers())
        xml = ET.fromstring(response.text)

        print(xml.findall("actionList action"))
        for action in xml.findall("action"):
            path = action.attrib["url"]

            response = requests.get(path, headers=self.headers())
            print(response.text)

    def connect(self):
        if self.registered():
            return True
        else:
            self.register()
            return False

    def register(self, pin=None):
        path = "{}:50002/register".format(self._host)

        auth = ('', pin) if pin is not None else None

        requests.get(path, params={
            "deviceId": self._device_id,
            "name": self._device_name,
            "registrationType": "initial",
        }, auth=auth, headers=self.headers())

    def renew(self):
        path = "{}:50002/register".format(self._host)

        response = requests.get(path, params={
            "deviceId": self._device_id,
            "name": self._device_name,
            "registrationType": "renewal",
            "wolSupport": "true",
        }, headers=self.headers())

    def registered(self):
        get_status_path = "{}:50002/getStatus".format(self._host)
        response = requests.get(get_status_path, headers=self.headers())

        return response.status_code == 200

    def get_remote_command_list(self):
        path = "{}:50002/getRemoteCommandList".format(self._host)

        response = requests.get(path, headers=self.headers())
        print(response.text)

    def play(self):
        command = "AAAAAwAAHFoAAAA9Aw=="
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
        irccCode.text = command

        xml = str.encode("<?xml version=\"1.0\"?>") + ET.tostring(root)

        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPACTION": '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"',
        }

        response = requests.post(path, headers=headers, data=xml)

    def headers(self):
        return {
            "User-Agent": "Sony Device Control",
            "X-CERS-DEVICE_INFO": self._device_name,
            "X-CERS-DEVICE-ID": self._device_id
        }

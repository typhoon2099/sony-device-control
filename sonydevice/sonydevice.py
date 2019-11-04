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
        print(response.text)
        xml = ET.fromstring(response.text)

        print(xml.findall("actionList action"))
        for action in xml.findall("action"):
            path = action.attrib["url"]
            print(action.attrib["url"])

            response = requests.get(path, headers=self.headers())
            print(response.headers)
            print(response.text)
            print(response.status_code)

    def connect(self):
        if self.registered():
            return True
        else:
            self.register()
            return False

    def register(self, pin=None):
        path = "{}:50002/register".format(self._host)

        auth = ('', pin) if pin is not None else None

        response = requests.get(path, params={
            "deviceId": self._device_id,
            "name": self._device_name,
            "registrationType": "initial",
        }, auth=auth, headers=self.headers())

    def registered(self):
        get_status_path = "{}:50002/getStatus".format(self._host)
        response = requests.get(get_status_path, headers=self.headers())

        return response.status_code == 200

    def get_remote_command_list(self):
        path = "{}:50002/getRemoteCommandList".format(self._host)

        response = requests.get(path, headers=self.headers())
        print(response.headers)
        print(response.text)
        print(response.status_code)

    def play(self):
        path = "{}:52323/upnp/control/IRCC".format(self._host)

        xml = '<?xml version="1.0"?>'\
            '<s:Enveope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">'\
            '<s:Body>'\
            '<u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1">'\
            '<IRCCCode>AAAAAwAAHFoAAAAaAw==</IRCCCode>'\
            '</u:X_SendIRCC>'\
            '</s:Body>'\
            '</s:Envelope>'

        print(xml)

        print(len(xml))

        headers = {
            **self.headers(),
            **{
                "Content-Type": "text/xml",
                "Content-Length": str(len(xml)),
                "charset": "UTF-8",
                "SOAPACTION": "urn:schemas-sony-com:service:IRCC:1#X_SendIRCC",
            }
        }

        print(headers)

        response = requests.post(path, data=xml, headers=headers)
        print(response.headers)
        print(response.text)
        print(response.status_code)

    def headers(self):
        return {
            "User-Agent": "Sony Device Control",
            "X-CERS-DEVICE_INFO": self._device_name,
            "X-CERS-DEVICE-ID": self._device_id
        }

import requests
import urllib.parse
from lxml import etree
from .ircc import Ircc


class SonyDevice(object):
    NAMESPACES = {
        "microsoft": "urn:schemas-microsoft-com:WMPNSS-1-0",
        "u": "urn:schemas-upnp-org:device-1-0",
    }

    def __init__(self, host, device_id, device_name):
        self._host = "http://{}".format(host)
        self._device_id = device_id
        self._device_name = device_name

        if self.registered():
            self.ircc = Ircc(host, device_id, device_name)

    def action_list(self):
        path = "{}:50002/actionList".format(self._host)
        response = requests.get(path, headers=self.headers())

        output = {}
        for action in etree.fromstring(response.text).findall("action"):
            output[action.attrib["name"]] = action.attrib["url"]

        return output
    
    def device_info(self):
        path = "{}:52323/dmr.xml".format(self._host)
        response = requests.get(path, headers=self.headers())
        print(response.text)
        xml = etree.fromstring(bytes(response.text, encoding="utf8"))

        device = xml.find("u:device", namespaces=self.NAMESPACES)

        def url_path(x):
            return urllib.parse.urljoin(path, x.text)

        output = {
            "udn": device.find("u:UDN", namespaces=self.NAMESPACES).text,
            "friendly_name": device.find("u:friendlyName", namespaces=self.NAMESPACES).text,
            "model_name": device.find("u:modelName", namespaces=self.NAMESPACES).text,
            "model_number": device.find("u:modelName", namespaces=self.NAMESPACES).text,
            "manufacturer": device.find("u:manufacturer", namespaces=self.NAMESPACES).text,
            "icons": list(map(url_path, device.findall("u:iconList/u:icon/u:url", namespaces=self.NAMESPACES))),
            "wol": device.find("microsoft:magicPacketWakeSupported", namespaces=self.NAMESPACES).text.strip() == '1',
        }

        return output

    def get_text(self):
        path = "{}:50002/getText".format(self._host)
        response = requests.get(path, headers=self.headers())

        if response.status_code == 200:
            return True

        print("Text input not available, no text input screen is displayed.")
        return False

    def send_text(self, text):
        if self.get_text():
            path = "{}:50002/sendText?text={}".format(self._host, text)

            response = requests.get(path, headers=self.headers())
            return response.status_code == 200

    def get_content_information(self):
        path = "{}:50002/getContentInformation".format(self._host)

        response = requests.get(path, headers=self.headers())

        output = {
            "status": response.headers["X-CERS-STATUS-CODE"],
        }

        for info_item in etree.fromstring(response.text).findall("infoItem"):
            output[info_item.attrib["field"]] = info_item.attrib["value"]

        return output

    def get_system_information(self):
        path = "{}:50002/getSystemInformation".format(self._host)

        response = requests.get(path)
        print(response.text)

    def get_status(self):
        path = "{}:50002/getStatus".format(self._host)

        response = requests.get(path, headers=self.headers())
        return response.text

    # def get_history_list(self):
    #     path = "{}:50002/getHistoryList".format(self._host)
    # 
    #     response = requests.get(path, headers=self.headers())
    #     print(response.text)
    #     print(response.status_code)
    #     print(response.headers)

    def registered(self):
        return self.renew()

    def register(self, pin=None):
        path = "{}:50002/register".format(self._host)

        auth = ('', pin) if pin is not None else None

        try:
            response = requests.get(path, params={
                "deviceId": self._device_id,
                "name": self._device_name,
                "registrationType": "initial",
                "wolSupport": "true",
            }, auth=auth, headers=self.headers())
        except requests.ConnectionError:
            print("Connection Error")
            return False

        return response.status_code == 200

    def renew(self):
        path = "{}:50002/register".format(self._host)

        try:
            response = requests.get(path, params={
                "deviceId": self._device_id,
                "name": self._device_name,
                "registrationType": "renewal",
                "wolSupport": "true",
            }, headers=self.headers())
        except requests.ConnectionError:
            print("Connection Error")
            return False

        return response.status_code == 200

    def headers(self):
        return {
            "User-Agent": "Sony Device Control",
            "X-CERS-DEVICE_INFO": self._device_name,
            "X-CERS-DEVICE-ID": self._device_id
        }

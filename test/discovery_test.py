from sonydevice.discovery import Discovery
from mock import patch


def test_finds_services():
    with patch('requests.get') as mock_request:
        mock_request.return_value.status_code = 200
        with open('./test/tv.xml', 'r') as file:
            mock_request.return_value.text = file.read()

        services = Discovery.find_services("http://192.168.1.68:52323/dmr.xml")

    expected = {
        "schemas-upnp-org": {
            "RenderingControl": {
                "url": "http://192.168.1.68:52323/upnp/control/RenderingControl",
            },
            "ConnectionManager": {
                "url": "http://192.168.1.68:52323/upnp/control/ConnectionManager",
            },
            "AVTransport": {
                "url": "http://192.168.1.68:52323/upnp/control/AVTransport",
            },
        },
        "dial-multiscreen-org": {
            "dial": {
              "url": "http://192.168.1.68:52323/upnp/control/DIAL",
            },
        },
        "schemas-sony-com": {
            "IRCC": {
                "url": "http://192.168.1.68/sony/IRCC",
            },
            "ScalarWebAPI": {
                "url": "http://192.168.1.68:52323/upnp/control/ScalarAPI",
            },
        },
    }

    assert services == expected

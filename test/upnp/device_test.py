from upnp.device import Device
from mock import patch


def test_finds_services():
    with patch('requests.get') as mock_request:
        mock_request.return_value.status_code = 200
        with open('./test/tv.xml', 'r') as file:
            mock_request.return_value.text = file.read()

        services = Device("http://192.168.1.68:52323/dmr.xml").services()


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
                "codeList": {
                    "Power": "AAAAAQAAAAEAAAAVAw==",
                    "Power On": "AAAAAQAAAAEAAAAuAw==",
                    "Power OFF": "AAAAAQAAAAEAAAAvAw==",
                }
            },
            "ScalarWebAPI": {
                "Version": 1.0,
                "url": "http://192.168.1.68:52323/upnp/control/ScalarAPI",
                "BaseUrl": "http://192.168.1.68/sony",
                "ServiceList": {"guide", "system", "videoScreen", "audio", "avContent", "recording", "appControl",
                                "browser", "notification", "cec", "accessControl", "encryption"},
            },
            "StandardDMR": 1.1,
            "MaxBGMCount": 64,
            "ScreenResolution": "2k",
            "TrackID": {
                "BaseURL": "http://192.168.1.68/sony/BgmSearch",
            },
            "DIALEX": {
                "AppsListURL": "http://192.168.1.68/DIAL/sony/applist",
                "DeviceID": "B0:00:03:A7:6F:23",
                "DeviceType": "CoreTV_DIAL",
            },
            "RDIS": {
              "Version": 1.0,
              "SessionControl": False,
              "EntryPort": 20677,
            },
        },
    }
    print(services)
    print("=====")
    print(expected)

    assert services == expected

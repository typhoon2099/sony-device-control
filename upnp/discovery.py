import socket
import struct
import re
import requests
import urllib.parse
from lxml import etree
from upnp.device import Device


class Discovery(object):
    MULTICAST_IP = '239.255.255.250'
    MULTICAST_PORT = 1900
    MULTICAST_GROUP = (MULTICAST_IP, MULTICAST_PORT)
    NAMESPACES = {
        "u": "urn:schemas-upnp-org:device-1-0",
    }

    @classmethod
    def find_devices(cls):
        message = "\r\n".join([
            "M-SEARCH * HTTP/1.1",
            "HOST: 239.255.255.250:1900",
            "MAN: \"ssdp:discover\"",
            "MX: 2",
            "ST: ssdp:all",
            "USER-AGENT: SonyDevice/1.0",
            "",
            "",
        ])

        sock = Discovery.ssdp_socket()

        devices = []

        sock.sendto(bytes(message, encoding="utf8"), Discovery.MULTICAST_GROUP)

        while True:
            try:
                data = sock.recvfrom(1024)

                ip = data[1][0]
                message = data[0].decode("utf-8")

                headers = dict()
                # Ignore the first line (it's not a header)
                for header in message.splitlines()[1:]:
                    if header == '':
                        continue
                    key, value = header.split(":", 1)
                    headers[key] = value.strip()

                devices.append(headers['LOCATION'])

            except socket.error:
                break

        sock.close()

        output = list()
        for location in set(devices):
            output.append(Device(location))

        return output


    @classmethod
    def ssdp_socket(cls):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        group = socket.inet_aton(Discovery.MULTICAST_IP)
        mreq = struct.pack('=4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        sock.settimeout(5)
        # sock.bind(Discovery.MULTICAST_GROUP)

        return sock

    def __init__(self, proto="ipv4", port=1900, ttl=2, iface=None, timeout=5, address=None, *args, **kwargs):
        allowed_protos = ("ipv4", "ipv6")
        if proto not in allowed_protos:
            raise ValueError("Invalid proto - expected one of {}".format(allowed_protos))
        self.port = port
        if proto == "ipv4":
            af_type = socket.AF_INET
            self.broadcast_ip = ipv4_multicast_ip
            self._address = (self.broadcast_ip, port)
        elif proto == "ipv6":
            af_type = socket.AF_INET6
            self.broadcast_ip = ipv6_multicast_ip  # TODO: Support other ipv6 multicasts
            self._address = (self.broadcast_ip, port, 0, 0)
        self.sock = socket.socket(af_type, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if (WINDOWS or MACOSX) and proto == "ipv6":
            self.sock.setsockopt(IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl)
            self.sock.setsockopt(IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 1)
        else:
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        self.sock.settimeout(timeout)

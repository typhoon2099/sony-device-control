import socket
import struct
import re


class Discovery(object):
    MULTICAST_IP = '239.255.255.250'
    MULTICAST_PORT = 1900
    MULTICAST_GROUP = (MULTICAST_IP, MULTICAST_PORT)

    @classmethod
    def find_devices(cls):
        message = """M-SEARCH * HTTP/1.1
HOST: 239.255.255.250:1900
MAN: "ssdp:discover"
ST: urn:schemas-sony-com:service:IRCC:1
MX: 1
USER-AGENT: SonyDevice/1.0
"""

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.bind(Discovery.MULTICAST_GROUP)
        sock.settimeout(0.2)

        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except AttributeError:
            pass

        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        group = socket.inet_aton(Discovery.MULTICAST_IP)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        devices = {}

        try:
            sock.sendto(bytes(message, encoding="utf8"), Discovery.MULTICAST_GROUP)

            while True:
                try:
                    data = sock.recvmsg(1024)
                    ip = data[3][0]
                    message = data[0].decode()

                    location = re.findall("LOCATION: (.*)", message)

                    if len(location) == 0:
                        continue

                    if ip not in devices:
                        devices[ip] = set()

                    devices[ip].add(location[0].strip())

                except socket.error:
                    pass
        finally:
            sock.close()

            return devices

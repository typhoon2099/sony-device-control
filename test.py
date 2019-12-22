from sonydevice.sonydevice import SonyDevice

device = SonyDevice("192.168.1.138", "Device ID", "Device Name")

if device.connect():
    device.get_remote_command_list()
    device.action_list()
    device.play()
else:
    pin = input("PIN: ")
    device.register(pin)

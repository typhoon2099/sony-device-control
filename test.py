from sonydevice.sonydevice import SonyDevice

device = SonyDevice("192.168.1.138", "Device ID", "Device Name")

if device.connect():
    # device.action_list()
    device.ircc.send("Play")
    # device.ircc.send("NotRealAction")
else:
    pin = input("PIN: ")
    device.register(pin)

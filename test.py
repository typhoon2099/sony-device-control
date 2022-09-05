from sonydevice.sonydevice import SonyDevice

device = SonyDevice("192.168.1.38", "Device ID", "Device Name")
print(device.device_info())

if device.registered():
    #device.action_list()
    device.ircc.send("Play")
    #device.ircc.send("NotRealAction")
else:
    device.register()
    pin = input("PIN: ")
    device.register(pin)

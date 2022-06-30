# Fir client.
# Copyright (c) 2022 bellrise <bellrise.dev@gmail.com>

from . import device


class Client:
    """Fir client. Controls the setup & pairing of devices, along with
    allowing the user to issue commands to the paired devices. """

    devices: list = []

    def add_device(self, addr: str, port: int):
        """Adds a device with the given address & port to the device list.
        If connecting fails, a ConnectionError is raised. """
        d = device.Device(addr, port)
        d.pair()
        devices.append(d)

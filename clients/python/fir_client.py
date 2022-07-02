# Fir client.
# Copyright (c) 2022 bellrise <bellrise.dev@gmail.com>

from libfir import device, protocol, ScanResult
from typing import List
import libfir
import socket


class Client:
    # Fir client. Controls the setup & pairing of devices, along with
    # allowing the user to issue commands to the paired devices. A user
    # interface is built into these methods, so calling these functions may
    # require user IO.

    known_devices: List[ScanResult] = []
    paired: List[device.Device] = []
    local_sock: socket.socket = None
    status: str = 'offline'

    # Network settings
    ip: str = '0.0.0.0'
    mask: int = 24

    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())

    def add_device(self, addr: str, port: int):
        # Adds a device with the given address & port to the device list.
        # If connecting fails, a ConnectionError is raised.
        d = device.Device(addr, port)
        d.pair()
        devices.append(d)

    def scan(self, port: int = protocol.FIR_PORT, do_log=False):
        # Scan the local network for open Fir clients. Uses the libfir.scan()
        # to do all the heavy work.
        results = libfir.scan(port, do_log)
        found = [x for x in results if x]

        print('Scanned %d devices, found ' % len(results), end='')
        if found:
            print('\033[92m%d\033[0m open.' % len(found))
        else:
            print('\033[91mnone\033[0m open.')

        self.known_devices = found

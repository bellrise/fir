# Fir device used by the client.
# Copyright (c) 2022 bellrise <bellrise.dev@gmail.com>

from typing import Optional
import socket

__all__ = ["Device"]


class Device:
    """Represents a single device a client can send commands to. This class
    handles the connection setup & communication using a socket. To pair with
    another Fir client, define a new device & call .pair() on it, like so:

        d = Device('192.168.1.2', 7708)
        try:
            d.pair()
        except ConnectionError as e:
            ...

    If pairing fails, a ConnectionError is raised. """

    name: str = '???'
    addr: str = ''
    port: int = 0

    is_paired = False
    sock: socket.socket = None

    def __init__(self, addr: str, port: int):
        """Set up a new device with the given address & port. """
        self.addr = addr
        self.port = port

    def pair(self):
        """Try pairing with the device. This connects this host to the device,
        so no other devices can use it. """
        raise NotImplemented('pairing with devices')

    def ping(self) -> Optional[tuple]:
        """Ping the device, even if not paired. The pinged device should return
        its chosen name, which is then automatically assigned to the `name`
        field in this class. """
        if self.is_paired:
            raise NotImplemented('ping when paired')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        try:
            sock.connect((self.addr, self.port))
        except OSError:
            return None

        sock.close()

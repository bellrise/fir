# Fir device used by the client.
# Copyright (c) 2022 bellrise <bellrise.dev@gmail.com>

import socket


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
        """Try pairing with the device. """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        try:
            self.sock.connect((self.addr, self.port))
        except OSError:
            raise ConnectionError('no route to host %s:%d' \
                    % (self.addr, self.port))

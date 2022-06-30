# libfir utils can be found in this file
# Copyright (c) 2022 bellrise <bellrise.dev@gmail.com>

from typing import Optional, List
import concurrent.futures
import socket


class ScanResult:
    """This is returned from scan(). Contains the IPv4 address, the port on
    which the open Fir client has been found and the device name that the
    Fir client declared. """

    name: str = None
    addr: str = None
    port: int = 0

    def __init__(self, name: str, addr: str, port: int):
        self.name = name
        self.addr = addr
        self.port = port

    def __str__(self) -> str:
        return '<%s %s:%d>' % (self.name, self.addr, self.port)


def __scan_one(args) -> Optional[ScanResult]:
    addr, port, do_log = args
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.settimeout(10)
    if do_log:
        print('\033[90mScanning %s:%d\033[0m' % (addr, port))
    try:
        sock.connect((addr, port))
        sock.close()
        return ScanResult('<name>', addr, port)
    except (OSError, KeyboardInterrupt):
        return None


def scan(port: int, do_log=False) -> List[ScanResult]:
    """Scan the local network for open Fir clients on the given port.
    Currently only scans all user addresses in the range of the /24
    network mask. Returns a list of ScanResults. """

    local_ip = socket.gethostbyname(socket.gethostname())
    a, b, c, d = local_ip.split('.')

    args = []
    for i in range(2, 255):
        # Skip ourselfs
        if i == d:
            continue
        ip = '%s.%s.%s.%d' % (a, b, c, i)
        args.append((ip, port, do_log))

    with concurrent.futures.ThreadPoolExecutor(32) as executor:
        results = executor.map(__scan_one, args)

    real_res = []
    for res in results:
        if res:
            real_res.append(res)

    return res

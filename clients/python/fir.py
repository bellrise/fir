#!/usr/bin/python3
# Fir client based around a command-line interface.
# Copyright (c) 2022 bellrise <bellrise.dev@gmail.com>

from libfir import device, protocol as prot
from typing import Optional, Union
import fir_client
import libfir
import string
import socket


__version__ = '0.0.1'


_client: fir_client.Client = None


def error(*strs):
    """Print an error message. """
    strs = ' '.join([str(x) for x in strs])
    print('\033[91merror:\033[0m ' + strs)


def validate_port(port: Union[str, int]) -> Optional[int]:
    """Validate the given port and return the correct port or None
    if something is invalid. """

    if isinstance(port, str):
        if not port:
            return None
        if not port.isnumeric():
            error(f'invalid port `{args}`: should be a number')
            return None
        port = int(args)

    if port <= 0 or port >= 65535:
        error(f'invalid port `{port}`: ports are in the 0 < port < 65535 range')
        return None

    return port


def scan(args: str):
    """Scan the local network for open devices. """
    port = validate_port(args) if args else prot.FIR_PORT
    if not port:
        return
    _client.scan(port)


def ping(args: str):
    # ping <addr> [port]
    if not args:
        error('missing `addr` argument')
        return
    args = args.split()
    if len(args) > 1:
        port = args[1]
    else:
        port = prot.FIR_PORT
    addr = args[0]

    # Setup a temporary connection with the device, and then send a ping.

    d = device.Device(addr, port)
    try:
        d.pair()
    except ConnectionError:
        error('Cannot ping device, no connection')
        return


def usage():
    print('Available commands:\n')
    print(
        'help               show this page',
        'scan [port]        scan the local network for open Fir clients '
        f'on the given port (default: {prot.FIR_PORT})',
        'ping <addr> [port] ping the given address on the port (default: '
        f'{prot.FIR_PORT})',
        sep='\n'
    )


def run_cmd(cmd):
    cmd = cmd.split(maxsplit=1)
    if len(cmd) > 1:
        cmd, args = cmd
    else:
        cmd = cmd[0]
        args = None

    callmap = {
        'help': (usage, ()),
        'scan': (scan, (args, )),
        'ping': (ping, (args, ))
    }

    if cmd in callmap:
        callmap[cmd][0](*callmap[cmd][1])
    else:
        error(f'Unknown command `{cmd}`, try `help`')


def main():
    global _client
    _client = fir_client.Client()

    print(f'\033[1;98mFir client {__version__}\033[0m')
    print(f'\033[90mClient IP: {_client._get_local_ip()}\033[0m')
    print(f'\033[90mDefault port: {prot.FIR_PORT}\033[0m')
    print(f'\033[90mProtocol ver: {prot.FIR_PROT_VER}\033[0m')

    while True:
        try:
            s = _client.status
            if s == 'offline':
                s = '\033[90moffline\033[0m'
            if s == 'open':
                s = '\033[96mopen\033[0m'
            if s == 'paired':
                s = '\033[92mpaired\033[0m'
            cmd = input(f'[{s}] ')
            run_cmd(cmd)
        except (KeyboardInterrupt, EOFError):
            print()
            break


main()

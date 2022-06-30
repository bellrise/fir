#!/usr/bin/python3
# Fir client based around a command-line interface.
# Copyright (c) 2022 bellrise <bellrise.dev@gmail.com>

from libfir import client, device, protocol as prot
import libfir
import string
import socket


__version__ = '0.0.1'


global_status: str = '\033[90moffline\033[0m'
global_client: client.Client = None


def get_local_ip() -> str:
    """Returns the local interface IPv4 address. """
    return socket.gethostbyname(socket.gethostname())


def error(*strs):
    """Print an error message. """
    strs = ' '.join([str(x) for x in strs])
    print('\033[91merror:\033[0m ' + strs)


def open_device(args: str):
    # TODO: open the device
    print(args)


def scan(args: str):
    if not args:
        args = prot.FIR_PORT
    elif not args.isnumeric():
        error(f'invalid port `{args}`: should be a number')
        return

    port = int(args)
    if port <= 0 or port >= 65535:
        error(f'invalid port `{port}`: ports are in the 0 < port < 65535 range')
        return

    print('Scanning ...')
    results = libfir.scan(port)

    if not results:
        print('No open devices found')
    else:
        print(f'Found {len(results)} devices')
        for res in results:
            print(res)


def ping(args: str):
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
        'open [port]        open a port for others to connect (default: '
        f'{prot.FIR_PORT})',
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
        'open': (open_device, (args, )),
        'scan': (scan, (args, )),
        'ping': (ping, (args, ))
    }

    if cmd in callmap:
        callmap[cmd][0](*callmap[cmd][1])
    else:
        error(f'Unknown command `{cmd}`, try `help`')

def main():
    global global_client

    print(f'\033[1;98mFir client {__version__}\033[0m')
    print(f'\033[90mClient IP: {get_local_ip()}\033[0m')
    print(f'\033[90mDefault port: {prot.FIR_PORT}\033[0m')
    print(f'\033[90mProtocol ver: {prot.FIR_PROT_VER}\033[0m')

    global_client = client.Client()

    while True:
        try:
            cmd = input(f'[{global_status}] ')
            run_cmd(cmd)
        except (KeyboardInterrupt, EOFError):
            print()
            break


main()

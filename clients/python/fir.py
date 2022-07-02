#!/usr/bin/python3
# Fir client based around a command-line interface.
# Copyright (c) 2022 bellrise <bellrise.dev@gmail.com>

from libfir import device, protocol as prot
from typing import Optional, List
import fir_client
import termios
import libfir
import string
import socket
import string
import sys


__version__ = '0.0.1'


class Shell:
    # Run a shell for the user. This is better than the default input() offered
    # by Python, because it contains more functionality like command history and
    # autocomplete.

    client: fir_client.Client
    valid_chars = string.ascii_letters + string.punctuation + string.digits \
            + ' '

    default_ps1 = '\033[93m#\033[0m '

    CMD_OK = 0
    CMD_ERR = 1
    CMD_EXIT = 2

    def __init__(self):
        self.ps1 = self.default_ps1
        self.client = fir_client.Client()
        self._stdin_attr = None

    def run(self):
        # Run the shell.
        self.welcome()
        self._enable_raw_stdin()

        while True:
            args = self._collect_line()
            if args is None:
                break
            cmd = getattr(self, '_command_%s' % args[0], self.on_unknown)
            cmd_code = cmd(args)
            if cmd_code == Shell.CMD_EXIT:
                break

        self._reset_stdin()

    def on_unknown(self, args: list) -> int:
        self.error('Unknown command `%s`' % args[0])
        return Shell.CMD_ERR

    def _command_help(self, args: list) -> int:
        """show this page"""
        print('Available commands:\n')

        # automatically generate the help page from docstrings
        for obj in dir(self):
            if not obj.startswith('_command'):
                continue
            name = obj.lstrip('_command')
            desc = getattr(self, obj).__doc__
            print('\033[96m%s\033[0m%s%s' % (name, ' ' * (16-len(name)), desc))

        return Shell.CMD_OK

    def _command_exit(self, args: list) -> int:
        """exit the client"""
        return Shell.CMD_EXIT

    def _autocomplete(self, args: list) -> List[str]:
        # Return a list of possible completions given the argument list.
        progs = ('help', 'exit')

    def _collect_line(self) -> Optional[list]:
        # Collect a line from the user, and return an argument list or None.

        buf = ''
        ptr = 0
        sys.stdout.write(self.ps1)
        sys.stdout.flush()

        def redraw():
            sys.stdout.write('\033[1K\033[2K\r' + self.ps1 + buf)
            if len(buf) - ptr != 0:
                sys.stdout.write('\033[%dD' % (len(buf) - ptr))

        while True:
            try:
                c = sys.stdin.read(1)
            except KeyboardInterrupt:
                print('\nExited')
                return None

            if c == '\x0c':
                # ^L clear screen
                sys.stdout.write('\033[2J\033[0;0H')
                redraw()

            if c == '\x17':
                # ^W remove last word
                wd = len(buf[:ptr]) - len(buf[:ptr].rstrip())
                s = buf[:ptr]
                if s:
                    ws = buf[:ptr].rstrip().split()
                    ndel = len(ws[-1]) + wd
                    to_del = buf[ptr-ndel:ptr]
                    to_keep = buf[:ptr-ndel] + buf[ptr:]
                    buf = to_keep
                    ptr -= ndel
                redraw()

            if c == '\x1b':
                # escape chars
                f = sys.stdin.read(1)
                if sys.stdin.readable():
                    # arrows
                    ar = sys.stdin.read(1)
                    if ar == '1':
                        # ctrl+arrow (linux st-256color)
                        d = sys.stdin.read(3)[2]
                        if d == 'C':
                            # ^-> move forward word
                            words = buf[ptr:].split()
                            if len(words) > 1:
                                wd = buf[ptr:].index(words[1])
                            else:
                                wd = len(buf) - ptr
                            ptr += wd
                        if d == 'D':
                            # ^<- move back word
                            wd = len(buf[:ptr]) - len(buf[:ptr].rstrip())
                            s = buf[:ptr].rstrip().split(' ')
                            if s:
                                move = len(s[-1]) + wd
                                ptr -= move
                    if ar == 'C':
                        # -> forward
                        if ptr < len(buf):
                            ptr += 1
                    if ar == 'D':
                        # <- back
                        if ptr > 0:
                            ptr -= 1
                redraw()

            if c == '\x7f' or c == '\x08':
                # backspace
                if ptr > 0:
                    ptr -= 1
                    buf = buf[:ptr] + buf[ptr+1:]
                    redraw()

            if c == '\r' or c == '\n':
                sys.stdout.write('\r\n')
                sys.stdout.flush()
                break

            if c in Shell.valid_chars:
                sys.stdout.write(c)
                # edit in-line
                if ptr < len(buf):
                    tmp = list(buf)
                    tmp.insert(ptr, c)
                    buf = ''.join(tmp)
                    ptr += 1
                    redraw()
                else:
                    buf += c
                    ptr += 1

            sys.stdout.flush()

        return buf.split()

    @staticmethod
    def error(*strs):
        strs = ' '.join([str(x) for x in strs])
        print('\033[91merror:\033[0m ' + strs)

    def welcome(self):
        print('\033[1;97mFir client %s\033[0m' % __version__)
        print('Client address:', self.client.ip)
        print('Network mask: assuming /%d' % self.client.mask)
        print('Scan port:', prot.FIR_PORT)
        print('\nType `help` for available commands')

    @staticmethod
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

    def _enable_raw_stdin(self):
        # Enable raw mode for stdin, allowing for better control over the shell.
        fd = sys.stdin.fileno()
        self._stdin_attr = termios.tcgetattr(fd)
        attrs = self._stdin_attr.copy()
        attrs[3] &= ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(fd, termios.TCSANOW, attrs)

    def _reset_stdin(self):
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, self._stdin_attr)


Shell().run()

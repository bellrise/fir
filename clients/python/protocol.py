# Fir Protocol definitions
# This is a Python version of the fir.h header found in /include.
# Copyright (c) 2022 bellrise

import struct


# The Fir Protocol listens on this port.
FIR_PORT = 7708


# Header size.
FIR_HEADER_SIZE = 16


# Packet version, which is the same as the protocol version.
FIR_PROT_VER = 1


# Packet type.
FIR_PING = 0
FIR_ERR  = 1
FIR_RAW  = 2


# Payload type.
FIR_PAYLOAD_RAW = 0


class PacketHeader:
    # Represents a packet header. Uses the `struct` module to pack the data
    # into a single stream of bytes. Supports version 1.

    __ver: int = FIR_PROT_VER
    __type: int = 0
    __time: int = 0
    __size: int = 0
    __ptype: int = 0

    def __init__(self, buf: bytes = None):
        # Create the class, and if `buf` is given, read the header from there.
        if buf and len(buf) < FIR_HEADER_SIZE:
            raise BufferError(f'buffer too small (<{FIR_HEADER_SIZE} bytes)')
        stuff = struct.unpack('!HHHHB7p', buf)
        if len(stuff) < 5:
            raise BufferError('failed to unpack buffer')

        # Assign stuff to the class
        self.__ver, self.__type, self.__time, self.__size, self.__ptype
            = stuff[:5]

    def as_bytes(self) -> bytes:
        # Returns the header in byte form.
        buf = struct.pack('!HHHHB7p', self.__ver, self.__type, self.__time,
                self.__size, self.__ptype, b'\0' * 7)
        if len(buf) != FIR_HEADER_SIZE:
            raise BufferError('failed to pack header, invalid length')

#!/usr/bin/env python3

import argparse
import logging
from collections import namedtuple
import struct
import socket

log = logging.getLogger("rcon")

SERVERDATA_AUTH = 3
SERVERDATA_AUTH_RESPONSE = 2
SERVERDATA_EXECCOMMAND = 2
SERVERDATA_RESPONSE_VALUE = 0

RCONCommand = namedtuple('RCONCommand', ['host', 'port', 'password', 'command'])


class InvalidPacketException(Exception):
    pass


class CommandFailure(Exception):
    pass


class RCON():
    @staticmethod
    def _encode_packet(f_id: int, f_type: int, f_body: str) -> bytes:
        b_body = f_body.encode("utf-8") + b"\x00"
        data = struct.pack(f"<ii{len(b_body)}sc", f_id, f_type, b_body, b"\x00")
        data = struct.pack("<i", len(data)) + data
        return data

    @staticmethod
    def _decode_packet(data: bytes) -> (int, int, int, str):
        if len(data) < 14:
            raise InvalidPacketException("packet size < 14")
        (f_size,) = struct.unpack("<i", data[:4])
        if len(data[4:]) != f_size:
            raise InvalidPacketException(f"packet size < f_size({f_size})")
        f_id, f_type = struct.unpack("<ii", data[4:12])
        f_body = data[12:len(data)-2].decode("utf-8")
        return f_size, f_id, f_type, f_body

    def __init__(self, host, port):
        self._connection = socket.create_connection((host, port))
        self.i = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()

    def _send_packet(self, f_id, f_type, f_body):
        self._connection.sendall(self._encode_packet(f_id, f_type, f_body))

    def _recv_packet(self) -> (int, int, int, str):
        data = self._connection.recv(4)
        (f_size,) = struct.unpack("<i", data)
        data += self._connection.recv(f_size)
        return self._decode_packet(data)

    def get_i(self) -> int:
        i = self.i
        self.i += 1
        return i

    def login(self, password) -> bool:
        i = self.get_i()
        self._send_packet(i, SERVERDATA_AUTH, password)
        r_size, r_id, r_type, r_body = self._recv_packet()
        if r_type == SERVERDATA_AUTH_RESPONSE and r_id == i:
            return True
        else:
            log.critical("RCON: login failure")
            return False

    def command(self, command: str) -> bool:
        i = self.get_i()
        self._send_packet(i, SERVERDATA_EXECCOMMAND, command)
        r_size, r_id, r_type, r_body = self._recv_packet()
        if r_type == SERVERDATA_RESPONSE_VALUE and r_id == i:
            log.info(r_body)
            return True
        else:
            return False


def get_args() -> RCONCommand:
    parser = argparse.ArgumentParser(description="Send commands using rcon.")
    parser.add_argument("host")
    parser.add_argument("port", type=int)
    parser.add_argument("password")
    parser.add_argument("command")
    args = parser.parse_args()
    command = RCONCommand(
        host=args.host,
        port=args.port,
        password=args.password,
        command=args.command,
    )
    return command


if __name__ == '__main__':
    command = get_args()
    try:
        with RCON(command.host, command.port) as conn:
            if conn.login(command.password):
                if not conn.command(command.command):
                    raise CommandFailure("command failure")
        exit(0)
    except Exception as e:
        print(type(e))
        log.critical(f"RCON: {e}")
        exit(1)

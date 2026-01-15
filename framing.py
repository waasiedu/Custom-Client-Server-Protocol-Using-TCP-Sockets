import socket
import struct
from .protocol import Frame

# Header: 4-byte length + 1-byte type
HEADER_STRUCT = struct.Struct("!IB")
HEADER_LEN = HEADER_STRUCT.size  # 5 bytes

MAX_FRAME_SIZE = 8 * 1024 * 1024  # 8 MB safety limit


class FramingError(Exception):
    pass


def read_exact(sock: socket.socket, n: int) -> bytes:
    """Read exactly n bytes from a TCP socket."""
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise FramingError("Connection closed during read")
        data += chunk
    return data


def send_frame(sock: socket.socket, frame: Frame) -> None:
    header = HEADER_STRUCT.pack(len(frame.payload), frame.msg_type)
    sock.sendall(header + frame.payload)


def recv_frame(sock: socket.socket) -> Frame:
    header = read_exact(sock, HEADER_LEN)
    length, msg_type = HEADER_STRUCT.unpack(header)

    if length > MAX_FRAME_SIZE:
        raise FramingError(f"Frame too large: {length} bytes")

    payload = read_exact(sock, length) if length > 0 else b""
    return Frame(msg_type, payload)

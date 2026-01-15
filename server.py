import argparse
import socket
import threading
import time

from .framing import recv_frame, send_frame, FramingError
from .protocol import Frame, TEXT, PING, PONG, DATA, ACK, TYPE_NAMES


def log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def handle_client(conn: socket.socket, addr):
    log(f"Connected: {addr}")
    conn.settimeout(30)

    try:
        while True:
            frame = recv_frame(conn)
            name = TYPE_NAMES.get(frame.msg_type, hex(frame.msg_type))
            log(f"Received {name} ({len(frame.payload)} bytes)")

            if frame.msg_type == PING:
                send_frame(conn, Frame(PONG, frame.payload))
            elif frame.msg_type in (TEXT, DATA):
                ack = f"ACK {len(frame.payload)} bytes".encode()
                send_frame(conn, Frame(ACK, ack))
            else:
                send_frame(conn, Frame(ACK, b"ACK"))
    except (FramingError, socket.timeout, ConnectionResetError):
        log(f"Disconnected: {addr}")
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9000)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((args.host, args.port))
        s.listen()

        log(f"Listening on {args.host}:{args.port}")

        while True:
            conn, addr = s.accept()
            threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            ).start()


if __name__ == "__main__":
    main()

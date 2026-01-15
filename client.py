import argparse
import socket
import time

from .framing import send_frame, recv_frame
from .protocol import Frame, TEXT, TYPE_NAMES


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--message", default="hello")
    args = parser.parse_args()

    payload = args.message.encode()

    with socket.create_connection((args.host, args.port), timeout=5) as sock:
        t0 = time.perf_counter()
        send_frame(sock, Frame(TEXT, payload))
        response = recv_frame(sock)
        rtt = (time.perf_counter() - t0) * 1000

        name = TYPE_NAMES.get(response.msg_type, hex(response.msg_type))
        print(f"Response: {name}, payload={response.payload!r}")
        print(f"RTT: {rtt:.3f} ms")


if __name__ == "__main__":
    main()

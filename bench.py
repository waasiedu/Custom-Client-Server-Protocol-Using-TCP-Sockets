import argparse
import socket
import statistics
import time

from .framing import send_frame, recv_frame
from .protocol import Frame, PING, DATA, PONG, ACK


def percentile(values, p):
    values = sorted(values)
    k = (len(values) - 1) * (p / 100)
    f = int(k)
    c = min(f + 1, len(values) - 1)
    if f == c:
        return values[f]
    return values[f] + (values[c] - values[f]) * (k - f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--iters", type=int, default=200)
    parser.add_argument("--sizes", type=int, nargs="+",
                        default=[64, 256, 1024, 4096, 16384])
    args = parser.parse_args()

    with socket.create_connection((args.host, args.port), timeout=5) as sock:
        # Latency
        rtts = []
        for _ in range(args.iters):
            t0 = time.perf_counter()
            send_frame(sock, Frame(PING, b""))
            resp = recv_frame(sock)
            assert resp.msg_type == PONG
            rtts.append((time.perf_counter() - t0) * 1000)

        print("Latency (ms):")
        print(f"  median: {statistics.median(rtts):.3f}")
        print(f"  p95:    {percentile(rtts, 95):.3f}")

        # Throughput
        print("\nThroughput (MiB/s):")
        for size in args.sizes:
            payload = b"x" * size
            total = 0
            t0 = time.perf_counter()
            for _ in range(args.iters):
                send_frame(sock, Frame(DATA, payload))
                resp = recv_frame(sock)
                assert resp.msg_type == ACK
                total += size
            dt = time.perf_counter() - t0
            mibps = (total / (1024 * 1024)) / dt
            print(f"  {size:6d} bytes → {mibps:.3f}")


if __name__ == "__main__":
    main()

# Custom Client–Server Protocol Using TCP Sockets

A compact but **production-style TCP client–server project** that demonstrates how to build a **custom application-layer protocol** on top of raw TCP sockets.

This project was designed to be:
- **Resume-aligned** (connection setup, message framing, latency & throughput analysis)
- **Readable and educational** (clear protocol spec, diagrams, and rationale)
- **Practical** (handles partial reads, graceful teardown, benchmarking)

> **Core idea:** TCP is a byte stream, not a message protocol.  
> This project implements a simple **length-prefixed framing protocol** so application messages are reconstructed correctly.

---

## What this project demonstrates

- TCP socket programming (`bind`, `listen`, `accept`, `connect`, timeouts, teardown)
- Application-layer **message framing**
- Client–server request/response design
- Latency (RTT) and throughput benchmarking under varying payload sizes
- Defensive networking practices (partial reads, max frame size guards)

---





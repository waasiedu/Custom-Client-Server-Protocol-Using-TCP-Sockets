# ByteStream  
*A Custom Client–Server Protocol Using TCP Sockets*

I built ByteStream to better understand what actually happens when you send data over a TCP socket.

TCP is often described as reliable and ordered, but once you start working directly with sockets, it becomes clear that TCP does not give you message boundaries — only a continuous stream of bytes. This project is my way of exploring what it takes to build a clean, predictable application protocol on top of that stream.

ByteStream is intentionally small, readable, and focused on correctness rather than scale.

---

## What this project does

- Implements a simple client–server protocol on top of TCP
- Adds explicit message framing to handle TCP’s byte-stream nature
- Correctly handles partial reads and writes
- Supports basic message types (text, ping/pong, bulk data)
- Measures latency and throughput across different payload sizes
- Logs behavior clearly to make data flow easy to follow

There are no frameworks involved — just sockets and careful handling.

---

## Why framing exists

TCP guarantees reliable, ordered delivery of bytes, but it does not preserve message boundaries.

If one side sends:
send("hello")
send("world")

The receiver might see:
"helloworld"
or
"hel" + "lo" + "world"

or any other split.

This means the application must define how messages start and end.

ByteStream solves this by adding a small fixed-size header before every payload, allowing the receiver to reconstruct complete messages safely and deterministically.

---

## Message framing format

Each message sent over the socket has the following structure:

4 bytes  → payload length (unsigned integer, big-endian)  
1 byte   → message type  
N bytes  → payload  

In other words:

| LENGTH | TYPE | PAYLOAD |

The receiver follows a simple rule:
1. Read exactly 5 bytes to obtain the header
2. Extract the payload length
3. Read exactly N bytes to obtain the payload

This avoids guessing and prevents corrupted message boundaries.

---

## Message types used

The protocol defines a small set of message types:

- TEXT  – UTF-8 encoded text messages  
- PING  – latency probe  
- PONG  – response to ping  
- DATA  – bulk payload for throughput testing  
- ACK   – acknowledgement from the server  

These are intentionally minimal and exist mainly to explore behavior.

---

## Server behavior

The server:
- Listens on a TCP socket
- Accepts incoming connections
- Handles each client independently
- Reconstructs frames using exact-length reads
- Responds based on message type
- Cleans up cleanly on disconnects or timeouts

At no point does the server assume that a single recv() call corresponds to a full message.

---

## Client behavior

The client:
- Establishes a TCP connection
- Sends framed messages
- Measures round-trip time using ping/pong
- Sends bulk data to observe throughput
- Prints results in a human-readable format

The focus is on visibility and understanding, not raw performance.

---

## Latency and throughput experiments

The benchmark script performs two main experiments.

Latency testing:
- Sends repeated ping messages
- Measures round-trip time (RTT)
- Reports median and tail latency

Throughput testing:
- Sends payloads of increasing size
- Measures effective data rate in MiB/s
- Shows where throughput begins to plateau

This makes the impact of payload size and framing overhead easy to observe.

---

## Message flow overview

Client connects to server  
Client sends framed message  
Server reads header  
Server reads payload  
Server responds with framed message  
Connection closes cleanly  

All communication follows this same pattern.

---

## Key takeaways from building ByteStream

- TCP is reliable but unstructured
- Message framing is required for correctness
- Partial reads are normal, not edge cases
- Average latency alone is misleading
- Clean connection teardown matters

---

## What this project is not

- Not a production-ready system
- Not optimized for high concurrency
- Not using async or epoll on purpose
- Not hiding complexity behind frameworks

This project is meant to be small, honest, and educational.

---

## Running the code

Start the server:
python -m tcp_framed.server

Run a client:
python -m tcp_framed.client --message "hello"

Run benchmarks:
python -m tcp_framed.bench

---

## Closing note

ByteStream exists to build intuition.

It helped me understand what TCP actually provides — and what it does not — once real data starts flowing across a socket.

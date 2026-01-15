# A Small TCP Protocol I Built to Really Understand the Stream

I built this project because I kept seeing TCP described as “reliable” and “ordered,” yet every real system still seemed to reinvent its own protocol on top of it.

So this repo is my attempt to answer a simple question:

> *What does it actually take to build a clean, predictable application protocol on top of raw TCP sockets?*

The answer turned out to be: **message framing, careful reads, and a lot of respect for the fact that TCP is just a byte stream.**

This project is intentionally small, readable, and hands-on.

---

## What this project does

- Implements a **length-prefixed framing protocol** on top of TCP
- Handles **partial reads** correctly (no assumptions about `recv()` boundaries)
- Supports a few simple message types (text, ping/pong, bulk data)
- Includes a lightweight **latency and throughput benchmark**
- Logs everything clearly so you can see what’s happening on the wire

There’s no framework, no magic — just sockets and discipline.

---

## Why framing exists (the short version)

TCP does **not** preserve message boundaries.

If you send:

from dataclasses import dataclass

# Message type identifiers (1 byte)
TEXT = 0x01
PING = 0x02
PONG = 0x03
DATA = 0x04
ACK  = 0x05

TYPE_NAMES = {
    TEXT: "TEXT",
    PING: "PING",
    PONG: "PONG",
    DATA: "DATA",
    ACK:  "ACK",
}

@dataclass(frozen=True)
class Frame:
    msg_type: int
    payload: bytes

    def __repr__(self) -> str:
        name = TYPE_NAMES.get(self.msg_type, f"0x{self.msg_type:02x}")
        return f"Frame(type={name}, payload_len={len(self.payload)})"

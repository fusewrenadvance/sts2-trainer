from __future__ import annotations

import struct

import pymem


class MemoryOps:
    """Typed read/write helpers over pymem for the trainer's common scalar types."""

    def __init__(self, memory: pymem.Pymem) -> None:
        self.memory = memory

    def read_i32(self, addr: int) -> int:
        return struct.unpack("<i", self.memory.read_bytes(addr, 4))[0]

    def write_i32(self, addr: int, value: int) -> None:
        self.memory.write_bytes(addr, struct.pack("<i", value & 0xFFFFFFFF if value < 0 else value))

    def read_f32(self, addr: int) -> float:
        return struct.unpack("<f", self.memory.read_bytes(addr, 4))[0]

    def write_f32(self, addr: int, value: float) -> None:
        self.memory.write_bytes(addr, struct.pack("<f", value))

    def read_ptr(self, addr: int) -> int:
        return int.from_bytes(self.memory.read_bytes(addr, 8), "little")

    def snapshot(self, addr: int, size: int) -> bytes:
        return self.memory.read_bytes(addr, size)

    def restore(self, addr: int, blob: bytes) -> None:
        self.memory.write_bytes(addr, blob)
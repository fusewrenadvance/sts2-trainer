from __future__ import annotations

import struct

from sts2_trainer.core.memory_ops import MemoryOps


class FakeMemory:
    def __init__(self) -> None:
        self.buf: dict[int, bytes] = {}

    def read_bytes(self, addr: int, size: int) -> bytes:
        return self.buf.get(addr, b"\x00" * size)[:size]

    def write_bytes(self, addr: int, data: bytes) -> None:
        self.buf[addr] = data


def test_i32_roundtrip():
    mem = FakeMemory()
    ops = MemoryOps(mem)  # type: ignore[arg-type]
    ops.write_i32(0x1000, 42)
    assert ops.read_i32(0x1000) == 42


def test_f32_roundtrip():
    mem = FakeMemory()
    ops = MemoryOps(mem)  # type: ignore[arg-type]
    ops.write_f32(0x2000, 1.5)
    assert abs(ops.read_f32(0x2000) - 1.5) < 1e-6


def test_snapshot_restore():
    mem = FakeMemory()
    ops = MemoryOps(mem)  # type: ignore[arg-type]
    ops.write_i32(0x3000, 7)
    snap = ops.snapshot(0x3000, 4)
    ops.write_i32(0x3000, 99)
    ops.restore(0x3000, snap)
    assert ops.read_i32(0x3000) == 7
    assert struct.calcsize("<i") == 4
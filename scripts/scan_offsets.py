"""Standalone offset scanner — useful when a game patch breaks signatures."""
from __future__ import annotations

import sys

from sts2_trainer.bootstrap import TrainerSession


def main() -> int:
    session = TrainerSession(overlay=False)
    session.attach()
    resolved = session.resolver.dump()
    if not resolved:
        print("no offsets resolved — check config/offsets.yaml", file=sys.stderr)
        return 1
    for name, addr in sorted(resolved.items()):
        print(f"{name:<20} 0x{addr:08X}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
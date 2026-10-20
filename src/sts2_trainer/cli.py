from __future__ import annotations

import argparse
import sys

from rich.console import Console

from sts2_trainer.bootstrap import TrainerSession
from sts2_trainer.utils.logger import get_logger

console = Console()
logger = get_logger("cli")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sts2-trainer", description="Slay the Spire 2 Trainer")
    p.add_argument("--version", action="store_true", help="print version and exit")
    p.add_argument("--no-overlay", action="store_true", help="run headless")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("attach", help="attach to the running game process")
    sub.add_parser("scan", help="scan for offsets and dump resolved addresses")
    sub.add_parser("run", help="attach, load features, and start the hotkey loop")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.version:
        from sts2_trainer import __version__
        console.print(f"sts2-trainer {__version__}")
        return 0

    session = TrainerSession(overlay=not args.no_overlay)
    cmd = args.cmd or "run"

    try:
        if cmd == "attach":
            session.attach()
            console.print(f"[green]attached to pid {session.pid}[/green]")
        elif cmd == "scan":
            session.attach()
            for name, addr in session.resolver.dump().items():
                console.print(f"  {name:<20} 0x{addr:08X}")
        elif cmd == "run":
            session.start()
    except KeyboardInterrupt:
        logger.warning("interrupted by user")
        session.stop()
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
from __future__ import annotations

from pathlib import Path

import yaml
import pymem

from sts2_trainer.utils.logger import get_logger

logger = get_logger("offsets")

CONFIG_PATH = Path(__file__).resolve().parents[3] / "config" / "offsets.yaml"


class OffsetResolver:
    """Resolves chained pointer offsets from config/offsets.yaml against the live process."""

    def __init__(self, memory: pymem.Pymem, config_path: Path = CONFIG_PATH) -> None:
        self.memory = memory
        self.config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        self._resolved: dict[str, int] = {}

    def _module_base(self) -> int:
        from pymem.process import module_from_name
        mod = module_from_name(self.memory.process_handle, self.config["game"]["module_name"])
        if mod is None:
            raise RuntimeError("game module not found")
        return mod.lpBaseOfDll

    def _read_ptr(self, addr: int) -> int:
        return int.from_bytes(self.memory.read_bytes(addr, 8), "little")

    def resolve(self, name: str) -> int:
        if name in self._resolved:
            return self._resolved[name]

        spec = self.config["offsets"][name]
        base = self._module_base()

        if "static_offset" in spec:
            addr = base + int(spec["static_offset"], 16)
            self._resolved[name] = addr
            return addr

        chain = spec.get("chain") or []
        if not chain:
            raise KeyError(f"offset {name} has no chain or static offset")

        addr = self.resolve(chain[0])
        for hop in chain[1:-1]:
            addr = self._read_ptr(addr + int(hop, 16))
        addr += int(chain[-1], 16)
        self._resolved[name] = addr
        return addr

    def resolve_all(self) -> None:
        for key in self.config["offsets"]:
            try:
                self.resolve(key)
            except Exception as exc:  # noqa: BLE001
                logger.warning("failed to resolve %s: %s", key, exc)

    def dump(self) -> dict[str, int]:
        return dict(self._resolved)
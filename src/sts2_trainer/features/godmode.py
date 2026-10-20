from __future__ import annotations

from sts2_trainer.features.base import Feature


class GodMode(Feature):
    name = "godmode"
    hotkey = "F3"

    def on_toggle(self) -> None:
        hp_addr = self.resolver.resolve("hp_current")
        max_addr = self.resolver.resolve("hp_max")
        hp_max = self.ops.read_i32(max_addr)
        self.ops.write_i32(hp_addr, hp_max)
        self.logger.info("hp pinned to max (%d)", hp_max)

    def tick(self) -> None:
        if not self._enabled:
            return
        hp_addr = self.resolver.resolve("hp_current")
        max_addr = self.resolver.resolve("hp_max")
        hp_max = self.ops.read_i32(max_addr)
        if self.ops.read_i32(hp_addr) < hp_max:
            self.ops.write_i32(hp_addr, hp_max)
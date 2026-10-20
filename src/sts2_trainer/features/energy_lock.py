from __future__ import annotations

from sts2_trainer.features.base import Feature


class InfiniteEnergy(Feature):
    name = "infinite_energy"
    hotkey = "F1"

    def on_toggle(self) -> None:
        addr = self.resolver.resolve("energy")
        current = self.ops.read_i32(addr)
        self.ops.write_i32(addr, 3)
        self.logger.info("energy was %d, locked to 3", current)

    def tick(self) -> None:
        """Called by the overlay tick loop to keep energy pinned."""
        if not self._enabled:
            return
        addr = self.resolver.resolve("energy")
        if self.ops.read_i32(addr) < 3:
            self.ops.write_i32(addr, 3)
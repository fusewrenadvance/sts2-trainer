from __future__ import annotations

from sts2_trainer.features.base import Feature

MAX_GOLD = 999_999


class GoldMultiplier(Feature):
    name = "gold_multiplier"
    hotkey = "F2"
    multiplier = 10

    def on_toggle(self) -> None:
        addr = self.resolver.resolve("gold")
        current = self.ops.read_i32(addr)
        new_value = min(current * self.multiplier, MAX_GOLD)
        self.ops.write_i32(addr, new_value)
        self.logger.info("gold %d -> %d (x%d)", current, new_value, self.multiplier)
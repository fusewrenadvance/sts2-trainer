from __future__ import annotations

from typing import TYPE_CHECKING

from sts2_trainer.features.energy_lock import InfiniteEnergy
from sts2_trainer.features.gold_multiplier import GoldMultiplier
from sts2_trainer.features.godmode import GodMode
from sts2_trainer.features.card_dupe import CardDuplicator

if TYPE_CHECKING:
    from sts2_trainer.core.memory_ops import MemoryOps
    from sts2_trainer.core.offsets import OffsetResolver


def load_features(resolver: "OffsetResolver", memory) -> list:
    ops = MemoryOps(memory)
    return [
        InfiniteEnergy(resolver, ops),
        GoldMultiplier(resolver, ops),
        GodMode(resolver, ops),
        CardDuplicator(resolver, ops),
    ]


__all__ = ["load_features", "InfiniteEnergy", "GoldMultiplier", "GodMode", "CardDuplicator"]
from __future__ import annotations

from abc import ABC, abstractmethod

from sts2_trainer.core.memory_ops import MemoryOps
from sts2_trainer.core.offsets import OffsetResolver
from sts2_trainer.utils.hotkeys import HotkeyBinding
from sts2_trainer.utils.logger import get_logger


class Feature(ABC):
    """Base class for every trainer feature module."""

    name: str = "feature"
    hotkey: str = "F0"

    def __init__(self, resolver: OffsetResolver, ops: MemoryOps) -> None:
        self.resolver = resolver
        self.ops = ops
        self.logger = get_logger(f"feature.{self.name}")
        self._binding: HotkeyBinding | None = None
        self._enabled = False

    @abstractmethod
    def on_toggle(self) -> None: ...

    def enable(self) -> None:
        if self._enabled:
            return
        self._binding = HotkeyBinding(self.hotkey, self.on_toggle)
        self._binding.register()
        self._enabled = True

    def disable(self) -> None:
        if self._binding:
            self._binding.unregister()
            self._binding = None
        self._enabled = False

    @property
    def enabled(self) -> bool:
        return self._enabled
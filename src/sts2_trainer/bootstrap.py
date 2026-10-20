from __future__ import annotations

import time

from sts2_trainer.core.attach import ProcessAttacher
from sts2_trainer.core.offsets import OffsetResolver
from sts2_trainer.features import load_features
from sts2_trainer.overlay.hud import TrainerOverlay
from sts2_trainer.utils.logger import get_logger

logger = get_logger("bootstrap")


class TrainerSession:
    """Top-level lifecycle: attach -> resolve offsets -> load features -> hotkey loop."""

    def __init__(self, overlay: bool = True) -> None:
        self.attacher = ProcessAttacher()
        self.resolver: OffsetResolver | None = None
        self.features = []
        self.overlay_enabled = overlay
        self._overlay: TrainerOverlay | None = None
        self.pid: int | None = None

    def attach(self) -> None:
        self.pid = self.attacher.attach()
        self.resolver = OffsetResolver(self.attacher.memory)
        self.resolver.resolve_all()
        logger.info("attached pid=%s module=0x%08X", self.pid, self.attacher.module_base)

    def start(self) -> None:
        self.attach()
        self.features = load_features(self.resolver, self.attacher.memory)
        for feat in self.features:
            feat.enable()
            logger.info("feature enabled: %s (%s)", feat.name, feat.hotkey)

        if self.overlay_enabled:
            self._overlay = TrainerOverlay(self.features)
            self._overlay.start()

        try:
            while True:
                time.sleep(0.25)
        finally:
            self.stop()

    def stop(self) -> None:
        for feat in self.features:
            try:
                feat.disable()
            except Exception:  # noqa: BLE001
                logger.exception("failed to disable %s", feat.name)
        if self._overlay:
            self._overlay.stop()
        self.attacher.detach()
        logger.info("session stopped")
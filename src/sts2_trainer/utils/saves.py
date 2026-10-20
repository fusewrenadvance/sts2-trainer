from __future__ import annotations

import shutil
import time
from pathlib import Path

from sts2_trainer.utils.logger import get_logger

logger = get_logger("saves")

SAVE_DIR = Path.home() / "AppData" / "Local" / "SlayTheSpire2" / "saves"
BACKUP_DIR = SAVE_DIR / ".trainer_backups"


def backup_before_attach() -> Path | None:
    if not SAVE_DIR.exists():
        logger.warning("save dir not found, skipping backup")
        return None
    BACKUP_DIR.mkdir(exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    dest = BACKUP_DIR / f"run-{stamp}"
    shutil.copytree(SAVE_DIR, dest, ignore=shutil.ignore_patterns(".trainer_backups"))
    logger.info("save backed up to %s", dest)
    return dest
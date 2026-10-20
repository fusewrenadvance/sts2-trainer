from __future__ import annotations

import ctypes
from dataclasses import dataclass

import pymem
from pymem.process import module_from_name

from sts2_trainer.utils.logger import get_logger

logger = get_logger("attach")

PROCESS_NAME = "SlayTheSpire2.exe"
MODULE_NAME = "SlayTheSpire2.exe"


@dataclass
class AttachResult:
    pid: int
    module_base: int


class ProcessAttacher:
    def __init__(self) -> None:
        self.pm: pymem.Pymem | None = None
        self.module_base: int = 0

    def attach(self) -> int:
        try:
            self.pm = pymem.Pymem(PROCESS_NAME)
        except pymem.exception.ProcessNotFound as exc:
            raise RuntimeError(
                "Slay the Spire 2 is not running. Launch the game first."
            ) from exc

        mod = module_from_name(self.pm.process_handle, MODULE_NAME)
        if mod is None:
            raise RuntimeError(f"module {MODULE_NAME} not found in process")
        self.module_base = mod.lpBaseOfDll
        logger.debug("module base 0x%08X", self.module_base)
        return self.pm.process_id

    @property
    def memory(self) -> pymem.Pymem:
        if self.pm is None:
            raise RuntimeError("not attached")
        return self.pm

    def detach(self) -> None:
        if self.pm is not None:
            try:
                self.pm.close_process()
            except Exception:  # noqa: BLE001
                pass
            self.pm = None

    def is_alive(self) -> bool:
        if self.pm is None:
            return False
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(0x1000, False, self.pm.process_id)
        if not handle:
            return False
        kernel32.CloseHandle(handle)
        return True
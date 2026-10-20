from __future__ import annotations

from typing import Callable

import keyboard


class HotkeyBinding:
    def __init__(self, key: str, callback: Callable[[], None]) -> None:
        self.key = key
        self.callback = callback
        self._handle = None

    def register(self) -> None:
        self._handle = keyboard.add_hotkey(self.key, self.callback, suppress=False)

    def unregister(self) -> None:
        if self._handle is not None:
            keyboard.remove_hotkey(self._handle)
            self._handle = None
from __future__ import annotations

import threading
import tkinter as tk

from sts2_trainer.utils.logger import get_logger

logger = get_logger("overlay")


class TrainerOverlay:
    """Minimal always-on-top HUD showing enabled features and hotkeys."""

    def __init__(self, features: list) -> None:
        self.features = features
        self._thread: threading.Thread | None = None
        self._root: tk.Tk | None = None
        self._stop = threading.Event()

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run, daemon=True, name="overlay")
        self._thread.start()

    def _run(self) -> None:
        self._root = tk.Tk()
        self._root.title("sts2-trainer")
        self._root.attributes("-topmost", True)
        self._root.attributes("-alpha", 0.82)
        self._root.geometry("+24+24")
        self._root.overrideredirect(True)

        self._label = tk.Label(
            self._root, text="", justify="left", font=("Consolas", 10),
            bg="#101418", fg="#d7e0ea", padx=10, pady=6,
        )
        self._label.pack()
        self._refresh()
        self._root.mainloop()

    def _refresh(self) -> None:
        if self._stop.is_set() or self._root is None:
            return
        lines = ["sts2-trainer  v0.6.3", "-" * 22]
        for feat in self.features:
            mark = "[x]" if feat.enabled else "[ ]"
            lines.append(f"{mark} {feat.hotkey:<4} {feat.name}")
        self._label.config(text="\n".join(lines))
        self._root.after(500, self._refresh)

    def stop(self) -> None:
        self._stop.set()
        if self._root is not None:
            try:
                self._root.quit()
            except tk.TclError:
                pass
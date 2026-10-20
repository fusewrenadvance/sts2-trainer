from __future__ import annotations

from sts2_trainer.features.base import Feature


class CardDuplicator(Feature):
    name = "card_duplicator"
    hotkey = "F4"
    max_dupes = 5

    def on_toggle(self) -> None:
        deck_ptr = self.resolver.resolve("deck_ptr")
        # deck is a vector<CardRef>; header layout: begin, end, capacity (24 bytes on x64)
        begin = self.ops.read_ptr(deck_ptr)
        end = self.ops.read_ptr(deck_ptr + 0x8)
        count = (end - begin) // 0x8
        self.logger.info("deck currently holds %d cards, dupe limit %d", count, self.max_dupes)
        if count == 0:
            self.logger.warning("empty deck, nothing to duplicate")
            return
        self.logger.info("card duplicator armed (manual dupe in overlay)")
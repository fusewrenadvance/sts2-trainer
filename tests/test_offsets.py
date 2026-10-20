from __future__ import annotations

from pathlib import Path

import yaml


def test_offsets_config_loads():
    cfg_path = Path(__file__).resolve().parents[1] / "config" / "offsets.yaml"
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    assert cfg["game"]["process_name"] == "SlayTheSpire2.exe"
    assert "energy" in cfg["offsets"]
    assert "gold" in cfg["offsets"]


def test_every_feature_offset_exists():
    cfg_path = Path(__file__).resolve().parents[1] / "config" / "offsets.yaml"
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    for feat_name, feat in cfg["features"].items():
        write = feat.get("write")
        if write and "target" in write:
            assert write["target"] in cfg["offsets"], f"{feat_name} -> missing {write['target']}"
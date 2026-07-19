from __future__ import annotations

from pathlib import Path
from types import ModuleType
import importlib.machinery
import sys


SRC_ROOT = Path(__file__).resolve().parents[1] / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


if "src.config" not in sys.modules:
    config_stub = ModuleType("src.config")
    config_stub.__spec__ = importlib.machinery.ModuleSpec(
        "src.config",
        loader=None,
        origin=str(SRC_ROOT / "app_config" / "config.py"),
    )
    sys.modules["src.config"] = config_stub

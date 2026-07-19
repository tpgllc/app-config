from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from types import ModuleType
import importlib
import os

import app_config.config as package_config
from app_config.configutils import ConfigUtils


_SKIP_ATTRS = {"cp", "cu"}


def clone_package_config(name: str = "test_config") -> ModuleType:
    """Build an isolated module-like object from the package defaults."""
    module = ModuleType(name)

    for key, value in vars(package_config).items():
        if key.startswith("__") or key in _SKIP_ATTRS or callable(value):
            continue

        if key == "config":
            setattr(module, key, None)
            continue

        setattr(module, key, deepcopy(value))

    module.wkdir_path = None
    module.wkdir = None
    module.srcdir = None
    module.datadir = None

    return module


def set_test_paths(config_module: ModuleType, root: Path) -> None:
    """Point the config module at a temporary test workspace."""
    data_dir = root / "data"
    src_dir = root / "src"
    data_dir.mkdir(parents=True, exist_ok=True)
    src_dir.mkdir(parents=True, exist_ok=True)

    config_module.wkdir_path = src_dir / "config.py"
    config_module.wkdir = f"{root}{os.sep}"
    config_module.srcdir = f"{src_dir}{os.sep}"
    config_module.datadir = f"{data_dir}{os.sep}"


def initialize_config_module(config_module: ModuleType, config_cls, autorun: bool = False) -> ModuleType:
    """Attach ConfigParms and ConfigUtils instances to a synthetic config module."""
    config_module.cp = config_cls(config_module, autorun=autorun)
    config_module.cu = ConfigUtils(config_module)
    return config_module


def reload_package_config():
    """Reload the real package config module for an isolated integration test."""
    return importlib.reload(package_config)

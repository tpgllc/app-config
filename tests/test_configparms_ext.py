from __future__ import annotations

from copy import deepcopy
import os
from pathlib import Path
import pytest

from app_config.configparms_ext import ConfigParmsExt
from tests.support import clone_package_config, initialize_config_module


class HookedConfigParms(ConfigParmsExt):
    def set_directories(self) -> None:
        if self.cfg.wkdir is None:
            self.cfg.wkdir_path = self.cfg._test_root / "src" / "config.py"
            self.cfg.srcdir = f"{self.cfg._test_root / 'src'}{os.sep}"
            self.cfg.wkdir = f"{self.cfg._test_root}{os.sep}"
            self.cfg.datadir = f"{self.cfg._test_root / 'data'}{os.sep}"
            self.cfg.extdir = "added in set_directories"

    def custom_init_routine(self) -> None:
        self.cfg.init_var = "loaded from ext"

    def set_custom_default_sects(self, config, sec, vars) -> bool:
        self.cfg.scds = "from set_custom_default_sects"
        return False

    def set_custom_default_vars(self, config, sec, vars, var) -> bool:
        self.cfg.scdv = "from set_custom_default_vars"
        return False

    def verify_config_sects(self, config, sec, vars) -> bool:
        self.cfg.vcs = "from verify_config_sects"
        return False

    def verify_config_vars(self, config, sec, vars, var) -> bool:
        self.cfg.vcv = "from verify_config_vars"
        return False

    def set_module_sects(self, config, sec, vars) -> bool:
        self.cfg.sms = "from set_module_sects"
        return False

    def set_module_vars(self, config, sec, vars, var) -> bool:
        self.cfg.smv = "from set_module_vars"
        if var == "seed":
            self.cfg.seed = 0.023
            return True
        return False

    def set_custom_module_vars(self, config) -> None:
        self.cfg.scmv = "from set_custom_module_vars"


def build_extended_config(tmp_path):
    cfg = clone_package_config("test_config_ext")
    cfg._test_root = tmp_path
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    (tmp_path / "src").mkdir(parents=True, exist_ok=True)
    cfg.seed = None
    cfg.sys_cfg_version = "0.1"

    cfg_values = deepcopy(cfg.cfg_values)
    cfg_values["DATA"] = [*cfg_values["DATA"], ("seed", "f")]
    cfg_values["SYSTEM"] = [("sys_cfg_version", "s"), ("sys_comment_prefixes", "l"), ("sys_var", "s")]
    cfg.cfg_values = cfg_values

    initialize_config_module(cfg, HookedConfigParms)
    cfg.cp.run()
    return cfg


def test_set_directories(tmp_path):
    cfg = build_extended_config(tmp_path)

    assert cfg.datadir == f"{tmp_path / 'data'}{os.sep}"
    assert cfg.extdir == "added in set_directories"


def test_custom_init_routine(tmp_path):
    cfg = build_extended_config(tmp_path)

    assert cfg.init_var == "loaded from ext"


def test_set_custom_default_hooks(tmp_path):
    cfg = build_extended_config(tmp_path)

    assert cfg.scds == "from set_custom_default_sects"
    assert cfg.scdv == "from set_custom_default_vars"


def test_set_module_hooks(tmp_path):
    cfg = build_extended_config(tmp_path)

    assert cfg.sms == "from set_module_sects"
    assert cfg.smv == "from set_module_vars"
    assert cfg.seed == 0.023


def test_set_custom_module_vars(tmp_path):
    cfg = build_extended_config(tmp_path)

    assert cfg.scmv == "from set_custom_module_vars"


def test_verify_config_hooks(tmp_path):
    cfg = build_extended_config(tmp_path)

    assert cfg.vcs == "from verify_config_sects"
    assert cfg.vcv == "from verify_config_vars"


def test_find_dir_path(tmp_path):
    cfg = clone_package_config("test_find_dir_path")
    cfg._test_root = tmp_path
    initialize_config_module(cfg, HookedConfigParms)

    nested_root = tmp_path / "workspace"
    start_file = nested_root / "src" / "pkg" / "module.py"
    target_dir = nested_root / "data"

    start_file.parent.mkdir(parents=True, exist_ok=True)
    start_file.touch()
    target_dir.mkdir(parents=True, exist_ok=True)

    result = cfg.cp.find_dir_path("data", str(start_file))

    assert result == Path(target_dir)

    with pytest.raises(FileNotFoundError, match="Could not find project data directory"):
        cfg.cp.find_dir_path("missing", str(start_file))


def test_find_file_path(tmp_path):
    cfg = clone_package_config("test_find_file_path")
    cfg._test_root = tmp_path
    initialize_config_module(cfg, HookedConfigParms)

    nested_root = tmp_path / "workspace"
    start_file = nested_root / "src" / "pkg" / "module.py"
    target_file = nested_root / "pyproject.toml"

    start_file.parent.mkdir(parents=True, exist_ok=True)
    start_file.touch()
    target_file.write_text("[project]\nname = 'test'\n", encoding="utf-8")

    result = cfg.cp.find_file_path("pyproject.toml", str(start_file))

    assert result == Path(target_file)

    with pytest.raises(FileNotFoundError, match="Could not find project file above"):
        cfg.cp.find_file_path("missing.toml", str(start_file))

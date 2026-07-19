from __future__ import annotations

from io import StringIO

from tests.support import reload_package_config, set_test_paths


def build_package_config(tmp_path):
    cfg = reload_package_config()
    set_test_paths(cfg, tmp_path)
    cfg.run()
    return cfg


def test_run_init_uses_module_dependency():
    cfg = reload_package_config()

    assert cfg.cp.cfg is cfg
    assert cfg.cu.cfg is cfg


def test_default_config(tmp_path):
    cfg = build_package_config(tmp_path)

    assert cfg.var1 is True
    assert cfg.m1 == "textm1"
    assert (tmp_path / "data" / cfg.cfg_flnm).is_file()


def test_adding_new_data_item(tmp_path):
    cfg = build_package_config(tmp_path)

    config = cfg.cp.read_config_file(cfg.config)
    original_version = config.get("SYSTEM", "sys_cfg_version")

    config.remove_option("MAIN", "var2")
    config.remove_option("SYSTEM", "sys_var")
    config.set("SYSTEM", "sys_cfg_version", "0.0.0")
    cfg.cp.write_cfg(config)
    cfg.cp.set_config_module_variables(config)

    assert not config.has_option("MAIN", "var2")
    assert not config.has_option("SYSTEM", "sys_var")

    config = cfg.cp.read_config_file(cfg.config)

    assert cfg.sys_cfg_version == original_version
    assert config.has_option("MAIN", "var2")
    assert config.has_option("SYSTEM", "sys_var")


def test_remove_default_comments(tmp_path):
    cfg = build_package_config(tmp_path)

    config = cfg.cp.set_default_config(cfg.config)
    comments = [key for key, _ in config["DATA"].items() if key.startswith("#")]

    cfg.cp.remove_default_comments(config)

    for key in comments:
        assert not config.has_option("DATA", key)


def test_print_config_vars(tmp_path):
    cfg = build_package_config(tmp_path)
    output = StringIO()

    cfg.cu.print_config_vars(heading="test heading", fileobj=output)

    text = output.getvalue()
    assert "--- test heading ---" in text
    assert "file name:" in text
    assert "sections:" in text

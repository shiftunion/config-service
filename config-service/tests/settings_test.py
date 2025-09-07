from __future__ import annotations

import logging
import importlib
import os

from app.core import config as config_mod


def test_env_overrides(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("LOG_LEVEL=DEBUG\nDB_HOST=customhost\n")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("DB_HOST", "customhost")
    importlib.reload(config_mod)
    s = config_mod.get_settings()
    assert s.DB_HOST == "customhost"
    assert s.log_level() == logging.DEBUG


def test_invalid_log_level_fallback(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "NOTREAL")
    importlib.reload(config_mod)
    s = config_mod.get_settings()
    assert s.log_level() == logging.INFO

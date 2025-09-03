from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest


def test_checksum_calculation_tmpdir(tmp_path: Path):
    from migrations import file_checksum

    p = tmp_path / "m.sql"
    p.write_text("select 1;\n")
    c1 = file_checksum(p)
    p.write_text("select 2;\n")
    c2 = file_checksum(p)
    assert c1 != c2

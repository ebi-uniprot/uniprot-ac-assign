import shutil
from pathlib import Path

from revert import revert
from utils import assert_files_eq


def test_revert(tmp_path):
    test_input_path = Path("test_files/input")
    shutil.copytree(test_input_path, tmp_path, dirs_exist_ok=True)
    revert(3, tmp_path)
    assert_files_eq(
        tmp_path / "backup" / "available_acs(3).txt", tmp_path / "available_acs.txt"
    )
    assert_files_eq(
        tmp_path / "backup" / "assigned_acs(3).txt", tmp_path / "assigned_acs.txt"
    )

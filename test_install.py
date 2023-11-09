from pathlib import Path

from install import install
from utils import assert_files_eq


def test_install(tmp_path):
    install(tmp_path)
    ac_assign_path = tmp_path / "ac_assign.py"
    revert_path = tmp_path / "revert.py"
    assert ac_assign_path.exists()
    assert revert_path.exists()
    assert_files_eq(ac_assign_path, Path("./ac_assign.py"))
    assert_files_eq(revert_path, Path("./revert.py"))

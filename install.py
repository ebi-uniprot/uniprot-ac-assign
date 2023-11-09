#!/usr/bin/env python3
import shutil
from pathlib import Path

from ac_assign import WORKING_PATH


def install(dest):
    scripts_path = Path(__file__).parent.resolve()
    assign_path = scripts_path / "ac_assign.py"
    revert_path = scripts_path / "revert.py"
    assert assign_path.exists()
    assert revert_path.exists()
    assert dest.exists()
    shutil.copy2(assign_path, dest)
    shutil.copy2(revert_path, dest)


def main():
    install(WORKING_PATH)


if __name__ == "__main__":
    main()

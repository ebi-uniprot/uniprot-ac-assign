#!/usr/bin/env python3
import shutil
from datetime import datetime
from pathlib import Path

from ac_assign import (
    ASSIGNED_ACS_FILE,
    AVAILABLE_ACS_FILE,
    BACKUP_DIR,
    WORKING_PATH,
    get_backup_file_counters,
    get_backup_files,
    get_filename_with_counter,
)


def get_number_lines(path):
    with open(path) as f:
        return len(f.readlines())


def revert(version):
    backup_path = WORKING_PATH / BACKUP_DIR
    for [src, dest] in [
        [
            backup_path / get_filename_with_counter(AVAILABLE_ACS_FILE, version),
            WORKING_PATH / AVAILABLE_ACS_FILE,
        ],
        [
            backup_path / get_filename_with_counter(ASSIGNED_ACS_FILE, version),
            WORKING_PATH / ASSIGNED_ACS_FILE,
        ],
    ]:
        print(f"Replacing {dest} with {src}")
        shutil.copy2(src, dest)
    print(f"Finished reverting to version {version}. Backup files left untouched.")


def list_backups_and_ask_for_version():
    backup_path = WORKING_PATH / BACKUP_DIR
    backup_path = Path("test_files/input/backup")
    print(f"Listing versions in {backup_path}")
    assert backup_path.exists()
    files = get_backup_files(backup_path)
    counters = get_backup_file_counters(files)
    for counter in counters:
        print(f"Version {counter}")
        for filename in [AVAILABLE_ACS_FILE, ASSIGNED_ACS_FILE]:
            filename_with_counter = get_filename_with_counter(filename, counter)
            path = backup_path / filename_with_counter
            stat = path.stat()
            date = datetime.fromtimestamp(stat.st_mtime)
            print(
                "--",
                filename_with_counter,
                "| modified",
                date.strftime("%Y-%m-%d %H:%M:%S"),
                "|",
                get_number_lines(path),
                "lines",
            )
    revert_version = int(input("Select version to revert to: "))
    assert revert_version in counters, "Must be in range"
    revert(revert_version)


def main():
    list_backups_and_ask_for_version()


if __name__ == "__main__":
    main()

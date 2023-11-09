#!/usr/bin/env python3
import shutil
from datetime import datetime

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
        return len([line for line in f.readlines() if line])


def revert(version, working_path):
    backup_path = working_path / BACKUP_DIR
    for file in [
        AVAILABLE_ACS_FILE,
        ASSIGNED_ACS_FILE,
    ]:
        src = backup_path / get_filename_with_counter(file, version)
        dest = working_path / file
        print(f"Replacing {dest} with {src}")
        shutil.copy2(src, dest)
    print(f"Finished reverting to version {version}. Backup files left untouched.")


def list_backups_and_ask_for_version(working_path):
    backup_path = working_path / BACKUP_DIR
    print(f"Listing versions in {backup_path}")
    assert backup_path.exists()
    files = get_backup_files(backup_path)
    counters = sorted(get_backup_file_counters(files), reverse=True)
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
    revert(revert_version, working_path)


def main():
    print(WORKING_PATH)
    list_backups_and_ask_for_version(WORKING_PATH)


if __name__ == "__main__":
    main()

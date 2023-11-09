#!/usr/bin/env python3
"""
script for assigning new ACs.
Asks assigner for location of flatfile and reads the IDs, then asks for the
name of the curator that needs the AC and the purpose, returns new ACs from
the AC list and increments current AC, writes info to ASSIGNDACS file.
"""

import argparse
import os
import re
import shutil
from datetime import date
from pathlib import Path

NUMBER_BACKUPS = 5
WORKING_PATH = Path(r"F:\ACNumbers")
BACKUP_DIR = "backup"
AVAILABLE_ACS_FILE = "available_acs.txt"
ASSIGNED_ACS_FILE = "assigned_acs.txt"


def get_ids_from_flat_file(flatfile):
    assert os.path.exists(
        flatfile
    ), "Could NOT find the flatfile. Check the flatfile location/path is correct"
    ids = []
    with open(flatfile, "r") as f:
        for line in f:
            if line.startswith("ID "):
                ids.append(line.split()[1])
    return ids


def get_backup_files(backup_path):
    return list(
        backup_path.glob(get_filename_with_counter(AVAILABLE_ACS_FILE, "*"))
    ) + list(backup_path.glob(get_filename_with_counter(ASSIGNED_ACS_FILE, "*")))


def get_backup_file_counters(files):
    p = re.compile(
        rf"(?:{get_filename_without_txt(AVAILABLE_ACS_FILE)}|{get_filename_without_txt(ASSIGNED_ACS_FILE)})\((\d+)\)\.txt$"
    )
    return sorted({int(m.group(1)) for m in (p.match(f.name) for f in files) if m})


def get_counters_to_remove(counters):
    return counters[:-NUMBER_BACKUPS]


def get_filename_without_txt(filename):
    extension = ".txt"
    assert filename.endswith(extension)
    return filename[: -len(extension)]


def get_filename_with_counter(filename, counter):
    return f"{get_filename_without_txt(filename)}({counter}).txt"


def remove_old_backup_files(counters, backup_path):
    for counter in get_counters_to_remove(counters):
        for file_name in [
            ASSIGNED_ACS_FILE,
            AVAILABLE_ACS_FILE,
        ]:
            file_path = backup_path / get_filename_with_counter(file_name, counter)
            file_path.unlink()


def backup_files(working_path):
    backup_path = working_path / BACKUP_DIR
    assert backup_path.exists()
    files = get_backup_files(backup_path)
    counters = get_backup_file_counters(files)
    next_counter = counters[-1] + 1 if counters else 1
    counters.append(next_counter)
    shutil.copy2(
        working_path / AVAILABLE_ACS_FILE,
        backup_path / get_filename_with_counter(AVAILABLE_ACS_FILE, next_counter),
    )
    shutil.copy2(
        working_path / ASSIGNED_ACS_FILE,
        backup_path / get_filename_with_counter(ASSIGNED_ACS_FILE, next_counter),
    )
    remove_old_backup_files(counters, backup_path)


def read_available_acs_file(available_acs_file):
    with open(available_acs_file, "r") as f:
        return f.read().splitlines()


def partition_available_acs(available_acs, flatfile_entry_ids):
    n_flatfile_entry_ids = len(flatfile_entry_ids)
    assert len(available_acs) >= n_flatfile_entry_ids
    new_acs = available_acs[:n_flatfile_entry_ids]
    rest_acs = available_acs[n_flatfile_entry_ids:]
    return new_acs, rest_acs


def generate_assigned_acs_lines(new_acs, flatfile_entry_ids, today, user, curator):
    assert len(new_acs) == len(flatfile_entry_ids)
    for new_ac, flatfile_entry_id in zip(new_acs, flatfile_entry_ids):
        yield " ".join([today, new_ac, flatfile_entry_id, user, curator])


def ac_assign(flatfile, curator, working_dir, today, user):
    flatfile_entry_ids = get_ids_from_flat_file(flatfile)
    working_path = Path(working_dir)
    assert working_path.exists()
    backup_files(working_path)
    available_acs_file = working_path / AVAILABLE_ACS_FILE
    available_acs = read_available_acs_file(available_acs_file)
    new_acs, rest_acs = partition_available_acs(available_acs, flatfile_entry_ids)
    assigned_acs_file = working_path / ASSIGNED_ACS_FILE
    with open(assigned_acs_file, "a+") as f:
        for line in generate_assigned_acs_lines(
            new_acs, flatfile_entry_ids, today, user, curator
        ):
            print(line, file=f)

    with open(available_acs_file, "w") as f:
        for ac in rest_acs:
            print(ac, file=f)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--flatfile", type=str, help="Flat file path")
    parser.add_argument(
        "--curator",
        type=str,
        help="Curator name and purpose e.g. For Bobs curation work",
    )
    args = parser.parse_args()
    return args.flatfile, args.curator


def main():
    flatfile, curator = get_arguments()
    today = date.today().strftime("%d/%m/%y")
    user = os.getlogin()
    ac_assign(flatfile, curator, WORKING_PATH, today, user)


if __name__ == "__main__":
    main()

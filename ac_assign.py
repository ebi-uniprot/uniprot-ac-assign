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


class UnknownBackUpFileError(Exception):
    pass


class AssignedAvailableFilesMismatchError(Exception):
    pass


class NotTxtExtensionError(Exception):
    pass


class NotEnoughAcsError(Exception):
    pass


class AcFlatFileMismatchError(Exception):
    pass


def get_ids_from_flat_file(flatfile):
    if not os.path.exists(flatfile):
        raise FileNotFoundError("flatfile")

    ids = []
    with open(flatfile, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("ID "):
                ids.append(line.split()[1])
    return ids


def get_backup_files(backup_path):
    return list(
        backup_path.glob(get_filename_with_counter(AVAILABLE_ACS_FILE, "*"))
    ) + list(backup_path.glob(get_filename_with_counter(ASSIGNED_ACS_FILE, "*")))


def get_backup_file_counters(files):
    available_stem = get_filename_without_txt(AVAILABLE_ACS_FILE)
    assigned_stem = get_filename_without_txt(ASSIGNED_ACS_FILE)
    p = re.compile(
        rf"(?P<assigned_or_available>{available_stem}|{assigned_stem})\((?P<counter>\d+)\)\.txt$"
    )
    available_counters = []
    assigned_counters = []
    for file in files:
        m = p.match(file.name)
        if m:
            counter = int(m.group("counter"))
            if m.group("assigned_or_available") == available_stem:
                available_counters.append(counter)
            else:
                assigned_counters.append(counter)
        else:
            raise UnknownBackUpFileError(file)
    available_counters = sorted(available_counters)
    assigned_counters = sorted(assigned_counters)

    if available_counters != assigned_counters:
        raise AssignedAvailableFilesMismatchError(
            f"{available_counters} ≠ {assigned_counters}"
        )
    return available_counters


def get_counters_to_remove(counters):
    return counters[:-NUMBER_BACKUPS]


def get_counter_from_filename(filename):
    extension = ".txt"
    if not filename.endswith(extension):
        raise NotTxtExtensionError(filename)
    return filename[: -len(extension)]


def get_filename_without_txt(filename):
    extension = ".txt"
    if not filename.endswith(extension):
        raise NotTxtExtensionError(filename)
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
    if not backup_path.exists():
        raise FileNotFoundError(backup_path)
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
    with open(available_acs_file, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def partition_available_acs(available_acs, flatfile_entry_ids):
    n_flatfile_entry_ids = len(flatfile_entry_ids)
    if len(available_acs) < n_flatfile_entry_ids:
        raise NotEnoughAcsError
    new_acs = available_acs[:n_flatfile_entry_ids]
    rest_acs = available_acs[n_flatfile_entry_ids:]
    return new_acs, rest_acs


def generate_assigned_acs_lines(new_acs, flatfile_entry_ids, today, user, comment):
    if len(new_acs) != len(flatfile_entry_ids):
        raise AcFlatFileMismatchError
    for new_ac, flatfile_entry_id in zip(new_acs, flatfile_entry_ids):
        yield " ".join([today, new_ac, flatfile_entry_id, user, comment])


def ac_assign(flatfile, comment, working_dir, today, user):
    flatfile_entry_ids = get_ids_from_flat_file(flatfile)
    working_path = Path(working_dir)
    if not working_path.exists():
        raise FileNotFoundError("working path")
    backup_files(working_path)
    available_acs_file = working_path / AVAILABLE_ACS_FILE
    available_acs = read_available_acs_file(available_acs_file)
    new_acs, rest_acs = partition_available_acs(available_acs, flatfile_entry_ids)
    assigned_acs_file = working_path / ASSIGNED_ACS_FILE
    with open(assigned_acs_file, "a+", encoding="utf-8") as f:
        for line in generate_assigned_acs_lines(
            new_acs, flatfile_entry_ids, today, user, comment
        ):
            print(line, file=f)

    with open(available_acs_file, "w", encoding="utf-8") as f:
        for ac in rest_acs:
            print(ac, file=f)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--flatfile", "-f", required=True, type=str, help="Flat file path"
    )
    parser.add_argument(
        "--comment",
        "-c",
        required=True,
        type=str,
        help="Curator name and purpose e.g. For Bobs curation work",
    )
    args = parser.parse_args()
    return args.flatfile, args.comment


def main():
    flatfile, comment = get_arguments()
    today = date.today().strftime("%d/%m/%y")
    user = os.getlogin()
    try:
        ac_assign(flatfile, comment, WORKING_PATH, today, user)
    except UnknownBackUpFileError as err:
        print(
            f"Unknown file in backups detected: {err.args[0]}\n\nPlease remove before proceeding"
        )
    except AssignedAvailableFilesMismatchError as err:
        print(
            f"Mismatch between assigned and available backup files. Found these versions: {err.args[0]}"
        )
    except FileNotFoundError as err:
        print(f"Could not find {err.args[0]}. Check location/path is correct.")
    except NotTxtExtensionError as err:
        print(f"Expected .txt extension for {err.args[0]}")
    except NotEnoughAcsError:
        print("There aren't enough available accessions for provided flat file")
    except AcFlatFileMismatchError:
        print(
            "Sometheing went wrong as there aren't an equal number of accessions to assign and the number accessions in the flat file"
        )


if __name__ == "__main__":
    main()

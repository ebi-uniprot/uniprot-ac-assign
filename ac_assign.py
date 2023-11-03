#!/usr/bin/env python3
"""
script for assigning new ACs.
Asks assigner for location of flatfile and reads the IDs, then asks for the
name of the curator that needs the AC and the purpose, returns new ACs from
the AC list and increments current AC, writes info to ASSIGNDACS file.
"""

import argparse
import os
import shutil
from datetime import date
from pathlib import Path


def get_ids_from_flat_file(flatfile):
    assert os.path.exists(
        flatfile
    ), "Could NOT find the flatfile. Check the flatfile location/path is correct"
    # extracts entry ID from flatfile
    ids = []
    with open(flatfile, "r") as f:
        for line in f:
            if line.startswith("ID "):
                ids.append(line.split()[1])
    return ids


def backup_files(working_dir):
    if not os.path.exists("archive"):
        os.mkdir("archive")

    for file in ["ac_list.txt", "ac_datafile.txt"]:
        shutil.copy2(file, "archive")


def read_ac_list_file(ac_list_file):
    with open(ac_list_file, "r") as f:
        return f.read().splitlines()


def partition_ac_list(ac_list, flatfile_entry_ids):
    n_flatfile_entry_ids = len(flatfile_entry_ids)
    assert len(ac_list) >= n_flatfile_entry_ids
    # TODO: inform user when there are less than 10 accessions in ac_list
    new_acs = ac_list[:n_flatfile_entry_ids]
    rest_acs = ac_list[n_flatfile_entry_ids:]
    return new_acs, rest_acs


def generate_ac_datafile_lines(new_acs, flatfile_entry_ids, today, user, curator):
    assert len(new_acs) == len(flatfile_entry_ids)
    for new_ac, flatfile_entry_id in zip(new_acs, flatfile_entry_ids):
        yield " ".join([today, new_ac, flatfile_entry_id, user, curator])


def get_arguments():
    """
    ./ac_assign.py --flatfile ./test_files/single_flatfile.txt --curator "For Bob's curation work" --working_dir ./test_files
    ./ac_assign.py --flatfile /foo/bar --curator "For Bob's curation work" """

    parser = argparse.ArgumentParser()
    parser.add_argument("--flatfile", type=str, help="Flat file path")
    parser.add_argument(
        "--curator",
        type=str,
        help="Curator name and purpose e.g. For Bobs curation work",
    )
    parser.add_argument(
        "--working_dir",
        type=str,
        help="Location of folder containing AC list and assigndacs",
        default="/add/this/in",
    )
    args = parser.parse_args()
    return args.flatfile, args.curator, args.working_dir


def ac_assign(flatfile, curator, working_dir, today, user):
    flatfile_entry_ids = get_ids_from_flat_file(flatfile)
    assert os.path.exists(working_dir)
    ac_list_file = Path(working_dir, "ac_list.txt")
    ac_list = read_ac_list_file(ac_list_file)
    new_acs, rest_acs = partition_ac_list(ac_list, flatfile_entry_ids)
    ac_datafile_file = Path(working_dir, "ac_datafile.txt")
    with open(ac_datafile_file, "a+") as f:
        for line in generate_ac_datafile_lines(
            new_acs, flatfile_entry_ids, today, user, curator
        ):
            print(line, file=f)

    with open(ac_list_file, "w") as f:
        for ac in rest_acs:
            print(ac, file=f)

    # backup_files(working_dir)


def main():
    flatfile, curator, working_dir = get_arguments()
    today = date.today().strftime("%d/%m/%y")
    user = os.getlogin()
    ac_assign(flatfile, curator, working_dir, today, user)


if __name__ == "__main__":
    main()

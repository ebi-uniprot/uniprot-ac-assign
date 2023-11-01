#!/usr/bin/env python3
"""
script for assigning new ACs.
Asks assigner for location of flatfile and reads the IDs, then asks for the
name of the curator that needs the AC and the purpose, returns new ACs from
the AC list and increments current AC, writes info to ASSIGNDACS file.
"""

import argparse
import os
from datetime import date
import shutil

today = date.today()
date_today = today.strftime("%d/%m/%y")
user = os.getlogin()

"""
TODO

[ ] use zip to iterate over new_acs and flat_file_entry_ids at the same time
[ ] test get_ids_from_flat_file using pytest
[ ] test write_new_ac
    [ ] create dummy directory ./test_run for script output to be stored
    [ ] run script and check /test_run is the same as ./test_files/output
    [ ] ensure that ./test_files are untouched
[ ] create another command line argument to specify archive location
[ ] archive with incrementing
[ ] keep only the last n archive
[ ] create another function to revert to latest in archive
"""


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


def read_ac_list_file():
    with open("ac_list.txt", "r") as f:
        return f.read().splitlines()


def partition_ac_list(ac_list, flatfile_entry_ids):
    n_flatfile_entry_ids = len(flatfile_entry_ids)
    assert len(ac_list) >= n_flatfile_entry_ids
    # TODO: inform user when there are less than 10 accessions in ac_list
    new_acs = ac_list[:n_flatfile_entry_ids]
    rest_acs = ac_list[n_flatfile_entry_ids:]
    return new_acs, rest_acs


def write_new_ac(flatfile_entry_ids):
    # add information to end of assigndacs file
    assign_IDs = get_ids_from_flat_file(flatfile)
    assign_AC = get_new_ac(flatfile)
    # use zip to iterate over new_acs and flat_file_entry_ids at the same time
    with open("ac_datafile.txt", "a+") as f:
        assigned = zip(assign_AC, assign_IDs)
        for a, i in assigned:
            line = f"{date_today} {a} {i} {user} {curator}"
            print(f'Writing "{line}" to ac_datafile.txt')
            f.write(f"\n{line}")

        with open("ac_list.txt", "w") as f:
            for ac in rest_acs:
                print(ac, file=f)


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
        # add default location /
    )
    args = parser.parse_args()
    return args.flatfile, args.curator, args.working_dir


# Define main function
def main():
    flatfile, curator, working_dir = get_arguments()
    flatfile_entry_ids = get_ids_from_flat_file(flatfile)
    assert os.path.exists(working_dir)
    os.chdir(working_dir)
    ac_list = read_ac_list_file()
    new_acs, rest_acs = partition_ac_list(ac_list, flatfile_entry_ids)
    # backup_files(working_dir)
    write_new_ac(args.flatfile, args.curator, args.working_dir)
    # new_acs = get_new_ac(flatfile)


# Execute main() function
if __name__ == "__main__":
    main()

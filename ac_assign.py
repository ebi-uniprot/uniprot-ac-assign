#!/usr/bin/env python3
"""
script for assigning new ACs.
Asks assigner for location of flatfile and reads the IDs, then asks for the
name of the curator that needs the AC and the purpose, returns new ACs from
the AC list and increments current AC, writes info to ASSIGNDACS file.
Kate W
"""

import argparse
import os
from datetime import date
import shutil

today = date.today()
date_today = today.strftime("%d/%m/%y")
user = os.getlogin()


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


# finds the flatfile and extracts entry ID
def write_new_ac(flatfile, curator, working_dir):
    flat_file_entry_ids = get_ids_from_flat_file(flatfile)
    print(flat_file_entry_ids)

    # retrieves latest AC from AC file and deletes it, incrementing next AC
    # While writing creates a temp file, then renames once writing has completed to
    # prevent the original file being destroyed if an error occurs during the write
    # def assign_info():
    # location of folder containing AC list and assigndacs
    assert os.path.exists(working_dir)
    os.chdir(working_dir)

    if not os.path.exists("archive"):
        os.mkdir("archive")

    for file in ["ac_list.txt", "ac_datafile.txt"]:
        shutil.copy2(file, "archive")

    with open("ac_list.txt", "r") as f:
        ac_list = f.read().splitlines()
    n_flat_file_entry_ids = len(flat_file_entry_ids)
    assert len(ac_list) >= n_flat_file_entry_ids
    # inform user when there are less than 10 accessions in ac_list

    new_acs = ac_list[:n_flat_file_entry_ids]
    rest_acs = ac_list[n_flat_file_entry_ids:]

    # add information to end of assigndacs file
    with open("ac_datafile.txt", "a+") as f:
        # TODO: use zip to iterate over new_acs and flat_file_entry_ids at the same time
        for 
            line = " ".join([date_today, new_ac, flat_file_entry_id, user, curator])
            print(f'Writing "{line}" to ac_datafile.txt')
            print(line, file=f)
    with open("ac_list.txt", "w") as f:
        for ac in rest_acs:
            print(ac, file=f)


def get_arguments():
    """
    ./ac_assign.py --flatfile ./test_files/single_flatfile.txt --curator "For Bob's curation work" --working_dir ./test_files
    ac_assign.py --flatfile /foo/bar --curator "For Bob's curation work" """

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
    return parser.parse_args()


# Define main function
def main():
    args = get_arguments()
    write_new_ac(args.flatfile, args.curator, args.working_dir)


# Execute main() function
if __name__ == "__main__":
    main()

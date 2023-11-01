import os
from pathlib import Path
from ac_assign import get_ids_from_flat_file, partition_ac_list, read_ac_list_file

working_dir = "test_files/input"


def test_get_ids_from_flat_file_multiple():
    flatfile = Path("test_files/input/multiple_flatfile.txt")
    assert get_ids_from_flat_file(flatfile) == [
        "CO1AA_EPIMA",
        "CO1A2_EPIMA",
        "CO1AB_EPIMA",
        "CO1AA_EPICS",
        "CO1A2_EPICS",
        "CO1AB_EPICS",
        "CO1AA_EPIAE",
        "CO1A2_EPIAE",
        "CO1AB_EPIAE",
        "CO1AA_EPICA",
        "CO1A2_EPICA",
        "CO1AB_EPICA",
    ]


def test_get_ids_from_flat_file_single():
    flatfile = Path("test_files/input/single_flatfile.txt")
    assert get_ids_from_flat_file(flatfile) == [
        "LOQS_DROME",
    ]


# def test_read_ac_list_file():
#     """
#     TODO
#     1. change directory to test_files/input
#     2. call read_ac_list_file() and assert that
#         a. it has the correct length
#         b. starts with C0HML5 (list[0])
#         c. ends with C0HMR2 (list[-1])
#     """
#     read_ac_list_file()


def test_partition_ac_list():
    flatfile_entry_ids = [
        "CO1AA_EPIMA",
        "CO1A2_EPIMA",
        "CO1AB_EPIMA",
        "CO1AA_EPICS",
    ]
    ac_list = [
        "C0HML5",
        "C0HML6",
        "C0HML7",
        "C0HML8",
        "C0HML9",
        "C0HMM0",
        "C0HMM1",
        "C0HMM2",
        "C0HMM3",
        "C0HMM4",
        "C0HMM5",
    ]
    new_acs, rest_acs = partition_ac_list(ac_list, flatfile_entry_ids)
    assert new_acs == [
        "C0HML5",
        "C0HML6",
        "C0HML7",
        "C0HML8",
    ]
    print(rest_acs)
    assert rest_acs == [
        "C0HML9",
        "C0HMM0",
        "C0HMM1",
        "C0HMM2",
        "C0HMM3",
        "C0HMM4",
        "C0HMM5",
    ]
    assert len(ac_list) == len(new_acs) + len(rest_acs)
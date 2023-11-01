from pathlib import Path
import shutil

from ac_assign import (
    ac_assign,
    generate_ac_datafile_lines,
    get_ids_from_flat_file,
    partition_ac_list,
    read_ac_list_file,
)

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


def test_generate_ac_datafile_lines():
    flatfile_entry_ids = [
        "CO1AA_EPIMA",
        "CO1A2_EPIMA",
        "CO1AB_EPIMA",
        "CO1AA_EPICS",
    ]
    new_acs = [
        "C0HML5",
        "C0HML6",
        "C0HML7",
        "C0HML8",
    ]
    user = "User"
    today = "01/02/03"
    curator = "For Bob's curation work"
    assert list(
        generate_ac_datafile_lines(new_acs, flatfile_entry_ids, today, user, curator)
    ) == [
        "01/02/03 C0HML5 CO1AA_EPIMA User For Bob's curation work",
        "01/02/03 C0HML6 CO1A2_EPIMA User For Bob's curation work",
        "01/02/03 C0HML7 CO1AB_EPIMA User For Bob's curation work",
        "01/02/03 C0HML8 CO1AA_EPICS User For Bob's curation work",
    ]


def test_ac_assign():
    temp_dir = Path("temp")
    test_dir = Path("test_files")
    test_input_dir = Path(test_dir, "input")
    test_output_dir = Path(test_dir, "output")
    temp_dir.mkdir()
    shutil.copytree(test_input_dir, temp_dir)
    flatfile = Path(temp_dir, "multiple_flatfile.txt")
    curator = "For Bob's curation work"
    ac_assign(flatfile, curator, temp_dir)
    for file in ["ac_datafile.txt", "ac_list.txt"]:
        assert list(open(Path(temp_dir, file))) == list(
            open(Path(test_output_dir, file))
        )
    temp_dir.rmdir()

from pathlib import Path
import shutil

from ac_assign import (
    ac_assign,
    generate_ac_datafile_lines,
    get_ids_from_flat_file,
    partition_ac_list,
    read_ac_list_file,
)

user = "User"
today = "01/02/03"
curator = "For Bob's curation work"


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


def test_read_ac_list_file():
    ac_list_file = Path("test_files/input/ac_list.txt")
    ac_list = read_ac_list_file(ac_list_file)
    assert len(ac_list) == 48
    assert ac_list[0] == "C0HML5"
    assert ac_list[-1] == "C0HMR1"


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
    assert list(
        generate_ac_datafile_lines(new_acs, flatfile_entry_ids, today, user, curator)
    ) == [
        "01/02/03 C0HML5 CO1AA_EPIMA User For Bob's curation work",
        "01/02/03 C0HML6 CO1A2_EPIMA User For Bob's curation work",
        "01/02/03 C0HML7 CO1AB_EPIMA User For Bob's curation work",
        "01/02/03 C0HML8 CO1AA_EPICS User For Bob's curation work",
    ]


def test_ac_assign(tmp_path):
    test_path = Path("test_files")
    test_input_path = Path(test_path, "input")
    test_output_path = Path(test_path, "output")
    shutil.copytree(test_input_path, tmp_path, dirs_exist_ok=True)
    flatfile = Path(tmp_path, "multiple_flatfile.txt")
    curator = "For Bob's curation work"
    ac_assign(flatfile, curator, tmp_path, today, user)
    for file in ["ac_datafile.txt", "ac_list.txt"]:
        assert list(open(Path(tmp_path, file))) == list(
            open(Path(test_output_path, file))
        )

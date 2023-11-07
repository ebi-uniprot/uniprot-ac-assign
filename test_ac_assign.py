import shutil
from pathlib import Path

from ac_assign import (
    ac_assign,
    generate_ac_datafile_lines,
    get_backup_file_counters,
    get_counters_to_remove,
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
    assert ac_list[-1] == "C0HMR2"


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


def assert_files_eq(a, b):
    assert list(open(a)) == list(open(b))


def test_ac_assign(tmp_path):
    test_path = Path("test_files")
    test_input_path = test_path / "input"
    test_output_path = test_path / "output"
    tmp_backup_path = tmp_path / "backup"
    tmp_backup_path.mkdir()
    shutil.copytree(test_input_path, tmp_path, dirs_exist_ok=True)
    flatfile = tmp_path / "multiple_flatfile.txt"
    ac_assign(flatfile, curator, tmp_path, today, user)
    for file in ["ac_datafile.txt", "ac_list.txt"]:
        assert_files_eq(tmp_path / file, test_output_path / file)
    for file in ["ac_datafile", "ac_list"]:
        assert_files_eq(
            tmp_backup_path / f"{file}(6).txt", test_input_path / f"{file}.txt"
        )
        old_backup_path = tmp_backup_path / f"{file}(1).txt"
        assert not old_backup_path.exists()


def test_get_backup_file_counters():
    files = [
        "ac_list(1).txt",
        "ac_datafile(1).txt",
        "ac_list(2).txt",
        "ac_datafile(2).txt",
        "ac_list(3).txt",
        "ac_datafile(3).txt",
    ]
    assert get_backup_file_counters([Path(file) for file in files]) == [1, 2, 3]


def test_get_counters_to_remove():
    assert not get_counters_to_remove([1, 2, 3])
    assert not get_counters_to_remove([1, 2, 3, 4, 5])
    assert get_counters_to_remove([1, 2, 3, 4, 5, 6]) == [1]

from pathlib import Path
from ac_assign import get_ids_from_flat_file


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

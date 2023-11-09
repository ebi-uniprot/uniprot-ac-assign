def assert_files_eq(a, b):
    assert list(open(a)) == list(open(b))

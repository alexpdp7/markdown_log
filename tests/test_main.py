import md_log


def test_nothing():
    assert md_log.parse_args([]) is None

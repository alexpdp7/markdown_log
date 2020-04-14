from md_log import daily_targets


def test_matches_filter_no_filter():
    assert daily_targets._matches_filter([], None)


def test_matches_filter():
    assert daily_targets._matches_filter(["foo"], "foo")


def test_matches_filter_any():
    assert daily_targets._matches_filter(["foo", "bar"], "foo")


def test_matches_filter_none():
    assert not daily_targets._matches_filter(["foo", "bar"], "baz")


def test_matches_filter_prefix():
    assert daily_targets._matches_filter([["foo", "bar", "baz"]], ["foo", "bar"])


def test_matches_filter_shorter():
    assert not daily_targets._matches_filter([["foo", "bar"]], ["foo", "bar", "baz"])

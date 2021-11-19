import datetime
import io

import md_log
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


def test_args():
    args = md_log.parse_args(
        ["daily-target", "--filter", "foo", "--target-hours", "3", "log.md"]
    )
    assert args.filter == "foo"
    assert args.target_hours == 3


def test_daily_targets():
    headers, table = daily_targets.create_daily_targets_report(
        [
            io.StringIO(
                """
# 2019-12-03
## 09:00-16:00
### Something

* ...

# 2019-12-04
## 09:00-17:00
### Something

* ...

# 2019-12-05
## 09:00-18:00
### Something

* ...
"""
            )
        ],
        None,
        8,
        False,
    )
    assert headers == ["Date", "Sum", "Target", "Delta", "Running"]
    assert table == [
        [
            datetime.date(2019, 12, 3),
            datetime.timedelta(seconds=7 * 60 * 60),
            "- 8:00:00",
            "= - 1:00:00",
            "+ ↘ = = 0:00:00",
        ],
        [
            datetime.date(2019, 12, 4),
            datetime.timedelta(seconds=8 * 60 * 60),
            "- 8:00:00",
            "= = 0:00:00",
            "+ ↘ = + 1:00:00",
        ],
        [
            datetime.date(2019, 12, 5),
            datetime.timedelta(seconds=9 * 60 * 60),
            "- 8:00:00",
            "= + 1:00:00",
            "+ ↘ = + 1:00:00",
        ],
    ]


def test_daily_targets_digest():
    headers, table = daily_targets.create_daily_targets_report(
        [
            io.StringIO(
                """
# 2019-12-03
## 09:00-17:00
### Something

* ...

# 2019-12-04
## 09:00-16:00
### Something

* ...

# 2019-12-05
## 09:00-16:00
### Something

* ...

# 2019-12-06
## 09:00-18:00
### Something

* ...

# 2019-12-07
## 09:00-18:00
### Something

* ...

# 2019-12-08
## 09:00-16:00
### Something

* ...

# 2019-12-09
## 09:00-16:00
### Something

* ...

# 2019-12-10
## 09:00-18:00
### Something

* ...

# 2019-12-11
## 09:00-18:00
### Something

* ...
"""
            )
        ],
        None,
        8,
        True,
    )
    assert headers == ["Date", "Sum", "Target", "Delta", "Running"]
    assert table == [
        [
            datetime.date(2019, 12, 3),
            datetime.timedelta(seconds=8 * 60 * 60),
            "- 8:00:00",
            "= = 0:00:00",
            "+ ↘ = = 0:00:00",
        ],
        [
            datetime.date(2019, 12, 8),
            datetime.timedelta(seconds=7 * 60 * 60),
            "- 8:00:00",
            "= - 1:00:00",
            "+ ↘ = = 0:00:00",
        ],
        [
            datetime.date(2019, 12, 9),
            datetime.timedelta(seconds=7 * 60 * 60),
            "- 8:00:00",
            "= - 1:00:00",
            "+ ↘ = + 1:00:00",
        ],
        [
            datetime.date(2019, 12, 10),
            datetime.timedelta(seconds=9 * 60 * 60),
            "- 8:00:00",
            "= + 1:00:00",
            "+ ↘ = + 2:00:00",
        ],
        [
            datetime.date(2019, 12, 11),
            datetime.timedelta(seconds=9 * 60 * 60),
            "- 8:00:00",
            "= + 1:00:00",
            "+ ↘ = + 1:00:00",
        ],
    ]

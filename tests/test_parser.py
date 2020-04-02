import datetime
import io

import panflute

from md_log import parser


def test_basic():
    log = """
# 2019-12-03

## 09:00-10:00

### This / is / an / activity

### Another / thing

* I did some stuff
"""
    periods = parser.parse([io.StringIO(log)])
    assert len(periods) == 1
    assert periods[0].begin == datetime.datetime(2019, 12, 3, 9, 0)
    assert periods[0].end == datetime.datetime(2019, 12, 3, 10, 0)
    assert periods[0].task_hierarchies == [
        ["This", "is", "an", "activity"],
        ["Another", "thing"],
    ]
    assert len(periods[0].items) == 1
    assert panflute.stringify(periods[0].items[0]) == "I did some stuff"


def test_warnings():
    walker = parser.Walker()
    log = """
# WTF

## WTF

* ...
"""
    walker.parse_file(io.StringIO(log))
    assert len(walker.periods) == 0
    assert walker.warnings == [
        "Ignoring header for day WTF",
        "Ignoring header for period WTF",
    ]

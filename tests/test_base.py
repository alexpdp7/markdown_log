import datetime
import io

import panflute

import md_log


def test_basic():
    log = """
# 2019-12-03

## 09:00-10:00

### This / is / an / activity

### Another / thing

* I did some stuff
"""
    walker = md_log.Walker()
    walker.parse_file(io.StringIO(log))
    assert len(walker.periods) == 1
    assert walker.periods[0].begin == datetime.datetime(2019, 12, 3, 9, 0)
    assert walker.periods[0].end == datetime.datetime(2019, 12, 3, 10, 0)
    assert walker.periods[0].task_hierarchies == [
        ["This", "is", "an", "activity"],
        ["Another", "thing"],
    ]
    assert len(walker.periods[0].items) == 1
    assert panflute.stringify(walker.periods[0].items[0]) == "I did some stuff"

import collections
import dataclasses
import datetime
import itertools
import sys
import typing

import panflute as pf


@dataclasses.dataclass
class Period:
    begin: datetime.datetime
    end: datetime.datetime
    task_hierarchies: typing.List[typing.List[str]] = dataclasses.field(
        default_factory=list
    )
    items: typing.List[pf.ListItem] = dataclasses.field(default_factory=list)


class Walker:
    def __init__(self):
        self.period = None
        self.periods = []
        self.current_day = None

    def parse_file(self, f):
        doc = pf.convert_text(f.read(), standalone=True)
        doc.walk(self.action)

    def action(self, elem, doc):
        if isinstance(elem, pf.Header):
            if elem.level == 1:
                day_text = elem.content[0].text
                try:
                    self.current_day = datetime.date.fromisoformat(day_text)
                except ValueError:
                    print(f"Ignoring header for day {day_text}")
                    self.current_day = None
            if elem.level == 2:
                period_text = elem.content[0].text
                try:
                    begin_time, end_time = map(
                        datetime.time.fromisoformat, period_text.split("-")
                    )
                    begin = datetime.datetime.combine(self.current_day, begin_time)
                    end = datetime.datetime.combine(self.current_day, end_time)
                    self.period = Period(begin=begin, end=end)
                    self.periods.append(self.period)
                except ValueError:
                    print(f"Ignoring header for period {period_text}")
                    self.period = None
            if elem.level == 3:
                # first, partition on '/'s
                def is_slash(e):
                    return isinstance(e, pf.Str) and e.text == "/"

                parts = [
                    list(content)
                    for group, content in itertools.groupby(elem.content, is_slash)
                    if not group
                ]

                def elem_to_text(e):
                    if isinstance(e, pf.Space):
                        return " "
                    return e.text

                def elems_to_text(e):
                    return " ".join(map(elem_to_text, e)).strip()

                task_hierarchy = list(map(elems_to_text, parts))
                self.period.task_hierarchies.append(task_hierarchy)
        else:
            if self.period and isinstance(elem, pf.ListItem):
                self.period.items.append(elem)


def main():
    with open(sys.argv[1], "r") as f:
        walker = Walker()
        walker.parse_file(f)
        periods = walker.periods
        date_hours = collections.defaultdict(datetime.timedelta)
        for period in periods:
            date_hours[period.begin.date()] += period.end - period.begin
        for date, time in date_hours.items():
            print(date, time)


if __name__ == "__main__":
    main()

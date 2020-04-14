import dataclasses
import datetime
import itertools
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
        self.warnings = []

    def parse_file(self, f):
        doc = pf.convert_text(f.read(), standalone=True)
        doc.walk(self.action)

    def action(self, elem, doc):
        if isinstance(elem, pf.Header):
            if elem.level == 1:
                day_text = elem.content[0].text
                try:
                    self.current_day = datetime.datetime.strptime(
                        day_text, "%Y-%m-%d"
                    ).date()
                except ValueError:
                    if "NOWARN" not in pf.stringify(elem):
                        self.warnings.append(
                            f"Ignoring header for day {pf.stringify(elem)}"
                        )
                    self.current_day = None
            if elem.level == 2:
                period_text = elem.content[0].text
                try:
                    begin_time, end_time = map(
                        lambda d: datetime.datetime.strptime(d, "%H:%M").time(),
                        period_text.split("-"),
                    )
                    begin = datetime.datetime.combine(self.current_day, begin_time)
                    end = datetime.datetime.combine(self.current_day, end_time)
                    self.period = Period(begin=begin, end=end)
                    self.periods.append(self.period)
                except ValueError:
                    if "NOWARN" not in pf.stringify(elem):
                        self.warnings.append(
                            f"Ignoring header for period {pf.stringify(elem)}"
                        )
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


def parse(files):
    walker = Walker()
    for file in files:
        walker.parse_file(file)
    if walker.warnings:
        print("\n".join(walker.warnings))
    return walker.periods

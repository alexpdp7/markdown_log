import collections
import dataclasses
import datetime
import itertools
import typing

import panflute as pf


def bp():
    import sys

    sys.stdin = open("/dev/tty")
    import pdb

    pdb.set_trace()


@dataclasses.dataclass
class Period:
    begin: datetime.datetime
    end: datetime.datetime
    task_hierarchies: typing.List[typing.List[str]] = dataclasses.field(
        default_factory=list
    )
    items: typing.List[pf.ListItem] = dataclasses.field(default_factory=list)


def prepare(doc):
    doc.period = None
    doc.periods = []


def action(elem, doc):
    if isinstance(elem, pf.Header):
        if elem.level == 1:
            day_text = elem.content[0].text
            try:
                doc.current_day = datetime.date.fromisoformat(day_text)
            except ValueError:
                print(f"Ignoring header for day {day_text}")
                doc.current_day = None
        if elem.level == 2:
            period_text = elem.content[0].text
            try:
                begin_time, end_time = map(
                    datetime.time.fromisoformat, period_text.split("-")
                )
                begin = datetime.datetime.combine(doc.current_day, begin_time)
                end = datetime.datetime.combine(doc.current_day, end_time)
                doc.period = Period(begin=begin, end=end)
                doc.periods.append(doc.period)
            except ValueError:
                print(f"Ignoring header for period {period_text}")
                doc.period = None
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
            doc.period.task_hierarchies.append(task_hierarchy)
    else:
        if doc.period and isinstance(elem, pf.ListItem):
            doc.period.items.append(elem)


def finalize(doc):
    date_hours = collections.defaultdict(datetime.timedelta)
    for period in doc.periods:
        date_hours[period.begin.date()] += period.end - period.begin
    for date, time in date_hours.items():
        print(date, time)


def main(doc=None, input_stream=None, output_stream=None):
    return pf.run_filter(
        action,
        prepare=prepare,
        finalize=finalize,
        doc=doc,
        input_stream=input_stream,
        output_stream=output_stream,
    )


if __name__ == "__main__":
    main()

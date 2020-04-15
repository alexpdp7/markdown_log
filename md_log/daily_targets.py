import argparse
import dataclasses
import datetime
import typing

import tabulate

from md_log import parser


HELP = """
For every day, print hours logged and deviation to target from that day until
the last day.

For instance, if on the last day you log one hour above the target, "too much
01:00:00" will be shown as deviation. If the previous day you log two hours
below the target, "too little 01:00:00" will be shown for that day (+1-2). If
the first day you log one hour above the target, "exact 00:00:00" will be shown
for that day.
""".strip()

FILTER_HELP = """
/-separated, only consider periods where one of the task hierarchies begins with
this
""".strip()


def make_parser(subparsers):
    daily_target_parser = subparsers.add_parser("daily-target", description=HELP)
    daily_target_parser.add_argument("--filter", help=FILTER_HELP)
    daily_target_parser.add_argument("--target-hours", default=8, type=int)
    daily_target_parser.add_argument("logfiles", nargs="+", type=argparse.FileType("r"))
    daily_target_parser.set_defaults(func=daily_targets)


def _hierarchy_matches_filter(hierarchy, filter):
    if len(filter) > len(hierarchy):
        return False
    for i, filter_part in enumerate(filter):
        if hierarchy[i] != filter_part:
            return False
    return True


def _matches_filter(task_hierarchies, filter):
    if not filter:
        return True
    return any([_hierarchy_matches_filter(h, filter) for h in task_hierarchies])


def _sign(timedelta):
    if timedelta.total_seconds() > 0:
        return "+"
    if timedelta.total_seconds() < 0:
        return "-"
    return "="


def _format(timedelta):
    return f"{_sign(timedelta)} {abs(timedelta)}"


class Report:
    def __init__(self, target, filter):
        self.target = target
        self.filter = filter
        self.days = dict()

    def _make_day(self, date):
        return Day(date=date, report=self)

    def add_period(self, period):
        if _matches_filter(period.task_hierarchies, self.filter):
            date = period.begin.date()
            day = self.days.get(date, self._make_day(date))
            day.matching_time += period.end - period.begin
            self.days[date] = day

    def update_running_difference_to_target(self):
        target_diff = datetime.timedelta()
        for day in sorted(self.days.keys(), reverse=True):
            target_diff -= self.target
            target_diff += self.days[day].matching_time
            self.days[day].running_difference_to_target = target_diff

    def get_table(self):
        return (
            ["Date", "Sum", "Target", "Delta", "Running"],
            [day.as_row() for _, day in sorted(self.days.items())],
        )


@dataclasses.dataclass
class Day:
    date: datetime.date
    report: Report
    running_difference_to_target: typing.Optional[
        datetime.timedelta
    ] = dataclasses.field(default=None,)
    matching_time: datetime.timedelta = dataclasses.field(
        default_factory=datetime.timedelta,
    )

    @property
    def target(self):
        return self.report.target

    @property
    def difference_to_target(self):
        return self.matching_time - self.target

    def as_row(self):
        return [
            self.date,
            self.matching_time,
            f"- {self.target}",
            "= " + _format(self.difference_to_target),
            "+ \u2198 = " + _format(self.running_difference_to_target),
        ]


def _make_report(periods, filter, target):
    report = Report(target, filter)
    for period in periods:
        report.add_period(period)
    report.update_running_difference_to_target()
    return report


def daily_targets(args):
    periods = parser.parse(args.logfiles)
    filter = args.filter.split("/") if args.filter else None
    report = _make_report(periods, filter, datetime.timedelta(hours=args.target_hours))
    headers, table = report.get_table()
    print(tabulate.tabulate(table, headers, stralign="right"))

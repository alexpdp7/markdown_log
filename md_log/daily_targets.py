import argparse
import collections
import datetime

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
    for i, filter_part in enumerate(filter):
        if hierarchy[i] != filter_part:
            return False
    return True


def _matches_filter(task_hierarchies, filter):
    if not filter:
        return True
    return any([_hierarchy_matches_filter(h, filter) for h in task_hierarchies])


def _make_report(periods, filter, target_hours):
    date_hours = collections.defaultdict(datetime.timedelta)
    for period in periods:
        if _matches_filter(period.task_hierarchies, filter):
            date_hours[period.begin.date()] += period.end - period.begin

    target_diff = datetime.timedelta()
    date_target = dict()
    for day in sorted(date_hours.keys(), reverse=True):
        target_diff += target_hours
        target_diff -= date_hours[day]
        date_target[day] = target_diff
    return date_hours, date_target


def _to_str_target_diff(timedelta):
    type = (
        "exact"
        if timedelta == datetime.timedelta()
        else "too little"
        if timedelta.total_seconds() > 0
        else "too much"
    )
    return f"{type} {abs(timedelta)}"


def daily_targets(args):
    periods = parser.parse(args.logfiles)
    filter = args.filter.split("/") if args.filter else None
    date_hours, date_target = _make_report(
        periods, filter, datetime.timedelta(hours=args.target_hours)
    )
    for day in sorted(date_hours.keys()):
        print(day, date_hours[day], _to_str_target_diff(date_target[day]))

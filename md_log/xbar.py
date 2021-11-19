import argparse
import datetime

import tabulate

from md_log import daily_targets


HELP = """
Acts as an xbar/Argos plugin
""".strip()


def xbar(args):
    print("Log")
    print("---")
    filter = args.filter.split("/") if args.filter else None
    headers, table = daily_targets.create_daily_targets_report(
        [args.logfile], filter, args.target_hours, True
    )
    table = tabulate.tabulate(table, headers, stralign="right", tablefmt="rst")
    table = table.replace("\n", " | font=mono trim=false\n")
    print(table)
    print()
    args.logfile.seek(0)
    found_today = False
    stopped = False
    for line in args.logfile.readlines():
        line = line.strip()
        if datetime.date.today().strftime("# %Y-%m-%d") == line:
            found_today = True
        if "STOP_XBAR" in line:
            stopped = True
        if found_today and not stopped:
            print(line + "| font=mono")
    print("refresh | refresh=true")


def make_parser(subparsers):
    daily_target_parser = subparsers.add_parser("xbar", description=HELP)
    daily_target_parser.add_argument("--filter", help=daily_targets.FILTER_HELP)
    daily_target_parser.add_argument("--target-hours", default=8, type=int)
    daily_target_parser.add_argument("logfile", type=argparse.FileType("r"))
    daily_target_parser.set_defaults(func=xbar)

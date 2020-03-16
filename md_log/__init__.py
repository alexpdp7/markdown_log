import collections
import datetime
import sys

from md_log import parser


def main():
    with open(sys.argv[1], "r") as f:
        periods = parser.parse([f])
        date_hours = collections.defaultdict(datetime.timedelta)
        for period in periods:
            date_hours[period.begin.date()] += period.end - period.begin
        for date, time in date_hours.items():
            print(date, time)


if __name__ == "__main__":
    main()

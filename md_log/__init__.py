import argparse
import sys

from md_log import daily_targets


def parse_args(argv):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    daily_targets.make_parser(subparsers)
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return None
    return args


def main():
    args = parse_args(sys.argv[1:])
    if not args:
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()

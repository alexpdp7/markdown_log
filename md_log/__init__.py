import argparse

from md_log import daily_targets


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    daily_targets.make_parser(subparsers)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

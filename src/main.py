import os
import src.dbt_test_coverage as dbt_test_coverage
import argparse
from pkg_resources import get_distribution


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--recursive",
        help="If you want to search sub directories for yml-files (default: True)",
    )

    args = parser.parse_args()

    if args.recursive:
        recursive = args.recursive
    else:
        recursive = True

    print("")
    print("Running src " + get_distribution("dbt-test-coverage").version)
    print("")

    try:
        dbt_test_coverage.test_coverage(os.getcwd(), recursive=recursive)
    except KeyboardInterrupt:
        print("Interupted by user")


if __name__ == "__main__":
    main()

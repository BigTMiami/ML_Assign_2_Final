import argparse

from helpers import must_exist

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Chart")
    parser.add_argument(
        "job_file",
        help="The job file to run",
    )

    args = parser.parse_args()
    must_exist(args.job_file)

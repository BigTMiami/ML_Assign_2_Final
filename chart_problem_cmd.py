import argparse

from charting import problem_chart
from helpers import must_exist

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Chart")
    parser.add_argument("job_file", help="Job File in experiment folder")
    parser.add_argument(
        "-lengths", nargs="+", type=int, default=[30, 60, 90], help="Lengths to add"
    )
    parser.add_argument("--xscale_log", action="store_true", help="Log the x scale")

    args = parser.parse_args()

    problem_chart(args.job_file, xscale_log=args.xscale_log)

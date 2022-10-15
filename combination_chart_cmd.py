import argparse

from charting import combination_chart
from helpers import must_exist

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Chart")
    parser.add_argument("problem_type", help="Type of problem")
    parser.add_argument("experiment_name", help="Experiment Name - usually length_XX")
    parser.add_argument("--xscale_log", action="store_true", help="Log the x scale")

    args = parser.parse_args()

    combination_chart(args.problem_type, args.experiment_name, xscale_log=args.xscale_log)

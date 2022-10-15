import argparse
from importlib import import_module
from itertools import repeat
from multiprocessing.pool import Pool

from core_code import run_mjob, run_multi_job

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random Optimization Solver Job Runner")
    parser.add_argument("job_files", help="The job file to run", nargs="+")

    args = parser.parse_args()
    for job_file in args.job_files:
        print(f"STARTING {job_file}")
        print("*******************************************")
        run_mjob(job_file)
        print("")

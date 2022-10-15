import argparse
from importlib import import_module

from helpers import must_exist
from core_code import run_algorithm_with_problem

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random Optimization Solver Job Runner")
    parser.add_argument(
        "job_file",
        help="The job file to run",
    )

    args = parser.parse_args()
    must_exist(args.job_file)

    module = args.job_file.replace("/", ".")
    module = module.replace(".py", "")
    job = import_module(module).job

    run_algorithm_with_problem(
        job["problem"],
        job["algorithm"],
        job["length"],
        seed=job["seed"],
        max_iterations=job["max_iterations"],
        max_attempts=job["max_attempts"],
        restarts=job["restarts"],
        temperatures=job["temperatures"],
        decays=job["decays"],
        populations=job["populations"],
        mutations=job["mutations"],
        keep_percents=job["keep_percents"],
    )

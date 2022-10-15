import string
import sys

import six

sys.modules["sklearn.externals.six"] = six
from itertools import repeat
from multiprocessing.pool import Pool
from shutil import copy2
from time import time

import mlrose_hiive as mh
import numpy as np
import pandas as pd

from charting import fitness_chart, problem_chart
from helpers import (
    get_file_and_directory,
    get_filedir,
    import_item_from_module_file,
    load_dict_from_json,
    save_json_to_file,
)
from problems import get_four_peaks_problem, get_k_colors_problem, get_knapsack_problem


def get_problem(problem_type, length, seed):
    maximize = True
    if problem_type == "four_peaks":
        sup_title = f"Four Peaks (length={length})"
        problem = get_four_peaks_problem(length=length)
    elif problem_type == "knapsack":
        sup_title = f"Knapsack (length={length})"
        problem = get_knapsack_problem(length=length, seed=seed)
    elif problem_type == "k_color":
        sup_title = f"K Colors (length={length})"
        problem = get_k_colors_problem(length=length, seed=seed)
        maximize = False
    else:
        raise Exception(f"Unsupported Problem Type of {problem_type}")

    return sup_title, problem, maximize


def get_runner(
    algorithm_type,
    info_settings,
    problem,
    max_iterations,
    experiment_name,
    output_directory,
    seed,
    max_attempts,
    **kwargs,
):
    iteration_list = np.arange(0, max_iterations, max_iterations / 20)
    all_line_cols = []

    if algorithm_type == "rhc":
        if "restarts" not in kwargs:
            print(f"RHC needs restarts")
            return
        info_settings["r"] = kwargs["restarts"]

        runner = mh.RHCRunner(
            problem=problem,
            experiment_name=experiment_name,
            output_directory=output_directory,
            seed=seed,
            iteration_list=iteration_list,
            max_attempts=max_attempts,
            restart_list=kwargs["restarts"],
        )

        title = "Random Hill Climbing"
        line_col = "Restarts"

    elif algorithm_type == "sa":
        if "temperatures" not in kwargs:
            print(f"SA needs -temperatures 1 2 3 ")
            return

        if "decays" not in kwargs:
            print(f"SA needs -decays geom arith exp ")
            return

        decay_list = []
        for decay_type in kwargs["decays"]:
            if decay_type == "geom":
                decay_list.append(mh.GeomDecay)
            elif decay_type == "arith":
                decay_list.append(mh.ArithDecay)
            elif decay_type == "exp":
                decay_list.append(mh.ExpDecay)
            else:
                print(f"Unsupported decay type {decay_type}")
                return

        info_settings["d"] = kwargs["decays"]
        info_settings["t"] = kwargs["temperatures"]

        runner = mh.SARunner(
            problem=problem,
            experiment_name=experiment_name,
            output_directory=output_directory,
            seed=seed,
            iteration_list=iteration_list,
            max_attempts=max_attempts,
            temperature_list=kwargs["temperatures"],
            decay_list=decay_list,
        )

        title = "Simulated Annealing"
        if len(decay_list) > 1:
            line_col = "schedule_type"
        else:
            line_col = "Temperature"

        if len(decay_list) > 1:
            all_line_cols.append("schedule_type")
        if len(kwargs["temperatures"]) > 1:
            all_line_cols.append("Temperature")

    elif algorithm_type == "ga":
        if "populations" not in kwargs:
            print(f"GA needs -populations 50 100 200")
            return
        if "mutations" not in kwargs:
            print(f"GA needs -mutations 0.1 0.2 0.3")
            return

        info_settings["p"] = kwargs["populations"]
        info_settings["mu"] = kwargs["mutations"]

        runner = mh.GARunner(
            problem=problem,
            experiment_name=experiment_name,
            output_directory=output_directory,
            seed=seed,
            iteration_list=iteration_list,
            max_attempts=max_attempts,
            population_sizes=kwargs["populations"],
            mutation_rates=kwargs["mutations"],
        )

        title = "Genetic Algorithm"
        if len(kwargs["populations"]) > 1:
            line_col = "Population Size"
        else:
            line_col = "Mutation Rate"

        if len(kwargs["populations"]) > 1:
            all_line_cols.append("Population Size")
        if len(kwargs["mutations"]) > 1:
            all_line_cols.append("Mutation Rate")

    elif algorithm_type == "mimic":
        if "keep_percents" not in kwargs:
            print(f"MIMIC needs -keep_percents 0.1 0.2 0.3")
            return
        if "populations" not in kwargs:
            print(f"MIMIC needs -populations 50 100 200")
            return

        info_settings["p"] = kwargs["populations"]
        info_settings["k"] = kwargs["keep_percents"]

        runner = mh.MIMICRunner(
            problem=problem,
            experiment_name=experiment_name,
            output_directory=output_directory,
            seed=seed,
            iteration_list=iteration_list,
            max_attempts=max_attempts,
            keep_percent_list=kwargs["keep_percents"],
            population_sizes=kwargs["populations"],
        )

        title = "MIMIC"

        if len(kwargs["populations"]) > 1:
            line_col = "Population Size"
        else:
            line_col = "Keep Percent"

        if len(kwargs["populations"]) > 1:
            all_line_cols.append("Population Size")
        if len(kwargs["keep_percents"]) > 1:
            all_line_cols.append("Keep Percent")

    return runner, title, line_col, all_line_cols


def fitness_chart_from_csv(directory, run_info_file):
    run_file = f"{directory}/{run_info_file}"
    ri = load_dict_from_json(run_file)

    stats_file = f"{directory}/{ri['filename']}"
    df = pd.read_csv(stats_file)
    fitness_chart(
        df,
        ri["line_col"],
        title=ri["title"],
        sup_title=ri["sup_title"],
        maximize=ri["maximize"],
        info_settings=ri["info_settings"],
    )


def run_algorithm_with_problem(
    problem_type,
    algorithm_type,
    length,
    seed=1,
    max_iterations=500,
    max_attempts=50,
    output_directory=None,
    **kwargs,
):
    print(f"Starting {problem_type} {algorithm_type} {length} {output_directory}")
    experiment_name = f"length_{length}"
    info_settings = {"l": length, "ma": max_attempts}

    output_directory = (
        f"experiments/{problem_type}" if output_directory is None else output_directory
    )

    sup_title, problem, maximize = get_problem(problem_type, length, seed)

    runner, title, line_col, all_line_cols = get_runner(
        algorithm_type,
        info_settings,
        problem,
        max_iterations,
        experiment_name,
        output_directory,
        seed,
        max_attempts,
        **kwargs,
    )

    # the two data frames will contain the results
    start_time = time()
    df_run_stats, df_run_curves = runner.run()
    run_time = time() - start_time

    best_fitness = df_run_stats["Fitness"].max() if maximize else df_run_stats["Fitness"].min()
    best_settings = {}
    for col in all_line_cols:
        best_col_value = (
            df_run_stats[df_run_stats["Fitness"] == best_fitness]
            .sort_values(by=["Iteration"])[col]
            .iloc[0]
        )
        if (
            isinstance(best_col_value, mh.ArithDecay)
            or isinstance(best_col_value, mh.GeomDecay)
            or isinstance(best_col_value, mh.ExpDecay)
        ):
            best_col_value = best_col_value.init_temp
        best_col_value = (
            int(best_col_value) if isinstance(best_col_value, np.int64) else best_col_value
        )
        best_settings[col] = best_col_value

    print(
        f"    {problem_type} {algorithm_type} {length} Best Fitness: {best_fitness} Run Time of {run_time:0.2f} {best_settings} "
    )

    # Create Header File
    run_info = {
        "run_time": run_time,
        "best_fitness": best_fitness,
        "best_settings": best_settings,
        "stats_file": f"{algorithm_type}__{experiment_name}__run_stats_df.csv",
        "line_col": line_col,
        "all_line_cols": all_line_cols,
        "title": title,
        "sup_title": sup_title,
        "maximize": maximize,
        "info_settings": info_settings,
    }
    save_json_to_file(
        run_info,
        f"{output_directory}/{experiment_name}/{algorithm_type}__{experiment_name}__run_data.json",
    )

    stats_file = f"{output_directory}/{experiment_name}/{algorithm_type}__{experiment_name}__run_stats_df.csv"
    df = pd.read_csv(stats_file)

    if len(all_line_cols) > 1:
        for i in range(len(all_line_cols)):
            col = all_line_cols[i]
            filter_col = all_line_cols[(i + 1) % 2]

            filter_col_best_value = (
                df[df["Fitness"] == best_fitness].sort_values(by=["Iteration"])[filter_col].iloc[0]
            )
            df_filtered = df[df[filter_col] == filter_col_best_value]
            if (
                isinstance(filter_col_best_value, mh.ArithDecay)
                or isinstance(filter_col_best_value, mh.GeomDecay)
                or isinstance(filter_col_best_value, mh.ExpDecay)
            ):
                filter_col_best_value = filter_col_best_value.init_temp

            filter_title = f"{title} ({filter_col}={filter_col_best_value})"

            fitness_chart(
                df_filtered,
                col,
                all_line_cols,
                title=filter_title,
                sup_title=sup_title,
                maximize=maximize,
                info_settings=info_settings,
                filedir=f"{output_directory}/{experiment_name}/",
            )

    fitness_chart(
        df,
        line_col,
        all_line_cols,
        title=title,
        sup_title=sup_title,
        maximize=maximize,
        info_settings=info_settings,
        filedir=f"{output_directory}/{experiment_name}/",
    )

    return best_fitness


def starmap_with_kwargs(pool, fn, args_iter, kwargs_iter):
    args_for_starmap = zip(repeat(fn), args_iter, kwargs_iter)
    return pool.starmap(apply_args_and_kwargs, args_for_starmap)


def apply_args_and_kwargs(fn, args, kwargs):
    return fn(*args, **kwargs)


def run_multi_job(job_file):
    job = import_item_from_module_file(job_file, "job")

    args_iter = []
    kwargs_iter = []
    problem = job["problem"]
    description = job["description"]
    dir_name = f"{problem}_{description}"
    output_directory = get_filedir(dir_name, "experiments")
    # Copy Job
    copy2(job_file, output_directory)

    for length, length_settings in job["lengths"].items():
        for algorithm in length_settings["algorithms"]:
            args_iter.append([problem, algorithm, length])
            kwargs_iter.append(
                {
                    "output_directory": output_directory,
                    "seed": length_settings["seed"],
                    "max_iterations": length_settings["max_iterations"],
                    "max_attempts": length_settings["max_attempts"],
                    "restarts": length_settings["restarts"],
                    "temperatures": length_settings["temperatures"],
                    "decays": length_settings["decays"],
                    "populations": length_settings["populations"],
                    "mutations": length_settings["mutations"],
                    "keep_percents": length_settings["keep_percents"],
                }
            )

    with Pool(8) as pool:
        starmap_with_kwargs(pool, run_algorithm_with_problem, args_iter, kwargs_iter)

    directory, filename = get_file_and_directory(job_file)

    problem_chart(f"{output_directory}/{filename}")


def run_mjob(job_file):
    job = import_item_from_module_file(job_file, "job")

    args_iter = []
    kwargs_iter = []
    problem = job["problem"]
    description = job["description"]
    dir_name = f"{problem}_{description}"
    output_directory = get_filedir(dir_name, "experiments")
    # Copy Job
    copy2(job_file, output_directory)

    for length, length_settings in job["lengths"].items():
        for algorithm, algorithm_settings in length_settings["algorithms"].items():
            args_iter.append([problem, algorithm, length])
            kwargs_iter.append(
                {
                    "output_directory": output_directory,
                    "seed": algorithm_settings["seed"],
                    "max_iterations": algorithm_settings["max_iterations"],
                    "max_attempts": algorithm_settings["max_attempts"],
                    "restarts": algorithm_settings["restarts"]
                    if "restarts" in algorithm_settings
                    else None,
                    "temperatures": algorithm_settings["temperatures"]
                    if "temperatures" in algorithm_settings
                    else None,
                    "decays": algorithm_settings["decays"]
                    if "decays" in algorithm_settings
                    else None,
                    "populations": algorithm_settings["populations"]
                    if "populations" in algorithm_settings
                    else None,
                    "mutations": algorithm_settings["mutations"]
                    if "mutations" in algorithm_settings
                    else None,
                    "keep_percents": algorithm_settings["keep_percents"]
                    if "keep_percents" in algorithm_settings
                    else None,
                }
            )

    with Pool(8) as pool:
        starmap_with_kwargs(pool, run_algorithm_with_problem, args_iter, kwargs_iter)

    directory, filename = get_file_and_directory(job_file)

    problem_chart(f"{output_directory}/{filename}")

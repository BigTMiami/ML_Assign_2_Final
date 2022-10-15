import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from helpers import check_exists, get_file_and_directory, import_item_from_module_file

ALGORITHM_PALETTE = {
    "Genetic Algorithm": (0.12156862745098039, 0.4666666666666667, 0.7058823529411765),
    "MIMIC": (1.0, 0.4980392156862745, 0.054901960784313725),
    "Random Hill Climb": (0.17254901960784313, 0.6274509803921569, 0.17254901960784313),
    "Simulated Annealing": (0.8392156862745098, 0.15294117647058825, 0.1568627450980392),
}

ALGORITHM_NAMES = {
    "sa": "Simulated Annealing",
    "rhc": "Random Hill Climb",
    "ga": "Genetic Algorithm",
    "mimic": "MIMIC",
}

PROBLEM_NAMES = {"four_peaks": "Four Peaks", "knapsack": "Knapsack", "k_color": "K Colors"}


def title_to_filename(title, location="figures", file_ending="png"):
    safe_title = title.replace(" ", "_")
    safe_title = safe_title.replace(":", "_")
    safe_title = safe_title.replace(",", "_")
    safe_title = safe_title.replace("=", "_")
    safe_title = safe_title.replace("[", "")
    safe_title = safe_title.replace("]", "")
    safe_title = safe_title.replace("(", "")
    safe_title = safe_title.replace(")", "")
    safe_title = safe_title.replace("'", "")
    return f"{location}/{safe_title}.{file_ending}"


def save_to_file(plt, title, filedir=None):
    filedir = "figures" if filedir is None else filedir
    filename = title_to_filename(title, location=filedir)
    if os.path.exists(filename):
        os.remove(filename)
    plt.savefig(fname=filename, bbox_inches="tight")


def clean_settings(settings, to_string=True):
    if len(settings) == 0 and to_string:
        return ""
    settings_copy = settings.copy()

    if settings["algorithm"] == "rhc":
        del settings_copy["temperature"]
        del settings_copy["min_temp"]
        del settings_copy["decay"]
        del settings_copy["population"]
        del settings_copy["mutation"]
    elif settings["algorithm"] == "sa":
        del settings_copy["restart"]
        del settings_copy["population"]
        del settings_copy["mutation"]
    elif settings["algorithm"] == "ga":
        del settings_copy["restart"]
        del settings_copy["temperature"]
        del settings_copy["min_temp"]
        del settings_copy["decay"]
        del settings_copy["population"]
        del settings_copy["mutation"]
    elif settings["algorithm"] == "backprop":
        del settings_copy["restart"]
        del settings_copy["temperature"]
        del settings_copy["min_temp"]
        del settings_copy["decay"]
        del settings_copy["population"]
        del settings_copy["mutation"]
        del settings_copy["max_iters"]
        del settings_copy["max_attempts"]
    else:
        print(f"Unsupported Algorithm type {settings['algorithm']}")

    del settings_copy["capture_iteration_values"]
    del settings_copy["algorithm"]

    if to_string:
        return dict_to_str(settings_copy)
    else:
        return settings_copy


def save_run_info(settings, training_time, epoch_values):

    settings_str = clean_settings(settings)

    title = "nn_run_info" + settings_str
    filename = title_to_filename(title, location="Document/figures/neural", file_ending="pkl")

    save_dict = {}
    save_dict["settings"] = settings
    save_dict["training_time"] = training_time
    save_dict["epoch_values"] = epoch_values

    with (open(filename, "wb")) as f:
        pickle.dump(save_dict, f)


def load_run_info(filename):
    with (open(filename, "rb")) as f:
        run_info = pickle.load(f)

    return run_info["settings"], run_info["training_time"], run_info["epoch_values"]


def dict_to_str(values):
    dict_string = ""
    for key, value in values.items():
        if isinstance(value, list):
            values = ""
            for v in value:
                values += f"{v}_"
            values = values[:-1]
        else:
            values = value
        dict_string += f"_{key}_{values}"
    dict_string += "_"
    return dict_string


def fitness_chart(
    df,
    line_col,
    all_line_cols,
    title="TITLE",
    sup_title="SUPTITLE",
    maximize=True,
    xscale_log=False,
    info_settings={},
    external_ax=None,
    include_legend=True,
    use_algorithm_palette=False,
    filedir=None,
    include_y_label=True,
):
    # df_max = df.groupby(["Iteration", line_col]).agg({"Fitness": "max"}).reset_index()

    if external_ax is None:
        fig, ax = plt.subplots(1, figsize=(4, 5))
        fig.suptitle(sup_title, fontsize=16)
    else:
        ax = external_ax

    if not maximize:
        ax.invert_yaxis()
    if xscale_log:
        ax.set_xscale("log")

    ax.set_title(title)
    palette = ALGORITHM_PALETTE if use_algorithm_palette else sns.color_palette()

    sns.lineplot(
        data=df,
        x="Iteration",
        y="Fitness",
        hue=line_col,
        palette=palette,
        ax=ax,
        legend=include_legend,
    )

    if not include_y_label:
        ax.set(ylabel=None)

    if external_ax is None:
        info_settings_str = dict_to_str(info_settings)
        log_tag = "_log" if xscale_log else ""
        save_to_file(plt, sup_title + " " + title + info_settings_str + log_tag, filedir=filedir)


def time_chart(
    algorithms,
    times,
    title="TITLE",
    sup_title="SUPTITLE",
    info_settings={},
    external_ax=None,
    use_algorithm_palette=False,
    filedir=None,
    y_label=None,
    include_x_label=True,
):
    if external_ax is None:
        fig, ax = plt.subplots(1, figsize=(4, 5))
        fig.suptitle(sup_title, fontsize=16)
    else:
        ax = external_ax
    ax.set_title(title)

    palette = ALGORITHM_PALETTE if use_algorithm_palette else None
    sns.barplot(x=algorithms, y=times, ax=ax, palette=palette)

    ax.set_yscale("log")
    ax.set_xticklabels(
        algorithms,
        rotation=45,
        horizontalalignment="right",
        fontweight="light",
        fontsize="small",
    )
    if y_label is not None:
        ax.set_ylabel(y_label)
    if not include_x_label:
        ax.set_xticklabels([])
    if external_ax is None:
        info_settings_str = dict_to_str(info_settings)
        save_to_file(plt, sup_title + " " + title + info_settings_str, filedir=filedir)


def get_best_fitness(df, maximize):
    return df["Fitness"].max() if maximize else df["Fitness"].min()


def combination_chart(
    problem_type,
    experiment_name,
    xscale_log=True,
    ax_line=None,
    ax_time=None,
    ax_eval=None,
    curve_title=None,
    include_legend=True,
    output_directory=None,
    include_y_label=True,
):

    problem_dict = {"four_peaks": "Four Peaks", "knapsack": "Knapsack", "k_color": "K Colors"}
    if problem_type not in problem_dict:
        print(f"Unsupported problem type of {problem_type}")
        return
    problem_name = problem_dict[problem_type]
    output_directory = (
        f"experiments/{problem_type}" if output_directory is None else output_directory
    )
    maximize = False if problem_type == "k_color" else True

    concat_dfs = []
    times = []
    evals = []
    algorithms = []

    algorithm_type = "ga"
    stats_file = f"{output_directory}/{experiment_name}/{algorithm_type}__{experiment_name}__run_stats_df.csv"
    if check_exists(stats_file):
        algorithms.append(ALGORITHM_NAMES[algorithm_type])
        df = pd.read_csv(stats_file)
        best_fitness = get_best_fitness(df, maximize)
        ga_time = df[df["Fitness"] == best_fitness].sort_values(by=["Iteration"])["Time"].iloc[0]
        ga_evals = (
            df[df["Fitness"] == best_fitness].sort_values(by=["Iteration"])["FEvals"].iloc[0]
        )
        times.append(ga_time)
        evals.append(ga_evals)
        Population_Size = (
            df[df["Fitness"] == best_fitness]
            .sort_values(by=["Iteration"])["Population Size"]
            .iloc[0]
        )
        Mutation_Rate = (
            df[df["Fitness"] == best_fitness]
            .sort_values(by=["Iteration"])["Mutation Rate"]
            .iloc[0]
        )
        df_ga = df[
            (df["Population Size"] == Population_Size) & (df["Mutation Rate"] == Mutation_Rate)
        ][["Iteration", "Fitness"]]
        df_ga["Algorithm Type"] = "Genetic Algorithm"
        concat_dfs.append(df_ga)

    algorithm_type = "mimic"
    stats_file = f"{output_directory}/{experiment_name}/{algorithm_type}__{experiment_name}__run_stats_df.csv"
    if check_exists(stats_file):
        algorithms.append(ALGORITHM_NAMES[algorithm_type])
        df = pd.read_csv(stats_file)
        best_fitness = get_best_fitness(df, maximize)
        mimic_time = (
            df[df["Fitness"] == best_fitness].sort_values(by=["Iteration"])["Time"].iloc[0]
        )
        mimic_evals = (
            df[df["Fitness"] == best_fitness].sort_values(by=["Iteration"])["FEvals"].iloc[0]
        )
        times.append(mimic_time)
        evals.append(mimic_evals)
        Population_Size = (
            df[df["Fitness"] == best_fitness]
            .sort_values(by=["Iteration"])["Population Size"]
            .iloc[0]
        )
        Keep_Percent = (
            df[df["Fitness"] == best_fitness].sort_values(by=["Iteration"])["Keep Percent"].iloc[0]
        )
        df_mimic = df[
            (df["Population Size"] == Population_Size) & (df["Keep Percent"] == Keep_Percent)
        ][["Iteration", "Fitness"]]
        df_mimic["Algorithm Type"] = "MIMIC"
        concat_dfs.append(df_mimic)

    algorithm_type = "rhc"
    stats_file = f"{output_directory}/{experiment_name}/{algorithm_type}__{experiment_name}__run_stats_df.csv"
    if check_exists(stats_file):
        algorithms.append(ALGORITHM_NAMES[algorithm_type])
        df = pd.read_csv(stats_file)
        best_fitness = get_best_fitness(df, maximize)
        rhc_time = df[df["Fitness"] == best_fitness].sort_values(by=["Iteration"])["Time"].iloc[0]
        rhc_evals = (
            df[df["Fitness"] == best_fitness].sort_values(by=["Iteration"])["FEvals"].iloc[0]
        )
        times.append(rhc_time)
        evals.append(rhc_evals)
        restarts = (
            df[df["Fitness"] == best_fitness].sort_values(by=["Iteration"])["Restarts"].iloc[0]
        )
        df_rhc = df[df["Restarts"] == restarts][["Iteration", "Fitness"]]
        df_rhc["Algorithm Type"] = "Random Hill Climb"
        concat_dfs.append(df_rhc)

    algorithm_type = "sa"
    stats_file = f"{output_directory}/{experiment_name}/{algorithm_type}__{experiment_name}__run_stats_df.csv"
    if check_exists(stats_file):
        algorithms.append(ALGORITHM_NAMES[algorithm_type])
        df = pd.read_csv(stats_file)
        best_fitness = get_best_fitness(df, maximize)
        sa_time = df[df["Fitness"] == best_fitness].sort_values(by=["Iteration"])["Time"].iloc[0]
        sa_evals = (
            df[df["Fitness"] == best_fitness].sort_values(by=["Iteration"])["FEvals"].iloc[0]
        )
        times.append(sa_time)
        evals.append(sa_evals)
        schedule_type = (
            df[df["Fitness"] == best_fitness]
            .sort_values(by=["Iteration"])["schedule_type"]
            .iloc[0]
        )
        Temperature = (
            df[df["Fitness"] == best_fitness].sort_values(by=["Iteration"])["Temperature"].iloc[0]
        )
        df_sa = df[(df["Temperature"] == Temperature) & (df["schedule_type"] == schedule_type)][
            ["Iteration", "Fitness"]
        ]
        df_sa["Algorithm Type"] = "Simulated Annealing"
        concat_dfs.append(df_sa)

    df_master = pd.concat(concat_dfs)
    sup_title = f"{problem_name} ({experiment_name})"
    curve_title = "Algorithm Fitness Curves" if curve_title is None else curve_title

    all_line_cols = []

    fitness_chart(
        df_master,
        line_col="Algorithm Type",
        all_line_cols=all_line_cols,
        maximize=maximize,
        title=curve_title,
        sup_title=sup_title,
        xscale_log=xscale_log,
        external_ax=ax_line,
        include_legend=include_legend,
        use_algorithm_palette=True,
        include_y_label=include_y_label,
    )

    y_label = "Time (s)" if include_y_label else None
    time_chart(
        algorithms,
        times,
        title=f"Algorithms by Time",
        sup_title=sup_title,
        external_ax=ax_time,
        use_algorithm_palette=True,
        y_label=y_label,
        include_x_label=False,
    )

    y_label = "Func Evals" if include_y_label else None
    time_chart(
        algorithms,
        evals,
        title=f"Algorithms by Evals",
        sup_title=sup_title,
        external_ax=ax_eval,
        use_algorithm_palette=True,
        y_label=y_label,
    )


def problem_chart(job_file, xscale_log=False):
    file_dir, job_filename = get_file_and_directory(job_file)
    job = import_item_from_module_file(job_file, "job")
    problem = job["problem"]
    lengths = job["lengths"].keys()

    experiment_count = len(lengths)
    fig = plt.figure(figsize=(4 * experiment_count, 8))
    spec = fig.add_gridspec(7, experiment_count)
    ax_lines = []
    ax_times = []
    ax_evals = []
    for i in range(experiment_count):
        axl = fig.add_subplot(spec[0:3, i])
        ax_lines.append(axl)

        axt = fig.add_subplot(spec[3:5, i])
        ax_times.append(axt)

        axe = fig.add_subplot(spec[5:7, i])
        ax_evals.append(axe)

    fig.suptitle(f"{PROBLEM_NAMES[problem]}", fontsize=16)

    for i, length in enumerate(lengths):
        experiment_name = f"length_{length}"
        curve_title = f"Length {length}"
        ax_line = ax_lines[i]
        ax_time = ax_times[i]
        ax_eval = ax_evals[i]
        include_legend = True if i == 0 else False
        include_y_label = i == 0
        combination_chart(
            problem,
            experiment_name,
            ax_line=ax_line,
            ax_time=ax_time,
            ax_eval=ax_eval,
            xscale_log=xscale_log,
            curve_title=curve_title,
            include_legend=include_legend,
            output_directory=file_dir,
            include_y_label=include_y_label,
        )
    handles, labels = ax_lines[0].get_legend_handles_labels()
    ax_lines[0].get_legend().remove()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=4,
        bbox_to_anchor=(0.5, 0.955),
    )
    plt.subplots_adjust(hspace=2)
    save_to_file(plt, f"{problem}", filedir=file_dir)


def neural_training_chart(
    scores,
    start_node=0,
    title="TITLE",
    sup_title="SUPTITLE",
    chart_loss=False,
    location="Document/figures/neural",
    algorithm_settings={},
):
    info_settings_str = clean_settings(algorithm_settings)
    fig, ax = plt.subplots(1, figsize=(4, 5))
    fig.suptitle(title, fontsize=16)
    x = list(range(start_node, len(scores)))
    ax.set_title(sup_title)
    if chart_loss:
        ax.plot(x, scores[start_node:, 1], label="Training Loss")
        ax.set_ylabel("Loss")
    else:
        ax.plot(x, 100.0 - scores[start_node:, 2], label="Training Data")
        ax.plot(x, 100.0 - scores[start_node:, 4], label="Test Data")
        ax.set_ylabel("Error")
    ax.set_xlabel("Epochs")

    plt.legend()

    save_to_file(plt, title + " " + info_settings_str + sup_title, location=location)

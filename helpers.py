import json
import os
from datetime import datetime
from importlib import import_module
from pathlib import Path


def must_exist(file_dir_path):
    path_obj = Path(file_dir_path)
    if not path_obj.exists():
        raise Exception(f"{file_dir_path} does not exist")


def check_exists(file_dir_path):
    return Path(file_dir_path).exists()


def get_file_and_directory(fullfilename):
    path_obj = Path(fullfilename)
    if not path_obj.exists():
        raise Exception(f"{fullfilename} does not exist")
    directory = path_obj.parent
    filename = path_obj.name
    return directory, filename


def save_json_to_file(to_save_dict, file_name):
    with open(file_name, "w") as f:
        json.dump(to_save_dict, f, indent=2)


def load_dict_from_json(file_name):
    with open(file_name) as f:
        return_dict = json.load(f)
    return f


def clean_string(in_string):
    out_string = in_string.replace(" ", "_")
    out_string = out_string.replace(":", "_")
    out_string = out_string.replace(",", "_")
    out_string = out_string.replace("=", "_")
    out_string = out_string.replace(".", "_")
    out_string = out_string.replace("[", "")
    out_string = out_string.replace("]", "")
    out_string = out_string.replace("(", "")
    out_string = out_string.replace(")", "")
    out_string = out_string.replace("'", "")
    out_string = out_string.replace("%", "")
    out_string = out_string.replace("\n", "_")
    return out_string


def clean_parameter(param):
    out_string = param.replace("param_", "")
    out_string = out_string.replace("_", " ")
    out_string = out_string.replace("-", " ")
    return out_string.title()


def title_to_filename(title, file_ending):
    safe_title = clean_string(title)
    if file_ending is None:
        name = f"{safe_title}"
    else:
        name = f"{safe_title}.{file_ending}"
    return name


def get_filedir(title, location):
    """This function creates an id for the evaluation run.
    It then creates a directory to store the data.
    """
    file_dir = f"{title_to_filename(title, None)}_{datetime.now():%m_%d_%H_%M_%S}"
    directory = f"{location}/{file_dir}"

    os.mkdir(directory)
    return directory


def import_item_from_module_file(module_filename, module_item):
    must_exist(module_filename)
    module = module_filename.replace("/", ".")
    module = module.replace(".py", "")
    module = import_module(module)
    return getattr(module, module_item)

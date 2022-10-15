import os

import idx2numpy  # type: ignore
import numpy as np
from scipy.signal import convolve2d

np.set_printoptions(linewidth=400)

data_type = "mnist"

process_type_descriptions = {
    "flat": "MNIST flat: Flat feature scaled, digit labels",
    "array": "MNIST array: Array feature scaled, digit labels",
    "array_convolve": "MNIST array_convolve: Array feature scaled and 2d convolved to 26 X 26, digit labels",
    "flat_convolve": "MNIST flat_convolve: Array feature scaled, 2d convolved to 26 X 26 and then flattened, digit labels",
    "flat_convolve_onehot": "MNIST flat_convolve: Array feature scaled, 2d convolved to 26 X 26 and then flattened, labels (0-9) converted to one hot encoding ",
}

raw_file_location = "data/raw/mnist/"
processed_file_location = "data/processed/mnist/"
if not os.path.exists(processed_file_location):
    os.makedirs(processed_file_location)


def get_file_name(file_type, process_type):
    return f"{processed_file_location}{file_type}_{process_type}.npy"


def get_process_type_description(process_type):
    if process_type not in process_type_descriptions:
        raise Exception(f"Unsupported MNIST Data Process Type of {process_type}")
    return process_type_descriptions[process_type]


def int_to_one_hot(initial_array):
    return np.eye(10)[initial_array]


def save_files(process_type, train_data, train_labels, test_data, test_labels):
    print(f"Saving MNIST {process_type} files")
    train_data = np.save(get_file_name("train_data", process_type), train_data)
    train_labels = np.save(get_file_name("train_labels", process_type), train_labels)
    test_data = np.save(get_file_name("test_data", process_type), test_data)
    test_labels = np.save(get_file_name("test_labels", process_type), test_labels)


def convolve_array(in_array):
    convolve_array = np.ones((3, 3))
    in_array_convolve = np.empty((in_array.shape[0], in_array.shape[1] - 2, in_array.shape[2] - 2))

    for i in range(in_array.shape[0]):
        in_array_convolve[i] = convolve2d(in_array[i], convolve_array, mode="valid")

    return in_array_convolve


def process_mnist_data():
    train_image_file = f"{raw_file_location}train-images-idx3-ubyte"
    train_data = idx2numpy.convert_from_file(train_image_file) / 255
    train_label_file = f"{raw_file_location}train-labels-idx1-ubyte"
    train_labels = idx2numpy.convert_from_file(train_label_file)
    test_image_file = f"{raw_file_location}t10k-images-idx3-ubyte"
    test_data = idx2numpy.convert_from_file(test_image_file) / 255
    test_label_file = f"{raw_file_location}t10k-labels-idx1-ubyte"
    test_labels = idx2numpy.convert_from_file(test_label_file)

    # Save Array
    save_files("array", train_data, train_labels, test_data, test_labels)

    # Process To  Flat
    ti_shape = train_data.shape
    train_data_flat = train_data.reshape(ti_shape[0], ti_shape[1] * ti_shape[2])
    ti_shape = test_data.shape
    test_data_flat = test_data.reshape(ti_shape[0], ti_shape[1] * ti_shape[2])
    save_files("flat", train_data_flat, train_labels, test_data_flat, test_labels)

    # Array Convolve
    train_data_convolve = convolve_array(train_data)
    test_data_convolve = convolve_array(test_data)
    save_files(
        "array_convolve", train_data_convolve, train_labels, test_data_convolve, test_labels
    )

    # Flat Convolve
    ti_shape = train_data_convolve.shape
    train_data_convolve_flat = train_data_convolve.reshape(ti_shape[0], ti_shape[1] * ti_shape[2])
    ti_shape = test_data_convolve.shape
    test_data_convolve_flat = test_data_convolve.reshape(ti_shape[0], ti_shape[1] * ti_shape[2])
    save_files(
        "flat_convolve",
        train_data_convolve_flat,
        train_labels,
        test_data_convolve_flat,
        test_labels,
    )

    # Flat Convolve Onehot
    train_labels_one_hot = int_to_one_hot(train_labels)
    test_labels_one_hot = int_to_one_hot(test_labels)
    save_files(
        "flat_convolve_onehot",
        train_data_convolve_flat,
        train_labels_one_hot,
        test_data_convolve_flat,
        test_labels_one_hot,
    )


def load_mnist_data(process_type, col_to_array=False):
    process_type_desc = get_process_type_description(process_type)

    train_data = np.load(get_file_name("train_data", process_type))
    train_labels = np.load(get_file_name("train_labels", process_type))
    test_data = np.load(get_file_name("test_data", process_type))
    test_labels = np.load(get_file_name("test_labels", process_type))

    if col_to_array:
        print("Col To Array not implemented")
        # train_labels = train_labels.iloc[:, 0]
        # test_labels = test_labels.iloc[:, 0]

    return (process_type_desc, train_data, train_labels, test_data, test_labels)


if __name__ == "__main__":
    process_mnist_data()

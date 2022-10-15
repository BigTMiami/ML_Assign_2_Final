import gzip
import os

import requests


def download_data():

    print("Data Setup Starting")
    root_data_dir = "data/"

    raw_dir = "raw/"
    path = root_data_dir + raw_dir
    if not os.path.exists(path):
        os.makedirs(path)

    # MNIST
    print("Preparing to Download MNIST Data")
    mnist_files = [
        ("http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz", "train-images-idx3-ubyte"),
        ("http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz", "train-labels-idx1-ubyte"),
        ("http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz", "t10k-images-idx3-ubyte"),
        ("http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz", "t10k-labels-idx1-ubyte"),
    ]

    for url, filename in mnist_files:
        data = requests.get(url, allow_redirects=True)

        mnist_path = path + "mnist/"
        if not os.path.exists(mnist_path):
            os.makedirs(mnist_path)

        gz_file = mnist_path + "filename"
        with open(gz_file, "wb") as f:
            f.write(data.content)

        outfile = mnist_path + filename
        with gzip.open(gz_file, "rb") as readfile:
            with open(outfile, "wb") as writefile:
                writefile.write(readfile.read())

        os.remove(gz_file)
        print(f"   {filename} downloaded")

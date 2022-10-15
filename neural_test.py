import mlrose_hiive as mh
from mlrose_hiive.neural.neural_network import NeuralNetwork
from mlrose_hiive.runners import NNGSRunner

from data_mnist import load_mnist_data

grid_search_parameters = {
    "max_iters": [
        4,
        8,
    ],  # nn params
    "learning_rate": [0.001, 0.002],  # nn params
    "schedule": [mh.ArithDecay(1), mh.ArithDecay(100)],  # sa params
}


data_desc, x_train, y_train, x_test, y_test = load_mnist_data("flat_convolve_onehot")


nn_model1 = NeuralNetwork(
    hidden_nodes=[100, 100],
    activation="relu",
    algorithm="random_hill_climb",
    max_iters=1000,
    bias=True,
    is_classifier=True,
    learning_rate=0.0001,
    early_stopping=True,
    clip_max=5,
    max_attempts=100,
    random_state=3,
)

nn_model1.fit(x_train, y_train)


nnr = NNGSRunner(
    x_train=x_train,
    y_train=y_train,
    x_test=x_test,
    y_test=y_test,
    experiment_name="nn_test",
    algorithm=mh.algorithms.sa.simulated_annealing,
    grid_search_parameters=grid_search_parameters,
    iteration_list=[1, 10, 50, 100, 250, 500, 1000, 2500, 5000, 10000],
    hidden_layer_sizes=[[100, 100]],
    bias=True,
    early_stopping=False,
    clip_max=1e10,
    max_attempts=500,
    generate_curves=True,
    seed=1,
)

results = nnr.run()  # GridSearchCV instance returned

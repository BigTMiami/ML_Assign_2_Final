job = {
    "problem": "knapsack",
    "description": "Quick",
    "lengths": {
        30: {
            "algorithms": {
                "rhc": {
                    "max_iterations": 500,
                    "max_attempts": 30,
                    "seed": 1,
                    "restarts": [10],
                },
                "sa": {
                    "max_iterations": 500,
                    "max_attempts": 30,
                    "seed": 1,
                    "temperatures": [1, 10, 100],
                    "decays": ["arith", "geom", "exp"],
                },
                "ga": {
                    "max_iterations": 50,
                    "max_attempts": 5,
                    "seed": 1,
                    "mutations": [
                        0.1,
                        0.2,
                    ],
                    "populations": [100, 200],
                },
                "mimic": {
                    "max_iterations": 50,
                    "max_attempts": 10,
                    "seed": 1,
                    "populations": [100, 200],
                    "keep_percents": [0.1, 0.2],
                },
            }
        },
        60: {
            "algorithms": {
                "rhc": {
                    "max_iterations": 500,
                    "max_attempts": 30,
                    "seed": 1,
                    "restarts": [10],
                },
                "sa": {
                    "max_iterations": 500,
                    "max_attempts": 30,
                    "seed": 1,
                    "temperatures": [1, 10, 100],
                    "decays": ["arith", "geom", "exp"],
                },
                "ga": {
                    "max_iterations": 50,
                    "max_attempts": 5,
                    "seed": 1,
                    "mutations": [
                        0.1,
                        0.2,
                    ],
                    "populations": [100, 200],
                },
                "mimic": {
                    "max_iterations": 50,
                    "max_attempts": 10,
                    "seed": 1,
                    "populations": [100, 200],
                    "keep_percents": [0.1, 0.2],
                },
            }
        },
    },
}

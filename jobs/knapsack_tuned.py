job = {
    "problem": "knapsack",
    "description": "Tuned",
    "lengths": {
        30: {
            "algorithms": {
                "rhc": {
                    "max_iterations": 50,
                    "max_attempts": 30,
                    "seed": 1,
                    "restarts": [100],
                },
                "sa": {
                    "max_iterations": 500,
                    "max_attempts": 50,
                    "seed": 1,
                    "temperatures": [1, 10, 100],
                    "decays": ["arith", "geom", "exp"],
                },
                "ga": {
                    "max_iterations": 50,
                    "max_attempts": 10,
                    "seed": 1,
                    "mutations": [0.1, 0.2],
                    "populations": [100, 200],
                },
                "mimic": {
                    "max_iterations": 50,
                    "max_attempts": 20,
                    "seed": 1,
                    "populations": [100, 200],
                    "keep_percents": [0.05, 0.1],
                },
            }
        },
        60: {
            "algorithms": {
                "rhc": {
                    "max_iterations": 500,
                    "max_attempts": 60,
                    "seed": 1,
                    "restarts": [100],
                },
                "sa": {
                    "max_iterations": 2500,
                    "max_attempts": 90,
                    "seed": 1,
                    "temperatures": [2000, 3000, 4000],
                    "decays": ["arith", "geom", "exp"],
                },
                "ga": {
                    "max_iterations": 500,
                    "max_attempts": 10,
                    "seed": 1,
                    "mutations": [0.1, 0.2, 0.3],
                    "populations": [100, 200, 400],
                },
                "mimic": {
                    "max_iterations": 500,
                    "max_attempts": 10,
                    "seed": 1,
                    "populations": [100, 200, 400],
                    "keep_percents": [0.05, 0.1, 0.2],
                },
            }
        },
        90: {
            "algorithms": {
                "rhc": {
                    "max_iterations": 500,
                    "max_attempts": 60,
                    "seed": 1,
                    "restarts": [100],
                },
                "sa": {
                    "max_iterations": 2500,
                    "max_attempts": 90,
                    "seed": 1,
                    "temperatures": [2000, 3000, 4000],
                    "decays": ["arith", "geom", "exp"],
                },
                "ga": {
                    "max_iterations": 500,
                    "max_attempts": 10,
                    "seed": 1,
                    "mutations": [0.1, 0.2, 0.3],
                    "populations": [100, 200, 400],
                },
                "mimic": {
                    "max_iterations": 500,
                    "max_attempts": 10,
                    "seed": 1,
                    "populations": [100, 200, 400],
                    "keep_percents": [0.05, 0.1, 0.2],
                },
            }
        },
    },
}

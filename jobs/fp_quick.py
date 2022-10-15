job = {
    "problem": "four_peaks",
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
                    "max_iterations": 600,
                    "max_attempts": 30,
                    "seed": 1,
                    "temperatures": [0.1, 1, 10],
                    "decays": ["arith", "geom", "exp"],
                },
                "ga": {
                    "max_iterations": 500,
                    "max_attempts": 10,
                    "seed": 1,
                    "mutations": [0.2],
                    "populations": [200],
                },
                "mimic": {
                    "max_iterations": 500,
                    "max_attempts": 10,
                    "seed": 1,
                    "populations": [200],
                    "keep_percents": [0.1],
                },
            }
        },
        60: {
            "algorithms": {
                "rhc": {
                    "max_iterations": 500,
                    "max_attempts": 10,
                    "seed": 1,
                    "restarts": [5, 10],
                },
                "sa": {
                    "max_iterations": 500,
                    "max_attempts": 20,
                    "seed": 1,
                    "temperatures": [0.1, 1, 10],
                    "decays": [
                        "arith",
                        "geom",
                    ],
                },
                "ga": {
                    "max_iterations": 500,
                    "max_attempts": 20,
                    "seed": 1,
                    "mutations": [0.1, 0.2],
                    "populations": [25, 50],
                },
                "mimic": {
                    "max_iterations": 500,
                    "max_attempts": 10,
                    "seed": 1,
                    "populations": [25, 50],
                    "keep_percents": [0.1],
                },
            }
        },
    },
}

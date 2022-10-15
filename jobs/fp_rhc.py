job = {
    "problem": "four_peaks",
    "description": "RHC",
    "lengths": {
        30: {
            "algorithms": {
                "rhc": {
                    "max_iterations": 500,
                    "max_attempts": 10,
                    "seed": 1,
                    "restarts": [10, 20],
                }
            }
        },
        60: {
            "algorithms": {
                "rhc": {
                    "max_iterations": 500,
                    "max_attempts": 100,
                    "seed": 1,
                    "restarts": [10, 20],
                }
            }
        },
        90: {
            "algorithms": {
                "rhc": {
                    "max_iterations": 500,
                    "max_attempts": 100,
                    "seed": 1,
                    "restarts": [10, 20],
                }
            }
        },
    },
}

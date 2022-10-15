job = {
    "problem": "knapsack",
    "description": "SA Only",
    "lengths": {
        60: {
            "algorithms": {
                "sa": {
                    "max_iterations": 2500,
                    "max_attempts": 90,
                    "seed": 1,
                    "temperatures": [1000, 1500, 2000, 2500, 3000, 3500, 4000],
                    "decays": ["arith", "geom", "exp"],
                },
            }
        },
    },
}

# Test Data & Parameters


# Universal Parameters 7 Defined test parameters
initial_inventory = [12, 12, 12, 12]
holding_costs = [1, 1, 1, 1]
penalty_costs = [2, 2, 2, 2]
time_horizon = 35  # Length of customer demand list
actions = [0, 1, 2, 3]  # Range for Y in X+Y rule according to the paper / action space
state_space = [
    (i, j, k, l)
    for i in range(1, 10)
    for j in range(1, 10)
    for k in range(1, 10)
    for l in range(1, 10)
] # Each agent has 9 possible states


# Test problems data, as can found in the paper
test_problems = {
    "main": {
        "customer_demand": [15, 10, 8, 14, 9, 3, 13, 2, 13, 11, 3, 4, 6, 11, 15, 12, 15, 4, 12, 3, 13, 10, 15, 15, 3,
                            11, 1, 13, 10, 10, 0, 0, 8, 0, 14],
        "lead_times": [2, 0, 2, 4, 4, 4, 0, 2, 4, 1, 1, 0, 0, 1, 1, 0, 1, 1, 2, 1, 1, 1, 4, 2, 2, 1, 4, 3, 4, 1, 4, 0,
                       3, 3, 4]
    },
    "test1": {
        "customer_demand": [5, 14, 14, 13, 2, 9, 5, 9, 14, 14, 12, 7, 5, 1, 13, 3, 12, 4, 0, 15, 11, 10, 6, 0, 6, 6, 5,
                            11, 8, 4, 4, 12, 13, 8, 12],
        "lead_times": [2, 0, 2, 4, 4, 4, 0, 2, 4, 1, 1, 0, 0, 1, 1, 0, 1, 1, 2, 1, 1, 1, 4, 2, 2, 1, 4, 3, 4, 1, 4, 0,
                       3, 3, 4]
    },
    "test2": {
        "customer_demand": [15, 10, 8, 14, 9, 3, 13, 2, 13, 11, 3, 4, 6, 11, 15, 12, 15, 4, 12, 3, 13, 10, 15, 15, 3,
                            11, 1, 13, 10, 10, 0, 0, 8, 0, 14],
        "lead_times": [4, 2, 2, 0, 2, 2, 1, 1, 3, 0, 0, 3, 3, 3, 4, 1, 1, 1, 3, 0, 4, 2, 3, 4, 1, 3, 3, 3, 0, 3, 4, 3,
                       3, 0, 3]
    },
    "test3": {
        "customer_demand": [13, 13, 12, 10, 14, 13, 13, 10, 2, 12, 11, 9, 11, 3, 7, 6, 12, 12, 3, 10, 3, 9, 4, 15, 12,
                            7, 15, 5, 1, 15, 11, 9, 14, 0, 4],
        "lead_times": [4, 2, 2, 0, 2, 2, 1, 1, 3, 0, 0, 3, 3, 3, 4, 1, 1, 1, 3, 0, 4, 2, 3, 4, 1, 3, 3, 3, 0, 3, 4, 3,
                       3, 0, 3]
    }
}

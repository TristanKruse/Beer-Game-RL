# Investigate time_horizon -- q_learning.py
# Bei Analysis ggf. Abweichungen
import time
import pandas as pd
#import numpy as np
#import logging

from environment.supply_chain import SupplyChainEnv
from agent.q_learning import QLearning
from data.test_problems import (
    initial_inventory,
    holding_costs,
    penalty_costs,
    time_horizon,
    actions,
    state_space,
    test_problems,
)
from utils.analysis import print_logs, calculate_rewards, print_simulation_log
from utils.logger import setup_logger


def main():
    # Setup logging
    logger = setup_logger()

    # Record the start time
    start_time = time.time()

    # Initialize environment
    env = SupplyChainEnv(
        initial_inventory,
        holding_costs,
        penalty_costs,
        test_problems["main"]["customer_demand"],
        test_problems["main"]["lead_times"]
    )

    # Initialize Q-learning agent
    agent = QLearning(actions, state_space, max_iterations=100, time_horizon=time_horizon) # Best results were found using 100k iterations

    # Train the agent
    logs, simulation_log = agent.train(env)

    # Analyze and print logs
    print_logs(logs)

    # Analyze rewards for training
    episode_rewards = calculate_rewards(logs)
    print(f"Total rewards for all episodes: {episode_rewards}")

    # Analyze and print simulation log
    print_simulation_log(simulation_log)

    # Save simulation logs to a CSV file
    # df = pd.DataFrame(simulation_log, columns=['State', 'Action', 'Reward', 'Demand', 'Inventory Levels', 'Order Backlog'])
    # df.to_csv('simulation_logs.csv', index=False)
    # print("Simulation logs saved to simulation_logs.csv")

    # Record the end time
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")


# Standard Python entry point
if __name__ == "__main__":
    main()
import pandas as pd


def print_logs(logs, num_episodes=1):
    """
    Prints the logs of the last few episodes.

    Args:
        logs (list): The list of logs from the training process.
        num_episodes (int): Number of recent episodes to print.
    """
    for episode_index in range(-num_episodes, 0):
        episode_log = logs[episode_index]
        df = pd.DataFrame(episode_log, columns=['State', 'Action', 'Reward', 'Demand', 'Inventory Levels', 'Order Backlog'])
        print(f"Episode {len(logs) + episode_index + 1}")
        print(df)
        print("\n")

def calculate_rewards(logs):
    """
    Calculates total rewards per episode.

    Args:
        logs (list): The list of logs from the training process.

    Returns:
        list: Total rewards for each episode.
    """
    episode_rewards = []
    for episode in logs:
        total_episode_reward = sum(log[2] for log in episode)
        episode_rewards.append(total_episode_reward)
    return episode_rewards

def print_simulation_log(simulation_log):
    """
    Prints the simulation log.

    Args:
        simulation_log (list): The log of the simulation process.
    """
    df = pd.DataFrame(simulation_log, columns=['State', 'Action', 'Reward', 'Demand', 'Inventory Levels', 'Order Backlog'])
    print(df)
    print("\n")

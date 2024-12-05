import numpy as np

# Defining the Q-learning agent, RL algorithm
class QLearning:
    def __init__(self, actions, state_space, time_horizon=35, alpha=0.17, gamma=1, epsilon_start=0.98, epsilon_end=0.1,
                 epsilon_final=0.02, max_iterations=1, num_agents=4):
        """
        Initialize the Q-learning agent.

        Args:
            Q_tables (List of Dictionaries): Q-tables for each agent. -> makeing decisions independently
            alpha (float): Learning rate.
            gamma (float): Discount factor.
            epsilon_start (float): Initial exploration rate.
            epsilon_end (float): Final exploration rate.
            epsilon_final (float): Final exploration rate within each period.
            max_iterations (int): Maximum number of iterations for training.
            actions (list): List of possible actions/action space.
            state_space (list): List of all possible states.
            num_agents (int): Number of agents in the supply chain, default 4, see beer game.
        """
        # Initialize Q-table as a List of dictionaries
        self.Q_tables = [{} for _ in range(num_agents)]  # One Q-table per agent
        self.alpha = alpha # Learning rate
        self.gamma = gamma # Discount factor
        self.epsilon_start = epsilon_start # Initial exploration rate
        self.epsilon_end = epsilon_end  # Final exploration rate
        self.epsilon_final = epsilon_final # Final exploration rate within each period
        self.max_iterations = max_iterations # Maximum number of iterations for training
        self.actions = actions # List of possible actions
        self.state_space = state_space # List of all possible states
        self.num_agents = num_agents # Number of agents in the supply chain
        self.time_horizon = time_horizon

    def choose_action(self, state, epsilon):
        """
        Choose an action based on the current state using an epsilon-greedy policy.

        Args:
            state (tuple): The current state.
            epsilon (float): The current exploration rate.

        Returns:
            tuple: The chosen actions as a vector.
        """

        action_vector = []
        # making sure each agent chooses his action on his own, without taking the other agents' actions into account
        for agent in range(self.num_agents):

            # Exploration: choose a random action
            if np.random.rand() < epsilon:
                action = int(np.random.choice(self.actions))
            
            # Exploitation: choose the best action based on the agent's Q-table
            else:
                if state not in self.Q_tables[agent] or not self.Q_tables[agent][state]:
                    action = int(np.random.choice(self.actions))
                else:
                    action = max(self.Q_tables[agent][state], key=self.Q_tables[agent][state].get)
            action_vector.append(action)

        return tuple(action_vector)


    def choose_greedy(self, state):
        """
        Choose the best action based on the current state using a greedy policy.

        Args:
            state (tuple): The current state.

        Returns:
            tuple: The chosen actions as a vector.
        """
        # Exploit: choose the action with the highest Q-value
        action_vector = []

        for agent in range(self.num_agents):
            if state not in self.Q_tables[agent] or not self.Q_tables[agent][state]:
                action = int(np.random.choice(self.actions))
            else:
                action = max(self.Q_tables[agent][state], key=self.Q_tables[agent][state].get)
            action_vector.append(action)
        return tuple(action_vector)


    def update_Q(self, state, action_vector, reward, next_state):
        """
        Update the Q-value for the given state-action pair.

        Args:
            state (tuple): The current state.
            action (tuple): The actions taken.
            reward (int): The reward received.
            next_state (tuple): The next state.
        """

        # Update the Q-value using the Q-learning formula:
        # Q(s, a) = Q(s, a) + alpha * [reward + gamma * max_a' Q(s', a') - Q(s, a)]
        # This incorporates the immediate reward and the estimated optimal future reward,
        # Adjusted by the learning rate (alpha) and the discount factor (gamma)
        
        # Update Q-table for each agent
        for agent in range(self.num_agents):
            action = action_vector[agent]
            
            # Find the maximum Q-value for the next_state over all possible actions for the current agent, defaulting to 0.0 if empty
            max_q_next = max(self.Q_tables[agent][next_state].values(), default=0.0)            

            # Retrieve the current Q-value for the state-action pair, defaulting to 0 if not present
            old_value = self.Q_tables[agent][state].get(action, 0)
            
            # Calculate the TD target
            td_target = reward + self.gamma * max_q_next
            
            # Calculate the TD error
            td_error = td_target - old_value
            
            # Update the Q-value using the Q-learning update rule
            new_value = old_value + self.alpha * td_error
            self.Q_tables[agent][state][action] = new_value


    def train(self, env):
        """
        Train the Q-learning agent.

        Args:
            env (SupplyChainEnv): The environment.

        Returns:
            list: Logs of the training process.
        """

        logs = []
        # Linearly decrease epsilon within the iteration - increasing exploitation
        epsilon_decrement_outer = (self.epsilon_start - self.epsilon_end) / self.max_iterations
        new_epsilon_start = self.epsilon_start
        for iteration in range(self.max_iterations):
            state = env.reset()
            t = 0
            episode_log = []
            # Linearly decrease epsilon within the period - increasing exploitation
            epsilon_decrement = (new_epsilon_start - self.epsilon_final) / self.time_horizon
            epsilon = new_epsilon_start
            reward = 0
            while t < self.time_horizon:
                # a) Select an action using the epsilon-greedy policy
                action_vector = self.choose_action(state, epsilon)

                # Log for each timestamp during training
                episode_log.append((state, action_vector, reward, env.customer_demand[t], list(env.inventory_levels), list(env.order_backlog)))
                
                # b) Caclulate the next state and the reward - includes doing action & doing state vector
                next_state, reward = env.step(action_vector)

                # Update Q-table for each agent
                for agent in range(self.num_agents):
                    action = action_vector[agent]

                    # Fill Q-table with default values if not present
                    if state not in self.Q_tables[agent]:
                        self.Q_tables[agent][state] = {}
                    if action not in self.Q_tables[agent][state]:
                        self.Q_tables[agent][state][action] = 0

                    if next_state not in self.Q_tables[agent]:
                        self.Q_tables[agent][next_state] = {}


                # c) Update Q-table, using next state and actual reward
                self.update_Q(state, tuple(action_vector), reward, next_state)

                # Further decrease epsilon within the period - increasing exploitation
                epsilon -= epsilon_decrement

                # d) update state
                state = next_state

                # e) update time
                t += 1
            
            # Loging the final state of each episode
            episode_log.append((state, action_vector, reward, 0, list(env.inventory_levels), list(env.order_backlog)))
            logs.append(episode_log)

            # Linearly decrease epsilon within the iteration - increasing exploitation
            new_epsilon_start -= epsilon_decrement_outer

        # Run simulation after training is complete
        simulation_log = self.simulation(env)

        return logs, simulation_log
    

    def simulation(self, env):
        """
        Run the greedy policy on the learned Q-table.
        No more exploration, only taking the best action according to the Q-table.

        Args:
            env (SupplyChainEnv): The environment.

        Returns:
            list: Logs of the simulation process.
        """

        state = env.reset()
        t = 0
        simulation_log = []
        reward = 0
        while t < self.time_horizon:
            # Select the best action according to the greedy policy
            action = self.choose_greedy(state)
            simulation_log.append((state, action, reward, env.customer_demand[t], list(env.inventory_levels), list(env.order_backlog)))

            # Calculate the next state and the reward
            next_state, reward = env.step(action)
            
            # Log after each step during simulation

            state = next_state
            t += 1
        
        # Log the final state period 35
        simulation_log.append((state, action, reward, 0, list(env.inventory_levels), list(env.order_backlog)))

        return simulation_log

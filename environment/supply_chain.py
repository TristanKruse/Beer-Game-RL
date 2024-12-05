# Defining the beer Game environment


class SupplyChainEnv:
    def __init__(self, initial_inventory, holding_costs, penalty_costs, customer_demand, lead_times):
        """
        Initialize the environment for the beer game.

        Args:
            initial_inventory (list): Initial inventory levels for each actor in the supply chain.
            holding_costs (list): Holding costs per unit for each level in the supply chain.
            penalty_costs (list): Penalty costs per unit for each level in the supply chain.
            customer_demand (list): List of customer demand values over the time horizon.
            lead_times (list): List of lead times the same for each level.
            current_time (int): The current time step, starting at zero.
            reset (method): adding to init, to not have duplicate code.
        """
        self.initial_inventory = initial_inventory
        self.holding_costs = holding_costs
        self.penalty_costs = penalty_costs
        self.customer_demand = customer_demand
        self.lead_times = lead_times
        self.current_time = 0
        self.reset() 


    def reset(self):
        """
        Reset the environment to its initial state.
        This method sets up the initial conditions of the simulation, including inventory levels and backlogs.
        """
        self.inventory_levels = self.initial_inventory.copy()
        self.order_backlog = [0] * len(self.initial_inventory)
        self.current_time = 0

        # Initialize required inventory list for each agent
        # plus 1 to account for customer demand
        self.required_inventory = [0] * (len(self.initial_inventory)+1)
        
        # Initialize pending orders list for each agent
        self.pending_orders = [[] for _ in range(len(self.initial_inventory))]
        
        # Add initial pending orders of 4 units with lead times 0 and 1 for each agent
        for i in range(len(self.initial_inventory)):
            self.pending_orders[i].append((1, 4))  # Lead time 1
            self.pending_orders[i].append((2, 4))  # Lead time 2
        return self.get_state()


    def get_state(self):
        """
        Get the current state of the environment.
        The state is represented by coded inventory levels.

        Returns:
            tuple: A tuple representing the coded inventory levels.
        """
        # subtracting the backlog from the inventory levels and then coding the state
        return self.code_state(tuple(i - b for i, b in zip(self.inventory_levels, self.order_backlog)))


    def code_state(self, state):
        """
        Encode the state according to predefined ranges into discrete categories.

        Args:
            state (tuple): The actual state as a tuple of inventory levels.

        Returns:
            tuple: The coded state.
        """
        
        # iterating over each element of the state vector and encoding it
        coded_state = []
        for s in state:
            if s <= -6:
                coded_state.append(1)
            elif -6 < s <= -3:
                coded_state.append(2)
            elif -3 < s <= 0:
                coded_state.append(3)
            elif 0 < s <= 3:
                coded_state.append(4)
            elif 3 < s <= 6:
                coded_state.append(5)
            elif 6 < s <= 10:
                coded_state.append(6)
            elif 10 < s <= 15:
                coded_state.append(7)
            elif 15 < s <= 20:
                coded_state.append(8)
            else:
                coded_state.append(9)
        return tuple(coded_state)


    def get_reward(self):
        """
        Calculate the reward based on the current state.
        The reward is negative, representing costs.

        Returns:
            int: The negative cost, calculated as the sum of holding costs and penalty costs.
        """
        holding_cost = sum(
            [self.holding_costs[i] * max(0, self.inventory_levels[i]) for i in range(len(self.inventory_levels))])
        penalty_cost = sum(
            [self.penalty_costs[i] * max(0, self.order_backlog[i]) for i in range(len(self.inventory_levels))])
        return -(holding_cost + penalty_cost)


    def step(self, action):
        """
        Perform a single time step in the environment.

        Args:
            action (list): A list of actions for each agent in the supply chain.

        Returns:
            tuple: The new state and the reward obtained.
        """
        
        # Delivery Process
        for i in range(len(self.inventory_levels)):
            # Get orders that should be delivered at the current time
            orders_to_deliver = [order for order in self.pending_orders[i] if order[0] <= self.current_time]

            # Process each order
            for order in orders_to_deliver:
                delivery_time, amount = order
                self.inventory_levels[i] += amount
                # Remove the fulfilled order from the pending orders list
                self.pending_orders[i].remove(order)


        # Ordering Process
        for i in range(len(self.inventory_levels)):
            if i == 0:
                # For the retailer, set the required inventory directly to the demand
                self.required_inventory[i] = self.customer_demand[self.current_time]
            else:
                # For other agents, calculate the required inventory
                X = self.required_inventory[i-1]
                Y = action[i-1]
                self.required_inventory[i] = X + Y


            # Prioritize fulfilling backorders first
            backorder_fulfilled = 0
            if self.order_backlog[i] > 0:
                if self.inventory_levels[i] >= self.order_backlog[i]:
                    backorder_fulfilled = self.order_backlog[i]
                    self.inventory_levels[i] -= backorder_fulfilled
                    self.order_backlog[i] = 0
                else:
                    backorder_fulfilled = self.inventory_levels[i]
                    self.order_backlog[i] -= backorder_fulfilled
                    self.inventory_levels[i] = 0


            # Attempt to fulfill the current required inventory
            if self.inventory_levels[i] >= self.required_inventory[i]:
                order_fulfilled = self.required_inventory[i]
            else:
                order_fulfilled = self.inventory_levels[i]
                # Adding demand that couldn't be fullfilled to the backlog
                self.order_backlog[i] += self.required_inventory[i] - order_fulfilled

            # Total fulfilled order including backorders and current demand
            total_fulfilled = backorder_fulfilled + order_fulfilled
            self.inventory_levels[i] -= order_fulfilled

            # Update supplier's inventory and add to pending orders list
            # Skip adding to pending orders if i == 0
            if i != 0:
                self.pending_orders[i-1].append((self.current_time + self.lead_times[self.current_time], total_fulfilled))

            # Special handling for the factory (Agent 3)
            if i == 3:
                # The factory can always produce the required amount
                self.required_inventory[i+1] = self.required_inventory[i] + action[i]
                # Record production in pending orders with the appropriate lead time
                self.pending_orders[i].append((self.current_time + self.lead_times[self.current_time], self.required_inventory[i+1]))


        # Delivery Process again, to account for lead times of zero
        for i in range(len(self.inventory_levels)):
            # Get orders that should be delivered at the current time
            orders_to_deliver = [order for order in self.pending_orders[i] if order[0] <= self.current_time]

            # Process each order
            for order in orders_to_deliver:
                delivery_time, amount = order
                self.inventory_levels[i] += amount
                # Remove the fulfilled order from the pending orders list
                self.pending_orders[i].remove(order)

        self.current_time += 1

        return self.get_state(), self.get_reward()
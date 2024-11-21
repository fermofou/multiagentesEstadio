from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

class QueueAgent(Agent):
    """ An agent that represents a person in a queue. """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.queue_id = unique_id % 10  # Assign agent to one of 10 queues
        self.pos = None  # Initialize position as None (will be set later)

    def step(self):
        """ Move agent one step to the left or dequeue if at column 0. """
        if self.pos is None:
            return  # If the agent has been removed from the grid, don't do anything

        x, y = self.pos
        if x > 0:  # Prevent the agent from moving out of the grid
            new_pos = (x - 1, y)
            self.model.grid.move_agent(self, new_pos)
        elif x == 0:
            # Dequeue logic: remove agent from grid when reaching column 0
            self.model.grid.remove_agent(self)
            self.pos = None  # Set position to None after removal

class StadiumModel(Model):
    """ Model representing a stadium with queues. """
    def __init__(self, N):
        self.num_agents = N
        self.grid = MultiGrid(10, 10, True)  # 10x10 grid for visualization
        self.schedule = RandomActivation(self)

        # Create agents and place them in the grid
        for i in range(self.num_agents):
            agent = QueueAgent(i, self)
            self.schedule.add(agent)
            # Spread agents across the grid (modular positioning for queues)
            agent.pos = (i % 10, i // 10)  # Set initial position for the agent
            self.grid.place_agent(agent, agent.pos)

    def step(self):
        """ Advance the model by one step, move agents, and rebalance queues. """
        self.schedule.step()
        self.rebalance_queues()

    def rebalance_queues(self):
        """ Rebalance the queues if a queue exceeds the maximum size. """
        for x in range(10):  # Loop through each queue (column)
            # Collect all agents in this column
            agents_in_queue = [agent for agent in self.grid.get_cell_list_contents([(x, y) for y in range(10)])]

            if len(agents_in_queue) > 25:
                excess_agents = len(agents_in_queue) - 25
                # Move excess agents to other queues with fewer than 10 agents
                for i in range(self.num_agents):
                    if len([agent for agent in self.grid.get_cell_list_contents([(i, y) for y in range(10)])]) < 10:
                        for agent in agents_in_queue[:excess_agents]:
                            # Move agent to a new queue
                            new_pos = (i, (agent.pos[1] + 1) % 10)
                            self.grid.move_agent(agent, new_pos)
                        break  # Stop after moving the excess agents

def agent_portrayal(agent):
    """ Return the portrayal of the agent for visualization. """
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5,
        "Color": "purple",
        "Layer": 0
    }
    return portrayal

# Set up the visualization grid
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
# Set up the server and model
server = ModularServer(StadiumModel,
                       [grid],
                       "Stadium Queue Model",
                       {"N": 100})  # Number of agents
server.port = 8521  # Port number for the simulation
server.launch()

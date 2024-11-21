import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

class QueueAgent(Agent):
    """ An agent that represents a person in a queue. """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.queue_id = unique_id % 10  # Assign agent to a queue

    def step(self):
        # Move agent one step to the left
        x, y = self.pos
        
        if x > 0:
            self.model.grid.move_agent(self, (x - 1, y))

class StadiumModel(Model):
    """A model representing the stadium queues."""
    def __init__(self, N):
        self.num_agents = N
        self.grid = MultiGrid(10, 10, True)
        self.schedule = RandomActivation(self)

        # Create agents and assign them to the grid
        for i in range(self.num_agents):
            agent = QueueAgent(i, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (i % 10, i // 10))

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
        self.rebalance_queues()

    def rebalance_queues(self):
        """Redistribute agents to maintain balance in queues."""
        for x in range(10):
            agents_in_queue = [agent for agent in self.grid.get_cell_list_contents([(x, y) for y in range(10)])]
            
            if len(agents_in_queue) > 14:
                excess_agents = agents_in_queue[14:]  # Get excess agents
                half_excess = len(excess_agents) // 2
                
                # Move half of the excess agents to other queues
                for agent in excess_agents[:half_excess]:
                    target_queue = random.choice([i for i in range(10) if len(self.grid.get_cell_list_contents([(i, y) for y in range(10)])) < 10])
                    self.grid.move_agent(agent, (target_queue, random.randint(0, 9)))

            # Optionally, add new agents randomly to any queue with space
            for x in range(10):
                agents_in_queue = [agent for agent in self.grid.get_cell_list_contents([(x, y) for y in range(10)])]
                if len(agents_in_queue) < 10:
                    num_new_agents = random.randint(0, 10 - len(agents_in_queue))
                    for _ in range(num_new_agents):
                        agent = QueueAgent(self.schedule.get_agent_count(), self)
                        self.schedule.add(agent)
                        self.grid.place_agent(agent, (x, random.randint(0, 9)))

def agent_portrayal(agent):
    """Function to portray the agent on the grid."""
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5,
        "Color": "purple",
        "Layer": 0
    }
    return portrayal

# Set up the visualization grid and server
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(StadiumModel,
                       [grid],
                       "Stadium Queue Model",
                       {"N": 100})
server.port = 8521
server.launch()

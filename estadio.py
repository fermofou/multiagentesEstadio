from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

class QueueAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.queue_id = unique_id % 10  # Assign agent to a queue

    def step(self):
        # Move agent one step to the left
        x, y = self.pos
        if x > 0:
            self.model.grid.move_agent(self, (x - 1, y))

class StadiumModel(Model):
    def __init__(self, N):
        self.num_agents = N
        self.grid = MultiGrid(10, 10, True)
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            agent = QueueAgent(i, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (i % 10, i // 10))

    def step(self):
        self.schedule.step()
        self.rebalance_queues()

    def rebalance_queues(self):
        for x in range(10):
            agents_in_queue = [agent for agent in self.grid.get_cell_list_contents([(x, y) for y in range(10)])]
            if len(agents_in_queue) > 25:
                half = len(agents_in_queue) // 2
                for agent in agents_in_queue[:half]:
                    self.grid.move_agent(agent, (x, (agent.pos[1] + 1) % 10))

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5,
        "Color": "purple",
        "Layer": 0
    }
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(StadiumModel,
                       [grid],
                       "Stadium Queue Model",
                       {"N": 100})
server.port = 8521
server.launch()

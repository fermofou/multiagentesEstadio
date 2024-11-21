# Stadium Queue Model

## Problem

The problem at hand involves simulating a queue management system for a stadium with a dynamic number of fans. Each queue can hold a maximum of 10 fans. Over time, agents (representing fans) enter and exit queues, move within the queues, and are rebalanced based on certain conditions. The main challenges are:
- Managing and redistributing fans across different queues when queues become overcrowded.
- Ensuring random addition of new fans to the system.
- Balancing the queues to avoid bottlenecks while simulating the movement of fans from one location to another.

## Solution

This solution models the queue system using the `Mesa` framework, which is designed for agent-based modeling. The model uses two key classes:

1. **QueueAgent**: Represents an individual fan in the queue. Each agent has a unique ID and is assigned to a queue. They move to the left (i.e., advance in the queue) on each step of the simulation.

2. **StadiumModel**: Represents the stadium as a whole. The model maintains a grid (10x10), where each cell represents a spot in a queue. The model creates a specified number of agents and places them on the grid. It also handles the rebalance of agents between queues when any queue exceeds the maximum capacity of 14 agents. Additionally, it introduces new agents randomly to keep the queues filled.

### Key Features
- **Queue Management**: If a queue exceeds 14 agents, half of the excess agents are moved to other queues with space.
- **Random Addition of Agents**: New fans (agents) are added randomly to queues that have fewer than 10 agents.
- **Fan Movement**: Agents move one step to the left on each simulation step, simulating their movement through the queue.

## How It Works

1. **Initialization**:
    - The model initializes with `N` agents, each randomly placed in the 10x10 grid.
    - Each agent is assigned a unique `queue_id` based on their ID and placed in a queue.
   
2. **Step Logic**:
    - On each step, all agents move one step to the left in their queue (unless they are already at the farthest left).
    - If any queue has more than 14 agents, half of the excess agents are redistributed to other queues with space.
    - New agents are randomly added to any queue that has fewer than 10 agents, ensuring that queues remain populated without exceeding the max limit.

3. **Visualization**:
    - The agents are visualized using `Mesa's` `CanvasGrid`, where each agent is represented as a purple circle.
    - The grid is 10x10, and the agents are moved around the grid according to the simulation rules.

4. **Server**:
    - The model is run on a `ModularServer`, which allows interaction through a web interface. The simulation can be visualized and controlled through the server.

## Requirements

- Python 3.x
- Mesa library

To install the required dependencies, use:

```bash
pip install mesa
```

## How to Run

1. Clone this repository or download the script file.
2. Install the dependencies using the command above.
3. Run the script:

```bash
python stadium_queue_model.py
```

4. Open your browser and go to [http://localhost:8521](http://localhost:8521) to view the simulation.

## Comments

- **Queue Redistribution**: If a queue exceeds 14 agents, we redistribute half of the excess agents to other queues. The target queues are chosen randomly from those that have fewer than 10 agents, ensuring balance across the system.
  
- **Random Addition of New Agents**: At each step, if any queue has fewer than 10 agents, new agents are added randomly to fill those spots. This ensures that the system remains dynamic with the potential for queues to grow over time.

- **Fan Movement**: The fans move from right to left within their respective queues. This simple movement simulates the flow of people through a queue, such as entering the stadium.

## Future Improvements

- **col 0 error**: I'm not sure why column 0 remains with a bug where top and bottom rows are unqued, and they dont fill as agents pass. Could argue it's a feature (they did not meet security protocol).
  
- **Fan Exit Logic**: Add logic to simulate fans leaving the queue once they reach a certain position or after a set number of steps.

---

Let me know if you'd like to adjust or expand on any part!
![image](https://github.com/user-attachments/assets/3724236f-6d88-4f13-a034-adade86387e7)

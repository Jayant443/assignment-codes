import random

class Environment:
    def __init__(self):
        self.locations = ['A', 'B']
        self.status = {loc: random.choice(['Dirty', 'Clean']) for loc in self.locations}
        self.agent_location = random.choice(self.locations)

    def get_state(self):
        return self.agent_location, self.status[self.agent_location]

    def action(self, action):
        if action == 'Suck':
            self.status[self.agent_location] = 'Clean'
        elif action == 'MoveRight':
            self.agent_location = 'B'
        elif action == 'MoveLeft':
            self.agent_location = 'A'

def vacuum_reflex_agent(state):
    location, status = state
    if status == 'Dirty':
        return 'Suck'
    elif location == 'A':
        return 'MoveRight'
    elif location == 'B':
        return 'MoveLeft'

def run(steps):
    env = Environment()
    print(f"Agent at: {env.agent_location}, Status: {env.status}\n")
    for step in range(1, steps + 1):
        state = env.get_state()
        action = vacuum_reflex_agent(state)
        print(f"Step {step}: Location={state[0]}, Status={state[1]}) Action={action}")
        env.action(action)
        print(f"New State: {env.status}, Agent location: {env.agent_location}\n")

    if all(v == 'Clean' for v in env.status.values()):
        print("Environment is cleaned")
    else:
        print("Environment not cleaned")

random.seed(7)
run(steps=6)
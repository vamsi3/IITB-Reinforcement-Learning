import numpy as np


class Trajectory:
    def __init__(self, file):
        with open(file) as f:
            self.num_mdp_states = int(f.readline().strip())
            self.num_mdp_actions = int(f.readline().strip())
            self.mdp_discount = float(f.readline().strip())    
            self.states, self.actions, self.rewards = [], [], []
            for line in f:
                tokens = line.strip().split()
                if len(tokens) == 1:
                    self.states.append(int(tokens[0]))
                    break
                self.states.append(int(tokens[0]))
                self.actions.append(int(tokens[1]))
                self.rewards.append(float(tokens[2]))
            self.num_transitions = len(self.actions)
            self.states = np.array(self.states, dtype=np.int)
            self.actions = np.array(self.actions, dtype=np.int)
            self.rewards = np.array(self.rewards, dtype=np.float)

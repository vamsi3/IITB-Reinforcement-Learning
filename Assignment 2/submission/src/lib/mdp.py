import numpy as np


class MDP:
    def __init__(self, file):
        with open(file) as f:
            self.num_states = int(f.readline().strip())
            self.num_actions = int(f.readline().strip())
            self.R = np.array([[[float(r) for s2, r in enumerate(f.readline().strip().split())]
                                for a in range(self.num_actions)]
                                for s1 in range(self.num_states)], dtype=np.float64)
            self.T = np.array([[[float(p) for s2, p in enumerate(f.readline().strip().split())]
                                for a in range(self.num_actions)]
                                for s1 in range(self.num_states)], dtype=np.float64)
            self.discount = float(f.readline().strip())
            self.type = f.readline().strip()

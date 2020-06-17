import numpy as np


class MultiArmedBandit:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            self.p = np.array([float(p) for p in f.read().splitlines()])
        self.num_arms = len(self.p)
        self.max_p = max(self.p)

    def pull(self, arm_id):
        if (arm_id >= self.num_arms):
            raise IndexError("Arm ID '{}' is not less than arm count {}]".format(arm_id, self.num_arms))
        return np.random.binomial(1, self.p[arm_id])
import numpy as np


class Policy:
    def __init__(self, mdp):
        self.mdp = mdp
        self.set_actions(np.random.randint(
            self.mdp.num_actions, size=self.mdp.num_states, dtype=np.int64))

    def __str__(self):
        string = ""
        for state in range(self.mdp.num_states):
            string += f"{self.values[state]:.16f}\t{self.actions[state]}\n"
        return string[:-1]

    def set_values(self, values):
        self.values = np.asarray(values)
        self.actions = np.argmax(self.Q(), axis=1)
        return self

    def set_actions(self, actions):
        self.actions = np.asarray(actions)
        a = self.mdp.T[np.arange(self.mdp.num_states), self.actions]
        b = np.sum(a * 
            self.mdp.R[np.arange(self.mdp.num_states), self.actions], axis=1)
        a = np.identity(self.mdp.num_states) - self.mdp.discount * a
        self.values = np.linalg.solve(a, b)
        return self

    def Q(self):
        return np.sum(self.mdp.T * (self.mdp.R + 
            self.mdp.discount * self.values[np.newaxis, np.newaxis, :]), axis=2)

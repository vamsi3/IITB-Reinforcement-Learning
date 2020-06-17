import numpy as np


class WindyGridWorld:
    def __init__(self, rows, cols, start, goal, moves, stochastic, wind):
        self.size = np.array([rows, cols], dtype=np.int64)
        self.start = start
        self.goal = goal
        self.moves = moves
        self.stochastic = stochastic
        self.wind = wind
        self.num_states = self.size.prod()
        self.num_actions = self.moves.shape[0]

    def _ravel_state(self, state):
        if not ((0 <= self.state).all() and (self.state < self.size).all()):
            raise ValueError(f"Coordinates of internal state {state} is out of grid with size {self.size}")
        return np.ravel_multi_index(state, dims=self.size)

    # def _unravel_state(self, state):
    #     assert 0 <= state < self.num_states, \
    #         f"Argument 'state' = {state} is out of range [0, {self.num_states})"
    #     return np.unravel_index(state, self.size)

    def observe(self):
        return self._ravel_state(self.state)

    def reset(self):
        self.state = self.start.copy()

    def _step(self, action):
        wind = self.wind[self.state[1]]
        if self.stochastic:
            wind += np.random.randint(-1, 2)
        self.state[0] -= wind
        self.state += self.moves[action]
        self.state = np.maximum(self.state, np.zeros_like(self.state))
        self.state = np.minimum(self.state, self.size - 1)

    def step(self, action):
        self._step(action)
        reward = -1
        return self.observe(), reward, np.all(self.state == self.goal)

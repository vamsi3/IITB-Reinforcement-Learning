import numpy as np


class SARSA:
    def __init__(self, alpha, epsilon):
        self.alpha = alpha
        self.epsilon = epsilon

    @staticmethod
    def _random_argmax(arr):
        return np.random.choice(np.flatnonzero(arr == arr.max()))

    def _epsilon_greedy(self, state):
        if np.random.binomial(1, self.epsilon) == 1:
            action = np.random.randint(self.Q.shape[1])
        else:
            action = self._random_argmax(self.Q[state])
        return action

    def reset(self, num_states, num_actions):
        self.Q = np.zeros((num_states, num_actions), dtype=np.float)

    def explore(self, env):
        state = env.observe()
        action = self._epsilon_greedy(state)
        done = False
        steps = 0
        while not done:
            next_state, reward, done = env.step(action)
            next_action = self._epsilon_greedy(next_state)
            self.Q[state, action] += self.alpha * (reward + self.Q[next_state, next_action] - self.Q[state, action])
            state, action = next_state, next_action
            steps += 1
        return steps

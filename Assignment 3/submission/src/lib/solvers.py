import numpy as np


class Naive:
    def __init__(self):
        self.num_iter = int(1e9)
        self.eps = 1e-9

    def solve(self, trj):
        R = np.zeros((trj.num_mdp_states, trj.num_mdp_actions, trj.num_mdp_states), dtype=np.float)
        T = np.zeros((trj.num_mdp_states, trj.num_mdp_actions, trj.num_mdp_states), dtype=np.float)
        for t in range(trj.num_transitions):
            R[trj.states[t], trj.actions[t], trj.states[t + 1]] = trj.rewards[t]
            T[trj.states[t], trj.actions[t], trj.states[t + 1]] += 1
        Pi = T.sum(-1, keepdims=True)
        np.divide(T, Pi, out=T, where=(Pi != 0))
        Pi = Pi.squeeze()
        Pi_sum = Pi.sum(-1, keepdims=True)
        np.divide(Pi, Pi_sum, out=Pi, where=(Pi_sum != 0))
        del Pi_sum
        V = np.zeros(trj.num_mdp_states)
        for _ in range(self.num_iter):
            V_prev = V.copy()
            V = np.sum(Pi * np.sum(T * (R + trj.mdp_discount * V[np.newaxis, np.newaxis, :]), axis=2), axis=1)
            if (np.abs(V - V_prev) <= self.eps).all():
                break
        return V


class SARSA:
    def __init__(self):
        self.num_iter = 100
        self.alpha = 0.003

    def solve(self, trj):
        Q = np.zeros((trj.num_mdp_states, trj.num_mdp_actions), dtype=np.float)
        Pi = np.zeros((trj.num_mdp_states, trj.num_mdp_actions), dtype=np.float)
        for _ in range(self.num_iter):
            for t in range(trj.num_transitions - 1):
                if t < trj.num_transitions - 1:
                    x = Q[trj.states[t + 1], trj.actions[t + 1]]
                else:
                    x = Q[trj.states[t + 1]].max()
                Q[trj.states[t], trj.actions[t]] += \
                            self.alpha * (trj.rewards[t] + trj.mdp_discount * x - Q[trj.states[t], trj.actions[t]])
                Pi[trj.states[t], trj.actions[t]] += 1
        Pi /= Pi.sum(-1, keepdims=True)
        V = (Q * Pi).sum(1)
        return V


class TDLambda:
    def __init__(self):
        self.num_iter = 30
        self.alpha = 0.003
        self.lambda_ = 0.03

    def solve(self, trj):
        V = np.zeros(trj.num_mdp_states, dtype=np.float)
        for _ in range(self.num_iter):
            eligibility_trace = np.zeros(trj.num_mdp_states, dtype=np.float)
            for t in range(trj.num_transitions):
                delta = trj.rewards[t] + trj.mdp_discount * V[trj.states[t + 1]] - V[trj.states[t]]
                eligibility_trace[trj.states[t]] += 1
                V += self.alpha * delta * eligibility_trace
                eligibility_trace *= self.lambda_ * trj.mdp_discount
        return V


class TDZero:
    def __init__(self):
        self.num_iter = 150
        self.alpha = 0.0003

    def solve(self, trj):
        V = np.zeros(trj.num_mdp_states, dtype=np.float)
        for _ in range(self.num_iter):
            for t in range(trj.num_transitions):
                delta = trj.rewards[t] + trj.mdp_discount * V[trj.states[t + 1]] - V[trj.states[t]]
                V[trj.states[t]] += self.alpha * delta
        return V

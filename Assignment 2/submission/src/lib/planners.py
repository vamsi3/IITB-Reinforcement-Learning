from .policy import Policy
import numpy as np
import pulp


class LinearProgramming:
    def __init__(self):
        pass

    def solve(self, mdp):
        problem = pulp.LpProblem()
        values = pulp.LpVariable.dicts('values', range(mdp.num_states))
        problem += pulp.lpSum(var for var in values.values())
        for s1 in range(mdp.num_states):
            for a in range(mdp.num_actions):
                problem += values[s1] >= pulp.lpSum(mdp.T[s1][a][s2] * (mdp.R[s1][a][s2] + mdp.discount * values[s2])
                                                    for s2 in range(mdp.num_states))
        problem.solve()
        policy = Policy(mdp).set_values([var.varValue for var in values.values()])
        return policy


class HowardPolicyIteration:
    def __init__(self):
        pass

    def solve(self, mdp):
        policy = Policy(mdp)
        while True:
            improved_actions = np.argmax(policy.Q(), axis=1)
            if (policy.actions == improved_actions).all():
                break
            policy.set_actions(improved_actions)
        return policy

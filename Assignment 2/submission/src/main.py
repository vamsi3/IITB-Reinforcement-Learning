from lib.mdp import MDP
from lib.planners import HowardPolicyIteration, LinearProgramming
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--algorithm', type=str, required=True)
parser.add_argument('--mdp', type=str, required=True)

PLANNERS = {
    'hpi': HowardPolicyIteration(),
    'lp': LinearProgramming(),
}

if __name__ == '__main__':
    args = parser.parse_args()
    mdp = MDP(args.mdp)
    planner = PLANNERS[args.algorithm]
    optimal_policy = planner.solve(mdp)
    print(optimal_policy)

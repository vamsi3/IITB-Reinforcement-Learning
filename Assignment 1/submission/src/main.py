from lib.bandit import MultiArmedBandit
from lib.sampler import RoundRobin, EpsilonGreedy, UCB, KLUCB, Thompson
import argparse
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('--instance',   type=str,   required=True)
parser.add_argument('--algorithm',  type=str,   required=True)
parser.add_argument('--randomSeed', type=int,   required=True)
parser.add_argument('--epsilon',    type=float, required=True)
parser.add_argument('--horizon',    type=int,   required=True)


SAMPLERS = {
    'round-robin' : RoundRobin, 
    'epsilon-greedy': EpsilonGreedy, 
    'ucb': UCB, 
    'kl-ucb': KLUCB, 
    'thompson-sampling': Thompson, 
}


if __name__ == '__main__':
    args = parser.parse_args()
    np.random.seed(args.randomSeed)
    bandit = MultiArmedBandit(args.instance)
    if args.algorithm == 'epsilon-greedy':
        sampler = SAMPLERS[args.algorithm](bandit.num_arms, args.epsilon)
    else:
        sampler = SAMPLERS[args.algorithm](bandit.num_arms)
    reward = 0
    for i in range(args.horizon):
        reward += sampler.run(bandit)
    regret = bandit.max_p * args.horizon - reward
    print("{}, {}, {}, {}, {}, {:.2f}".format(args.instance, args.algorithm, args.randomSeed, args.epsilon, args.horizon, regret))
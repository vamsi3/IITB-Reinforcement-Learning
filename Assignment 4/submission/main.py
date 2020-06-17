import argparse
from lib.agents import SARSA
from lib.environments import WindyGridWorld
import matplotlib.pyplot as plt
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--alpha', type=float, default=0.5)
    parser.add_argument('--epsilon', type=float, default=0.1)
    parser.add_argument('--episodes', type=int, default=200)
    parser.add_argument('--seeds', type=int, default=150)
    return parser.parse_args()


def plot(args, ENV_CONFIG, label):
    agent = SARSA(args.alpha, args.epsilon)
    env = WindyGridWorld(**ENV_CONFIG)

    avg_steps = np.zeros(args.episodes)
    for seed in range(args.seeds):
        np.random.seed(seed)
        steps = []
        agent.reset(env.num_states, env.num_actions)
        for episode in range(args.episodes):
            env.reset()
            episode_steps = agent.explore(env)
            steps.append(episode_steps)
        steps = np.cumsum(steps)
        avg_steps += steps
    avg_steps /= args.seeds

    plt.plot(avg_steps, np.arange(1, avg_steps.size + 1), label=label)


def main():
    args = parse_args()

    MOVES       = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]], dtype=np.int64)
    KINGS_MOVES = np.array([[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]], dtype=np.int64)
    
    ENV_CONFIG = {
        'rows': 7,
        'cols': 10,
        'start': np.array([3, 0], dtype=np.int64),
        'goal': np.array([3, 7], dtype=np.int64),
        'wind': np.array([0, 0, 0, 1, 1, 1, 2, 2, 1, 0], dtype=np.int64),
        'moves': MOVES,
        'stochastic': False,
    }

    plot(args, ENV_CONFIG, "Windy GridWorld")
    ENV_CONFIG['moves'] = KINGS_MOVES
    plot(args, ENV_CONFIG, "+ King's Moves")
    ENV_CONFIG['stochastic'] = True
    plot(args, ENV_CONFIG, "+ Stochastic Wind")

    plt.xlabel("Time Steps")
    plt.ylabel("Episodes")
    plt.legend()
    plt.savefig('plot.png')


if __name__ == '__main__':
    main()

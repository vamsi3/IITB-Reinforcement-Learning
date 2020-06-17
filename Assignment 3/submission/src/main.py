import argparse
from lib.solvers import Naive, SARSA, TDLambda, TDZero
from lib.trajectory import Trajectory


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    parser.add_argument('--algorithm', type=str, default='Naive')
    args = parser.parse_args()

    trajectory = Trajectory(args.file)
    solver = eval(args.algorithm)()
    values = solver.solve(trajectory)
    print(*values, sep='\n')

import numpy as np


class Sampler:
    def __init__(self, num_arms):
        self.num_arms = num_arms
        self.reset()

    def reset(self):
        self.arm_rewards = np.zeros(self.num_arms)
        self.arm_pulls = np.zeros(self.num_arms)
        self.num_pulls = 0

    def run(self, bandit):
        arm = self._sample()
        reward = bandit.pull(arm)
        self.arm_rewards[arm] += reward
        self.arm_pulls[arm] += 1
        self.num_pulls += 1
        return reward

    @staticmethod
    def _random_argmax(arr):
        return np.random.choice(np.flatnonzero(arr == arr.max()))

    def _sample(self):
        raise NotImplementedError("Sampler is an Abstract Base Class. Use an actual sampler object.")


class RoundRobin(Sampler):
    def __init__(self, num_arms):
        super().__init__(num_arms)

    def _sample(self):
        return self.num_pulls % self.num_arms


class EpsilonGreedy(Sampler):
    def __init__(self, num_arms, epsilon = 0.5):
        super().__init__(num_arms)
        self.ep = epsilon

    def _sample(self):
        if np.random.binomial(1, self.ep) == 1:
            return np.random.randint(self.num_arms)
        else:
            return self._random_argmax(np.divide(self.arm_rewards, self.arm_pulls, out=np.zeros_like(self.arm_rewards), where=(self.arm_pulls != 0)))


class UCB(Sampler):
    def __init__(self, num_arms):
        super().__init__(num_arms)

    def _sample(self):
        if self.num_pulls < self.num_arms:
            return self.num_pulls
        else:
            return self._random_argmax(self.arm_rewards / self.arm_pulls + np.sqrt(2 * np.log(self.num_pulls) / self.arm_pulls))


class KLUCB(Sampler):
    def __init__(self, num_arms):
        '''The KL-UCB paper states that even though the proof uses c = 3 for regret bounds, in practice
        they recommend to take c = 0 for optimal performance. (Page 4 in arXiv:1102.2490)
        '''
        super().__init__(num_arms)
        self.c = 3

    @staticmethod
    def _root(func, a, b, eps=1e-4):
        while True:
            mid = (a + b) / 2
            func_mid = func(mid)
            if (np.abs(func_mid) < eps).all() and (np.abs(b - a) < eps).all():
                break
            idx = func_mid < 0
            a, b = np.where(idx, mid, a), np.where(idx, b, mid)
        return mid

    def _sample(self):
        if self.num_pulls < self.num_arms:
            return self.num_pulls
        else:
            p = self.arm_rewards / self.arm_pulls
            upper_bound = np.log(1 + self.num_pulls)
            upper_bound = (upper_bound + self.c * np.log(upper_bound)) / self.arm_pulls

            if (p == 1).any():
                return self._random_argmax(p)
            if (p == 0).all():
                return self._random_argmax(upper_bound)

            q_max = np.zeros(self.num_arms)
            q_max[p == 0] = 1 - np.exp(-upper_bound[p == 0])
            idx = (p != 0)
            p = p[idx]
            upper_bound = p * np.log(p) + (1 - p) * np.log(1 - p) - upper_bound[idx]
            q_max[idx] = self._root(lambda q: upper_bound - p * np.log(q) - (1 - p) * np.log(1 - q), a = p, b = np.ones_like(p))
            return self._random_argmax(q_max)


class Thompson(Sampler):
    def __init__(self, num_arms):
        super().__init__(num_arms)

    def _sample(self):
        return self._random_argmax(np.random.beta(1 + self.arm_rewards, 1 + self.arm_pulls - self.arm_rewards))
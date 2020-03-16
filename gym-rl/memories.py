import random
import numpy as np

class BasicMemory:
    def __init__(self, max_memory):
        self._max_memory = max_memory
        self._samples = []
        self._pos = 0

    def add_sample(self, sample):
        if len(self._samples) > self._max_memory:
            self._samples[self._pos] = sample
            self._pos = (self._pos + 1) % len(self._samples)
        else:
            self._samples.append(sample)

    def sample(self, no_samples):
        if no_samples > len(self._samples):
            return random.sample(self._samples, len(self._samples))
        else:
            return random.sample(self._samples, no_samples)

    def all(self):
        return np.array(self._samples)


class OrderedMemory:
    def __init__(self, max_memory):
        self._max_memory = max_memory
        self._memory = []

    def add_samples(self, samples, order):
        def takeFirst(elem):
            return elem[0]

        self._memory.extend([[order, sample] for sample in samples])
        if len(self._memory) > self._max_memory:
            self._memory.sort(key=takeFirst, reverse=True)
            self._memory = self._memory[:int(self._max_memory*0.7)]

    def sample(self, no_samples):
        if no_samples > len(self._memory):
            s = random.sample(self._memory, len(self._memory))
        else:
            s = random.sample(self._memory, no_samples)
        j = [x[1] for x in s]
        return j


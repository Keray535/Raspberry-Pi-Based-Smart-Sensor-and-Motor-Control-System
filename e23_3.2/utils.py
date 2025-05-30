# utils.py
from collections import deque

class MovingAverage:
    def __init__(self, size):
        self.window = deque(maxlen=size)

    def add(self, value):
        if value is not None:
            self.window.append(value)

    def average(self):
        if len(self.window) == self.window.maxlen:
            return sum(self.window) / len(self.window)
        return self.window[-1] if self.window else None
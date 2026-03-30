class BaseAgent:

    def __init__(self):
        self.name = self.__class__.__name__

    def run(self, task):
        raise NotImplementedError("Agents must implement the run() method.")
class BaseWorkflow:
    def __init__(self):
        self.name = self.__class__.__name__

    def run(self, task, orchestrator):
        raise NotImplementedError("Workflows must implement the run() method.")
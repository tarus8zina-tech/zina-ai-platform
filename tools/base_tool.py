class BaseTool:
    def __init__(self):
        self.name = self.__class__.__name__

    def execute(self, payload):
        raise NotImplementedError("Tools must implement the execute() method.")
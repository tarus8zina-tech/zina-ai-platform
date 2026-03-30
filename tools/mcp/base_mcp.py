class BaseMCP:
    def __init__(self, name, status="inactive"):
        self.name = name
        self.status = status

    def activate(self):
        self.status = "active"

    def deactivate(self):
        self.status = "inactive"

    def info(self):
        return {
            "name": self.name,
            "status": self.status,
        }

    def execute(self, payload):
        raise NotImplementedError("MCPs must implement the execute() method.")
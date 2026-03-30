class WorkflowRegistry:
    def __init__(self):
        self.workflows = {}

    def register_workflow(self, name, workflow):
        self.workflows[name] = workflow

    def get_workflow(self, name):
        return self.workflows.get(name)

    def overview(self):
        return list(self.workflows.keys())
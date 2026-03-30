class Registry:
    def __init__(self):
        self.agents = {}
        self.tools = {}
        self.workflows = {}

    def register_agent(self, name, agent):
        self.agents[name] = agent

    def register_tool(self, name, tool):
        self.tools[name] = tool

    def register_workflow(self, name, workflow):
        self.workflows[name] = workflow

    def get_agent(self, name):
        return self.agents.get(name)

    def get_tool(self, name):
        return self.tools.get(name)

    def get_workflow(self, name):
        return self.workflows.get(name)

    def overview(self):
        return {
            "agents": list(self.agents.keys()),
            "tools": list(self.tools.keys()),
            "workflows": list(self.workflows.keys()),
        }
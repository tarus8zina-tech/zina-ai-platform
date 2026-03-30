import os
import importlib


def load_agents(registry):
    agents_folder = "agents"

    for filename in os.listdir(agents_folder):
        if filename.endswith(".py") and filename != "__init__.py":

            module_name = filename[:-3]

            module = importlib.import_module(f"{agents_folder}.{module_name}")

            class_name = "".join(part.capitalize() for part in module_name.split("_"))

            agent_class = getattr(module, class_name)

            registry.register_agent(module_name, agent_class())
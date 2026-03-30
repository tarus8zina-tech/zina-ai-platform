import os
import importlib


def load_workflows(workflow_registry):

    workflows_folder = "workflows"

    for filename in os.listdir(workflows_folder):

        if filename.endswith(".py") and filename not in ["__init__.py", "base_workflow.py", "workflow_registry.py"]:

            module_name = filename[:-3]

            module = importlib.import_module(f"{workflows_folder}.{module_name}")

            class_name = "".join(part.capitalize() for part in module_name.split("_"))

            workflow_class = getattr(module, class_name)

            workflow_registry.register_workflow(module_name, workflow_class())
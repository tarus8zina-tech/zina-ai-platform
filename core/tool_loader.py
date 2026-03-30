import os
import importlib


def load_tools(tool_registry):

    tools_folder = "tools"

    for filename in os.listdir(tools_folder):

        if filename.endswith(".py") and filename not in ["__init__.py", "base_tool.py", "tool_registry.py"]:

            module_name = filename[:-3]

            module = importlib.import_module(f"{tools_folder}.{module_name}")

            class_name = "".join(part.capitalize() for part in module_name.split("_"))

            tool_class = getattr(module, class_name)

            tool_registry.register_tool(module_name, tool_class())
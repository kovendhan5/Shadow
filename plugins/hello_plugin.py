"""
Example plugin for Shadow AI
Each plugin must define a `register()` function that takes the ShadowAI instance.
"""

def register(shadow_ai):
    def hello_plugin_command(command):
        if command.lower().strip() == "hello plugin":
            print("👋 Hello from the plugin system!")
            return True
        return False
    # Register a new command handler
    shadow_ai.plugin_commands.append(hello_plugin_command)

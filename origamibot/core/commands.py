class CommandContainer:
    def __init__(self):
        self.command_holders = []

    def add_command(self, obj):
        self.command_holders.append(obj)

    def find_command(self, command: str) -> list:
        if command.startswith('/'):
            command = command[1:]

        # Do not look for protected/private methods 
        if command.startswith('_'):
            return []

        matches = []
        for holder in self.command_holders:
            if hasattr(holder, command):
                command_handle = getattr(holder, command)
                if callable(command_handle):
                    matches.append(command_handle)
        return matches

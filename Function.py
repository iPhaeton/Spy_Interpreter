class Function:
    def __init__(self, formal, body, environment):
        self.formal = formal
        self.body = body
        self.environment = environment
        self.owner_environment = None

    def set_owner(self, owner_env):
        self.owner_environment = owner_env
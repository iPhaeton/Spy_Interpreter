class Function:
    def __init__(self, formal, body, environment, owner_environment):
        self.formal = formal
        self.body = body
        self.environment = environment
        self.owner_environment = owner_environment
class Environment:
    def __init__(self, initial_dict = {}, parent = None):
        self.dict = initial_dict
        self.parent = parent

    def add(self, name, value):
        self.dict[name] = value
    
    def lookup(self, name):
        try:
            return self.dict[name]
        except KeyError:
            if self.parent != None:
                return self.parent.lookup(name)
            else:
                raise KeyError('No value for "' + name + '" found in the environment.')

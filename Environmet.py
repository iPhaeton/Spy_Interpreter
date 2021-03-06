class Environment:
    def __init__(self, names = [], values = [], parent = None, type = 'general'): #type = 'general' | 'class' | 'instance'
        self.dictionary = {}
        for name, value in zip(names, values):
            self.dictionary[name] = value
        self.parent = parent
        self.type = type

    def add(self, name, value):
        self.dictionary[name] = value
    
    def lookup(self, name):
        try:
            return self.dictionary[name]
        except KeyError:
            if self.parent != None:
                return self.parent.lookup(name)
            else:
                raise KeyError('No value for "' + name + '" found in the environment.')

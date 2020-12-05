class Primitive:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        if len(args) == 1 and args[0] == None:
            return self.func()
        else:
            return self.func(*args)
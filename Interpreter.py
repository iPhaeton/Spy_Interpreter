from Environmet import Environment
from Tokenizer import Tokenizer
from Function import Function

class Interpreter:
    def __init__(self):
        self.global_env = Environment(
            ['+', '-', '*', '/', '=', '>', '<', '>=', '<='],
            [
                lambda a, b: a + b,
                lambda a, b: a - b,
                lambda a, b: a * b,
                lambda a, b: a / b,
                lambda a, b: a == b,
                lambda a, b: a > b,
                lambda a, b: a < b,
                lambda a, b: a >= b,
                lambda a, b: a <= b,
            ],
        )

    def eval(self, form, env=None):
        if (env == None):
            env = self.global_env
        
        if isinstance(form, int):
            return form
        elif isinstance(form, float):
            return form
        elif isinstance(form, str):
            return env.lookup(form)
        elif form[0] == 'begin':
            val = None
            for entry in form[1:]:
                val = self.eval(entry, env)
            return val
        elif form[0] == 'set':
            (_, lhs, rhs) = form
            env.add(lhs, self.eval(rhs, env))
        elif form[0] == 'def':
            (_, name, params, body) = form
            env.add(name, Function(params, body, env))
        elif form[0] == 'if':
            (_, condition, ifBody, elseBody) = form
            if self.eval(condition, env):
                return self.eval(ifBody, env)
            else:
                return self.eval(elseBody, env)
        elif isinstance(form, list):
            f = self.eval(form[0], env)

            if callable(f):
                return f(*[self.eval(x, env) for x in form[1:]])
            else:
                return self.eval(f.body,
                                 Environment(
                                     f.formal,
                                     [self.eval(x, env) for x in form[1:]],
                                     f.environment,
                                 ))
        else:
            raise "Illegal expression: " + str(form)


text1 = '''
    (begin
        (set x 5)
        (def sum (a b) (if (>= a b) (+ (+ a b) x) 0))
        (sum 1 2)
    )
'''
tokenizer = Tokenizer(text1)
expression1 = tokenizer.tokenize()
print(expression1)
interpreter = Interpreter()
value = interpreter.eval(expression1)
print(value)

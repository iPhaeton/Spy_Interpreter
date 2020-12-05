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

    def lhs_eval(self, lhs, env):
        if isinstance(lhs, list):
            (_, object_expr, name) = lhs
            return (self.eval(object_expr, env), name)
        else:
            return (env, lhs)

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
        elif form[0] == 'attr':
            (_, object_expr, name) = form
            return self.eval(object_expr, env).lookup(name)
        elif form[0] == 'set':
            (_, lhs, expr) = form
            (targetEnv, name) = self.lhs_eval(lhs, env)
            targetEnv.add(name, self.eval(expr, env))
        elif form[0] == 'class':
            (_, name, super, body) = form
            if super == 'None':
                super = self.global_env
            class_env = Environment(parent=super)
            env.add(name, lambda: Environment(parent=class_env))
            self.eval(body, class_env)
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
                if (len(form[1:]) == 1 and form[1:][0] == 'None'):
                    return f()
                else:
                    args = [self.eval(x, env) for x in form[1:]]
                    return f(*args)
            else:
                return self.eval(f.body,
                                 Environment(
                                     f.formal,
                                     [self.eval(x, env) for x in form[1:]],
                                     f.environment,
                                 ))
        else:
            raise "Illegal expression: " + str(form)

        # print(env.dictionary)


text1 = '''
    (begin
        (set x 5)
        (def sum (a b) (if (>= a b) (+ (+ a b) x) 0))
        (sum 7 2)
    )
'''

text2 = '''
    (begin
        (set x 0)
        (class Class None
            (begin
                (set a 1)
                (def get_x () x)
                (def get_a () a)
            )
        )
        (set cl (Class None))
        ((attr cl get_a) cl)
    )
'''

tokenizer = Tokenizer(text2)
expression1 = tokenizer.tokenize()
print(expression1)
interpreter = Interpreter()
value = interpreter.eval(expression1)
print(value)

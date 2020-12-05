from Environmet import Environment
from Tokenizer import Tokenizer
from Function import Function
from Primitive import Primitive


class Interpreter:
    def __init__(self):
        self.global_env = Environment(
            ['+', '-', '*', '/', '=', '>', '<', '>=', '<='],
            [
                Primitive(lambda a, b: a + b),
                Primitive(lambda a, b: a - b),
                Primitive(lambda a, b: a * b),
                Primitive(lambda a, b: a / b),
                Primitive(lambda a, b: a == b),
                Primitive(lambda a, b: a > b),
                Primitive(lambda a, b: a < b),
                Primitive(lambda a, b: a >= b),
                Primitive(lambda a, b: a <= b),
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
        elif form == 'None':
            return None
        elif isinstance(form, str):
            return env.lookup(form)
        elif form[0] == 'begin':
            val = None
            for entry in form[1:]:
                val = self.eval(entry, env)
            return val
        elif form[0] == 'attr':
            (_, object_expr, name) = form
            object_instance = self.eval(object_expr, env)
            value = object_instance.lookup(name)
            if (isinstance(value, Function)):
                value.owner_environment = object_instance
            return value
        elif form[0] == 'set':
            (_, lhs, expr) = form
            (targetEnv, name) = self.lhs_eval(lhs, env)
            targetEnv.add(name, self.eval(expr, env))
        elif form[0] == 'class':
            (_, name, super, body) = form
            if super == 'None':
                super = self.global_env
            class_env = Environment(parent=super, type='class')
            env.add(name, Primitive(lambda: Environment(
                parent=class_env, type='instance')))
            self.eval(body, class_env)
        elif form[0] == 'def':
            (_, name, params, body) = form
            func_env = env
            if env.type == 'class':
                func_env = env.parent
            env.add(name, Function(params, body, func_env))
        elif form[0] == 'if':
            (_, condition, ifBody, elseBody) = form
            if self.eval(condition, env):
                return self.eval(ifBody, env)
            else:
                return self.eval(elseBody, env)
        elif isinstance(form, list):
            f = self.eval(form[0], env)

            if callable(f):
                args = [self.eval(x, env) for x in form[1:]]
                return f(*args)
            else:
                args = []
                if f.owner_environment is not None and f.owner_environment.type == 'instance':
                    args.append(f.owner_environment)
                args = args + [self.eval(x, env) for x in form[1:]]

                return self.eval(f.body,
                                 Environment(
                                     f.formal,
                                     args,
                                     f.environment,
                                 ))
        else:
            raise "Illegal expression: " + str(form)

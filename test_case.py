from Tokenizer import Tokenizer
from Interpreter import Interpreter

test_case_1 = '''
    (begin
        (set x 5)
        (def sum (a b) (if (>= a b) (+ (+ a b) x) 0))
        (sum 7 2)
    )
'''

test_case_2 = '''
    (begin
        (set x 0)
        (class Class None
            (begin
                (set a 1)
                (def get_x () x)
                (def get_a (self b) (+ (attr self a) b))
            )
        )
        (set cl (Class None))
        ((attr cl get_a) 2)
    )
'''

tokenizer_1 = Tokenizer(test_case_1)
expression_1 = tokenizer_1.tokenize()
interpreter_1 = Interpreter()
value_1 = interpreter_1.eval(expression_1)
print('test case 1', value_1)

tokenizer_2 = Tokenizer(test_case_2)
expression_2 = tokenizer_2.tokenize()
interpreter_2 = Interpreter()
value_2 = interpreter_2.eval(expression_2)
print('test case 2', value_2)
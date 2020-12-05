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
        (set cl1 (Class None))
        (set val1 ((attr cl1 get_a) 2))

        (set cl2 (Class None))
        (set (attr cl2 a) 3)
        (set val2 ((attr cl2 get_a) 2))

        (+ val1 val2)
    )
'''

tokenizer_1 = Tokenizer(test_case_1)
expression_1 = tokenizer_1.tokenize()
interpreter_1 = Interpreter()
value_1 = interpreter_1.eval(expression_1)
print('test case 1:', value_1) #14

tokenizer_2 = Tokenizer(test_case_2)
expression_2 = tokenizer_2.tokenize()
interpreter_2 = Interpreter()
value_2 = interpreter_2.eval(expression_2)
print('test case 2:', value_2) #8
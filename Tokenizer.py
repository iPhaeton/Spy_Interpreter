class Tokenizer:
    form_start = '('
    form_end = ')'
    index = 0
    space = ' '
    eol = '\n'
    allowed_tokens = ['+', '-', '*', '/', '=']

    def __init__(self, text):
        self.text = text
        self.length = len(text)

    def next(self):
        try:
            next_char = self.text[self.index]
            self.index += 1
            return next_char
        except IndexError:
            return None

    def peek(self):
        try:
            next_char = self.text[self.index]
            return next_char
        except IndexError:
            return None

    def is_token(self, char):
        return char in self.allowed_tokens

    def is_end_of_word(self, char):
        return char == self.eol or char == self.space or char == self.form_start or char == self.form_end or char == None

    def read_word(self):
        word = [self.next()]
        
        if self.is_end_of_word(word[0]):
            return ''.join(word)

        while not self.is_end_of_word(self.peek()):
            word.append(self.next())
        return ''.join(word)

    def tokenize(self):
        form = []

        while self.index < self.length:
            word = self.read_word()
            
            if word == self.form_start:
                form.append(self.tokenize())
            elif word == self.form_end:
                return form
            elif self.is_end_of_word(word):
                continue
            else:
                form.append(word)

        return form

text1 = '(+ 1 (* num -4'
text2 = '''
    (def fizz (x y)
    (+ x y))
'''
text3 = '''
    (begin (def fizz (a b)
    (+ a b))
    (fizz 3 4))
'''
text4 = '''
    (if (= x 3)
    (fizz x 10)
    (+ x 4))
'''
text5 = '''
    (def factorial (x)
    (if (= x 1)
    1
    (* x (factorial (- x 1)))))
'''
tokenizer = Tokenizer(text5)
tokens = tokenizer.tokenize()

print(tokens)

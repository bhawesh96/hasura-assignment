# Define the constants
TT_INT		= 'INT'
TT_STR      = 'STR'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'
TT_COMMA    = ','
DIGITS = '0123456789'  # for positions and page numbers
ALPHABETS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.'  # for image file name

##
# class to handle the character pointer position
class Position:
    def __init__(self, idx):
        self.idx = idx  # position index

    def advance(self):
        self.idx += 1  # increment the index by 1
        return self

##
# class to handle the Tokens. Each token has a type and can have a value
class Token:
    def __init__(self, type, value=None):
        self.type = type  # type of the token (int, str etc)
        self.value = value  # corresponding value

    def __repr__(self):  # method to represent the Token class in pretty format
        if self.value != None: return '{}:{}'.format(self.type, self.value)
        return self.type

##
# method to tokenize the given input text
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = Position(-1)
        self.curr_char = None  # the current character to which the positon index is pointing
        self.advance()

    def advance(self):
        self.pos.advance()
        self.curr_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
    
    ##
    # method to tokenize into chunks
    def make_tokens(self):
        multiline_tokens = []  # list of single-line tokens
        tokens = []  # list of tokens

        while self.curr_char != None:
            if self.curr_char in ' \t':  # space
                self.advance()
            elif self.curr_char in DIGITS:
                tokens.append(self.make_number())
            elif self.curr_char in ALPHABETS:
                tokens.append(self.make_string())
            elif self.curr_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.curr_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.curr_char == ',':
                tokens.append(Token(TT_COMMA))
                self.advance()
            elif self.curr_char == '\n':
                multiline_tokens.append(tokens)
                tokens = []  # clear the tokens
                self.advance()
        multiline_tokens.append(tokens)
        return multiline_tokens
    
    ##
    # method to tokenize the value of integers
    def make_number(self):
        num_str = ''
        while self.curr_char != None and self.curr_char in DIGITS:
            num_str += self.curr_char
            self.advance()
        return Token(TT_INT, int(num_str))
    
    ##
    # method to tokenize the value of strings
    def make_string(self):
        image_file_str = ''
        while self.curr_char != None and self.curr_char in ALPHABETS:
            image_file_str += self.curr_char
            self.advance()
        return Token(TT_STR, image_file_str)

##
# the main driver function
def main():
    with open('input.flip', 'r') as f:
        text = f.read()
    lexer = Lexer(text)  # the lexer object
    tokens = lexer.make_tokens()  # generate the tokens
    print tokens

main()
import sys
from fpdf import FPDF

# Define the constants
TT_INT      = 'INT'
TT_STR      = 'STR'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'
TT_COMMA    = 'COMMA'
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
# Class to define the Flipbook
class FlipBook:
    def __init__(self, init_page, end_page, image_file, x_pos, y_pos):
        self.init_page = init_page
        self.end_page = end_page
        self.image_file = image_file
        self.x_pos = x_pos
        self.y_pos = y_pos


class ElementNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return str(self.tok)

##
# method to Parse the tokens
class Parser:
    def __init__(self, list_of_tokens):
        self.list_of_tokens = list_of_tokens
        self.list_idx = 0
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.list_of_tokens[self.list_idx]):
            self.curr_tok = self.list_of_tokens[self.list_idx][self.tok_idx]
        elif self.list_idx < (len(self.list_of_tokens)-1):
            self.tok_idx = 0
            self.list_idx += 1
            self.curr_tok = self.list_of_tokens[self.list_idx][self.tok_idx]
        return self.curr_tok

    def factor_number(self):
        tok = self.curr_tok
        if tok.type ==  TT_INT:
            self.advance()
            return ElementNode(tok)

    def factor_string(self):
        tok = self.curr_tok
        if tok.type == TT_STR:
            self.advance()
            return ElementNode(tok)

    def parse(self):
        ast_obj = []
        while self.curr_tok.value != None:
            init_page = self.factor_number()
            end_page = self.factor_number()
            image_file = self.factor_string()
            position_string = self.factor_string()

            if self.curr_tok.type == TT_LPAREN:
                self.advance()
                x_pos = self.factor_number()
                self.advance()  # skip comma
                y_pos = self.factor_number()
                self.advance()  # RPAREN
                f = FlipBook(init_page, end_page, image_file, x_pos, y_pos)
                ast_obj.append(f)
        return ast_obj


##
# Method to calculate the end_page for each type of image
def calculate_end_page(ast):
    for index, f in enumerate(ast[:-1]):
        ast[index].end_page = ast[index+1].init_page - 1
    return ast


##
# Method to convert the token_type into the corresponding type (int/str etc)
def convert_tokens_to_var_type(ast):
    for f in ast:
        for key in f.__dict__.keys():
            tok_type = str(f.__dict__[key]).split(':')[0]
            tok_value = str(f.__dict__[key]).split(':')[1]
            if tok_type == 'INT':
                tok_value = int(tok_value)
            elif tok_type == 'STR':
                tok_value = str(tok_value)
            f.__dict__[key] = tok_value
    return ast


##
# Method to generate the PDF using pyPDF
def generate_pdf(ast, output_pdf_file):
    pdf = FPDF()
    for item in ast:
        for page in range(item.init_page, item.end_page+1):
            pdf.add_page()  # add a page
            pdf.image(item.image_file, x=item.x_pos, y=item.y_pos, w=100)  # insert the image at required position
    pdf.output(output_pdf_file)


##
# the main driver function
def main():
    input_args = sys.argv
    input_file = input_args[1]
    output_pdf_file = input_args[-1]
    with open(input_file, 'r') as f:
        text = f.read()
    lexer = Lexer(text)  # the lexer object
    tokens = lexer.make_tokens()  # generate the tokens
    parser = Parser(tokens)  # parse the tokens
    ast = parser.parse()  # get the AST
    ast = convert_tokens_to_var_type(ast)
    ast = calculate_end_page(ast)  # calculate the end_page for each type
    generate_pdf(ast, output_pdf_file)  # generate the PDF


main()
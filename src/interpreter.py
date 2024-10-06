##################
# Constants
###################

DIGITS = '0123456789'

##################
# Tokens
###################

# token types
TT_INT = 'TT_INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'


class Tokens:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self) -> str:
        '''
        Representation for tokens
        '''
        if self.value:
            return (f"Token({self.type}: {self.value})")
        return f"Token({self.type})"


##################
# Error
###################

class Error:
    """
    Generating custom error message
    """
    def __init__(self, pos_start, pos_end, error_name, details):
        self.error_name = error_name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __str__(self):
        # ANSI escape code for red text: \033[91m
        # Reset color with \033[0m
        result: str = f"\033[91m{self.error_name}: {self.details}\033[0m"
        result += f"File: {self.pos_start.file_name}, Line: {self.pos_start.line_no + 1}"
        return  result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character ==> ", details)


##################
# Position
###################

class Position:
    def __init__(self, index, line_no, cols, file_name, ftext):
        self.index = index
        self.line_no = line_no
        self.cols = cols
        self.file_name = file_name
        self.ftext = ftext

    def advance(self, current_char):
        self.index += 1
        self.cols += 1

        if current_char == '\n':
            # check for new line
            self.line_no += 1
            self.cols = 0

        return self     # returns the Position class

    def __copy__(self):
        return Position(self.index, self.line_no, self.cols, self.file_name, self.ftext)

##################
# Lexer
###################

class Lexer:
    def __init__(self, file_name, text):
        self.file_name = file_name
        self.text = text
        self.pos = Position(0, 0, 0, file_name, text)
        self.current_char = self.text[self.pos.index]
        # self.advance()

    def advance(self):
        '''Advancing the current character'''
        self.pos.advance(self.current_char)
        if self.pos.index < len(self.text):
            self.current_char = self.text[self.pos.index]
        else:
            self.current_char = None

    def make_tokens(self):
        tokens = []
        # searching for characters
        while self.current_char != None:
            if self.current_char.isspace():
                self.advance()

            # condition check for operators
            elif self.current_char == '+':
                tokens.append(Tokens(TT_PLUS))
                self.advance()

            elif self.current_char == '-':
                tokens.append(Tokens(TT_MINUS))
                self.advance()

            elif self.current_char == '*':
                tokens.append(Tokens(TT_MUL))
                self.advance()

            elif self.current_char == '/':
                tokens.append(Tokens(TT_DIV))
                self.advance()

            elif self.current_char == '(':
                tokens.append(Tokens(TT_LPAREN))
                self.advance()

            elif self.current_char == ')':
                tokens.append(Tokens(TT_RPAREN))
                self.advance()

            elif self.current_char in DIGITS:
                # for generating numbers
                tokens.append(self.make_numbers())

            else:
                # return some error
                pos_start = self.pos.__copy__()
                char:str = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None     # None for the error may be...


    def make_numbers(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == '.':
                    # breaks the loop if a number already has point
                    break
                dot_count += 1
                num_str += '.'

            else:
                num_str += self.current_char

            self.advance()

        if dot_count == 0:
            return  Tokens(TT_INT, int(num_str))        # for integers
        else:
            return  Tokens(TT_FLOAT, float(num_str))    # for floats


##################
# Run
###################

def run(file_name, text):
    lexer = Lexer(file_name,text)
    tokens, error = lexer.make_tokens()

    return  tokens, error



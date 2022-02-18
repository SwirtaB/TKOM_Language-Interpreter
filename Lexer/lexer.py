from HelperModules.sourcehandler import SourceHandler
from HelperModules.symbols import SymbolsTable, TokenTypes
from HelperModules.errorhandler import LexerError
from Lexer.token import Token

MAX_INT_LITERAL = 2147483647
MAX_FLOAT_LITERAL = 3.402823466e+38
MAX_STRING_SIZE = 2**16

class Lexer:
    def __init__(self, sourceHandler: SourceHandler, symbolsTable: SymbolsTable):
        if sourceHandler is None or symbolsTable is None:
            raise LexerError("SourceHandler was not provided.", None)

        self.sourceHandler = sourceHandler
        self.symbolsTable = symbolsTable
        self.currentToken = None
        self.allowedAfterNumber = ["=", "<", "<=", ">", ">=", "==", "!=", "+", "-", "*", "/", "(", ")", ";", ","]

        self.sourceHandler.get_next_char()

    def __get_current_char(self) -> str:
        return self.sourceHandler.get_current_char()
        
    def __get_next_char(self) -> str:
        return self.sourceHandler.get_next_char()
    
    def __get_position(self) -> tuple:
        return self.sourceHandler.get_position()

    def __try_build_id(self) -> Token:
        position = self.__get_position()

        if self.__get_current_char().isalpha() or self.__get_current_char() == "_":
            buffer = self.__get_current_char()
            while (self.__get_next_char().isalnum() or self.__get_current_char() == "_"):
                buffer += self.__get_current_char()
                if len(buffer) > MAX_STRING_SIZE:
                    raise LexerError("Invalid token, identifier length exceeded 2^16 chars.", self.sourceHandler)
            
            #check if builded identifier is a keyword else it is new identifier
            if buffer in self.symbolsTable.keywordsDict:
                return Token(type=self.symbolsTable.keywordsDict[buffer], value=buffer, position=position)
            else:
                return Token(type=TokenTypes.IDENTIFIER, value=buffer, position=position)

        else:
            return None

    def __try_build_number(self) -> Token:
        position = self.__get_position()

        #building number
        if self.__get_current_char().isdecimal():
            buffer = self.__get_current_char()
            if self.__get_current_char() != '0':
                while self.__get_next_char().isdecimal():
                    buffer += self.__get_current_char()

            else:
                self.__get_next_char()

            #found '.' char
            #building decimal
            if (dotChar := self.__get_current_char()) == '.':
                if self.__get_next_char().isdecimal():
                    buffer += dotChar + self.__get_current_char()
                    while self.__get_next_char().isdecimal():
                        buffer += self.__get_current_char()
                    #check if after decimal occures allowed symbol
                    if not(self.__get_current_char() in self.allowedAfterNumber or self.__get_current_char().isspace()):
                        raise LexerError("Invalid token", self.sourceHandler)

                    return Token(type=TokenTypes.FLOAT_LITERAL, value=float(buffer), position=position)
                else:
                    self.__get_next_char()
                    raise LexerError("Invlaid token, expected decimal after '.'", self.sourceHandler)
            #check if after number occures allowed symbol
            else:
                if not(self.__get_current_char() in self.allowedAfterNumber or self.__get_current_char().isspace()):
                    raise LexerError("Invalid token", self.sourceHandler)

                return Token(type=TokenTypes.INTEGER_LITERAL, value=int(buffer), position=position)
            
        return None
    
    def __try_build_string_literal(self) -> Token:
        position = self.__get_position()

        if self.__get_current_char() == '\"':
            buffer = ""
            while self.__get_next_char() != '\"':
                if self.__get_current_char() == '\\':
                    buffer += self.__get_next_char()
                else:
                    buffer += self.__get_current_char()

                if len(buffer) > MAX_STRING_SIZE:
                    raise LexerError("Invalid token, string literal exceeded 2^16 chars.", self.sourceHandler)

            self.__get_next_char()        
            return Token(type=TokenTypes.STRING_LITERAL, value=buffer, position=position)

        return None

    def __try_build_single_char_symbol(self) -> Token:
        position = self.__get_position()

        char = self.__get_current_char()
        if char in self.symbolsTable.singleCharSymbolsDict:
            self.__get_next_char()
            return Token(type=self.symbolsTable.singleCharSymbolsDict[char], value=char, position=position)

        else:
            return None
    
    def __try_build_logic_operator(self, firstChar: str, position: tuple) -> Token:
        secondChar = self.__get_next_char()
        if firstChar == secondChar:
            symbol = firstChar + secondChar
            self.__get_next_char()
            return Token(type=self.symbolsTable.doubleCharSymbolsDict[symbol], value=symbol, position=position)    
        else:
            raise LexerError(f"Invalid token, expected {firstChar}, got {secondChar}", self.sourceHandler)

    def __try_build_comp_or_ret_operator(self, firstChar: str, position: tuple) -> Token:
        secondChar = self.__get_next_char()
        if firstChar != '-' and secondChar == '=':
            symbol = firstChar + secondChar
            self.__get_next_char()
            return Token(type=self.symbolsTable.doubleCharSymbolsDict[symbol], value=symbol, position=position)
        elif firstChar == '-' and secondChar == '>':
            symbol = firstChar + secondChar
            self.__get_next_char()
            return Token(type=self.symbolsTable.doubleCharSymbolsDict[symbol], value=symbol, position=position)
        #If double char symbol could not be matched return single char symbol
        else:
            return Token(type=self.symbolsTable.singleCharSymbolsDict[firstChar], value=firstChar, position=position)

    def __try_build_double_char_symbol(self) -> Token:
        position = self.__get_position()

        firstChar = self.__get_current_char()
        if firstChar in ['&', '|']:
            return self.__try_build_logic_operator(firstChar=firstChar, position=position)      
        elif firstChar in ['<', '>', '=', '!', '-']:
            return self.__try_build_comp_or_ret_operator(firstChar=firstChar, position=position)
        else:
            return None

    def __discrad_whitespaces(self) -> None:
        while self.__get_current_char().isspace():
            self.__get_next_char()

    def __discard_comment(self) -> None:
        while self.__get_current_char() == '#':
            while self.__get_next_char() != '\n':
                pass
            self.__get_next_char()

    def get_token(self, verbose: bool = False) -> Token:
        while self.__get_current_char().isspace() or self.__get_current_char() == '#':
            self.__discard_comment()
            self.__discrad_whitespaces()

        position = self.__get_position()

        for try_build_token in [self.__try_build_id, 
                                self.__try_build_number,
                                self.__try_build_string_literal,
                                self.__try_build_double_char_symbol,
                                self.__try_build_single_char_symbol]:
            if token := try_build_token():
                token.position = position
                self.currentToken = token
                if verbose:
                    print(token)

                return token

        #If cannot build token: 1) invalid input, 2) one char left and it was EOF
        if self.__get_current_char():
            raise LexerError("Uknown token", self.sourceHandler)  
        else:
            return Token(type=TokenTypes.EOF, value="EOF", position=position)    
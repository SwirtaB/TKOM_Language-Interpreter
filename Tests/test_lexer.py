import unittest
from HelperModules.sourcehandler import FileHandler, DirectInputHandler
from HelperModules.symbols import SymbolsTable, TokenTypes
from HelperModules.errorhandler import LexerError
from Lexer.lexer import Lexer, MAX_STRING_SIZE
from Lexer.token import Token


def build_lexer_direct(input: str) -> Lexer:
    symbolsTable = SymbolsTable()
    sourceHandler = DirectInputHandler(input)
    return Lexer(sourceHandler=sourceHandler, symbolsTable=symbolsTable)


def build_lexer_file(filePath: str) -> Lexer:
    symbolsTable = SymbolsTable()
    sourceHandler = FileHandler(filePath)
    return Lexer(sourceHandler=sourceHandler, symbolsTable=symbolsTable)


class LexerTestSuit(unittest.TestCase):
    def test_no_source_handler(self):
        self.assertRaises(LexerError, Lexer, None, None)

    def test_empty_file(self):
        path = "Tests/lexer/empty_file.txt"
        lexer = build_lexer_file(path)

        lexerToken = lexer.get_token()
        self.assertEqual(lexerToken.type, TokenTypes.EOF)
        self.assertEqual(lexerToken.value, "EOF")

    def test_tokens(self):
        path = "Tests/lexer/tokens.txt"
        lexer = build_lexer_file(path)
        expectedTokens = [
            Token(TokenTypes.INTEGER, "int"),
            Token(TokenTypes.FLOAT, "float"),
            Token(TokenTypes.FRACTION, "frc"),
            Token(TokenTypes.STRING, "string"),
            Token(TokenTypes.FUNCTION, "fn"),
            Token(TokenTypes.IF, "if"),
            Token(TokenTypes.ELSE, "else"),
            Token(TokenTypes.WHILE, "while"),
            Token(TokenTypes.RETURN, "return"),
            Token(TokenTypes.DOT, "."),
            Token(TokenTypes.COMMA, ","),
            Token(TokenTypes.NEGATION, "!"),
            Token(TokenTypes.ASSIGNMENT, "="),
            Token(TokenTypes.LESS, "<"),
            Token(TokenTypes.GREATER, ">"),
            Token(TokenTypes.PLUS, "+"),
            Token(TokenTypes.MINUS, "-"),
            Token(TokenTypes.MULTIPLY, "*"),
            Token(TokenTypes.DIVIDE, "/"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.OPEN_PARENTHESES, "("),
            Token(TokenTypes.CLOSE_PARENTHESES, ')'),
            Token(TokenTypes.OPEN_BRACE, '{'),
            Token(TokenTypes.CLOSE_BRACE, '}'),
            Token(TokenTypes.LESS_OR_EQUAL, "<="),
            Token(TokenTypes.GREATER_OR_EQUAL, ">="),
            Token(TokenTypes.EQUAL, "=="),
            Token(TokenTypes.NOT_EQUAL, "!="),
            Token(TokenTypes.RETURN_SIGN, "->"),
            Token(TokenTypes.AND, "&&"),
            Token(TokenTypes.OR, "||"),
            Token(TokenTypes.INTEGER_LITERAL, 0),
            Token(TokenTypes.INTEGER_LITERAL, 1),
            Token(TokenTypes.INTEGER_LITERAL, 10),
            Token(TokenTypes.INTEGER_LITERAL, 100),
            Token(TokenTypes.INTEGER_LITERAL, 1000),
            Token(TokenTypes.INTEGER_LITERAL, 54321),
            Token(TokenTypes.MINUS, '-'),
            Token(TokenTypes.INTEGER_LITERAL, 10),
            Token(TokenTypes.FLOAT_LITERAL, float(0.0)),
            Token(TokenTypes.FLOAT_LITERAL, float(0.1)),
            Token(TokenTypes.FLOAT_LITERAL, float(0.01)),
            Token(TokenTypes.FLOAT_LITERAL, float(0.001)),
            Token(TokenTypes.FLOAT_LITERAL, float(0.54321)),
            Token(TokenTypes.MINUS, '-'),
            Token(TokenTypes.FLOAT_LITERAL, float(15.24)),
            Token(TokenTypes.STRING_LITERAL, "abcd"),
            Token(TokenTypes.STRING_LITERAL, "path/to/file"),
            Token(TokenTypes.STRING_LITERAL, "\"test\""),
            Token(TokenTypes.IDENTIFIER, "main"),
            Token(TokenTypes.IDENTIFIER, "new_fun"),
            Token(TokenTypes.IDENTIFIER, "newVar"),
            Token(TokenTypes.IDENTIFIER, "_some_1_text_")
        ]

        for token in expectedTokens:
            lexerToken = lexer.get_token()
            self.assertEqual(lexerToken.type, token.type)
            self.assertEqual(lexerToken.value, token.value)

    def test_large_id(self):
        largeID = ""
        for i in range(MAX_STRING_SIZE + 1):
            largeID += "a"

        lexer = build_lexer_direct(largeID)
        self.assertRaises(LexerError, lexer.get_token)

    def test_large_string(self):
        largeString = '\"'
        for i in range(MAX_STRING_SIZE + 1):
            largeString += "a"
        largeString += '\"'

        lexer = build_lexer_direct(largeString)
        self.assertRaises(LexerError, lexer.get_token)

    def test_invalid_int(self):
        input = "12newVal"
        lexer = build_lexer_direct(input)

        self.assertRaises(LexerError, lexer.get_token)

    def test_invalid_float(self):
        input = "15."
        lexer = build_lexer_direct(input)
        self.assertRaises(LexerError, lexer.get_token)

        input = "15.2."
        lexer = build_lexer_direct(input)
        self.assertRaises(LexerError, lexer.get_token)

    def test_invalid_double_chars(self):
        input = "|&"
        lexer = build_lexer_direct(input)
        self.assertRaises(LexerError, lexer.get_token)

        input = "&-"
        lexer = build_lexer_direct(input)
        self.assertRaises(LexerError, lexer.get_token)

    def test_unknown_token(self):
        input = "@15_elem"
        lexer = build_lexer_direct(input)
        self.assertRaises(LexerError, lexer.get_token)

    def test_print_tokens(self):
        path = "Tests/grammar/fibonacci.txt"
        lexer = build_lexer_file(path)

        while lexer.get_token(verbose=True).type != TokenTypes.EOF:
            pass

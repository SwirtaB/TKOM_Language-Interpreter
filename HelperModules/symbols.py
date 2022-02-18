from enum import Enum, auto


class TokenTypes(Enum):
    FUNCTION = auto(),
    IF = auto(),
    ELSE = auto(),
    WHILE = auto(),
    RETURN = auto(),
    INTEGER = auto(),
    FLOAT = auto(),
    FRACTION = auto(),
    STRING = auto(),
    DOT = auto(),
    COMMA = auto(),
    NEGATION = auto(),
    ASSIGNMENT = auto(),
    LESS = auto(),
    LESS_OR_EQUAL = auto(),
    GREATER = auto(),
    GREATER_OR_EQUAL = auto(),
    EQUAL = auto(),
    NOT_EQUAL = auto(),
    AND = auto(),
    OR = auto(),
    PLUS = auto(),
    MINUS = auto(),
    MULTIPLY = auto(),
    DIVIDE = auto(),
    SEMICOLON = auto(),
    RETURN_SIGN = auto(),
    OPEN_PARENTHESES = auto(),
    CLOSE_PARENTHESES = auto(),
    OPEN_BRACE = auto(),
    CLOSE_BRACE = auto(),
    IDENTIFIER = auto(),
    INTEGER_LITERAL = auto(),
    FLOAT_LITERAL = auto(),
    STRING_LITERAL = auto(),
    EOF = auto()


class SymbolsTable:
    def __init__(self):
        self.keywordsDict = {
            "fn": TokenTypes.FUNCTION,
            "if": TokenTypes.IF,
            "else": TokenTypes.ELSE,
            "while": TokenTypes.WHILE,
            "return": TokenTypes.RETURN,
            "int": TokenTypes.INTEGER,
            "float": TokenTypes.FLOAT,
            "frc": TokenTypes.FRACTION,
            "string": TokenTypes.STRING
        }
        self.singleCharSymbolsDict = {
            ".": TokenTypes.DOT,
            ",": TokenTypes.COMMA,
            "!": TokenTypes.NEGATION,
            "=": TokenTypes.ASSIGNMENT,
            "<": TokenTypes.LESS,
            ">": TokenTypes.GREATER,
            "+": TokenTypes.PLUS,
            "-": TokenTypes.MINUS,
            "*": TokenTypes.MULTIPLY,
            "/": TokenTypes.DIVIDE,
            ";": TokenTypes.SEMICOLON,
            "(": TokenTypes.OPEN_PARENTHESES,
            ")": TokenTypes.CLOSE_PARENTHESES,
            "{": TokenTypes.OPEN_BRACE,
            "}": TokenTypes.CLOSE_BRACE
        }
        self.doubleCharSymbolsDict = {
            "<=": TokenTypes.LESS_OR_EQUAL,
            ">=": TokenTypes.GREATER_OR_EQUAL,
            "==": TokenTypes.EQUAL,
            "!=": TokenTypes.NOT_EQUAL,
            "->": TokenTypes.RETURN_SIGN,
            "&&": TokenTypes.AND,
            "||": TokenTypes.OR
        }

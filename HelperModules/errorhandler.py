from HelperModules.sourcehandler import FileHandler, DirectInputHandler
from Lexer.token import Token
from Parser.types import *
from typing import Union
import re


class IError(Exception):
    pass


class LexerError(IError):
    def __init__(
            self, message: str,
            sourceHandler: Union[FileHandler, DirectInputHandler]) -> None:
        if sourceHandler is None:
            super().__init__("Lexer error.\n" + message)
        else:
            lineNr, columnNr = sourceHandler.get_position()
            line = sourceHandler.get_line()

            errorPointer = re.sub(r"\S", ' ', line)
            errorPointer = errorPointer[:(columnNr -
                                          1)] + '^' + errorPointer[columnNr:]

            self.message = f"Lexer error.\n" + f"Where: line:{lineNr}, column:{columnNr}\n" + f"{line}\n{errorPointer}\n" + f"What: {message}\n"
            super().__init__(self.message)


class ParserError(IError):
    def __init__(self, message: str, currentToken: Token = None) -> None:
        if currentToken is None:
            super().__init__("Parser error.\n" + message)
        else:
            lineNr, columnNr = currentToken.position
            self.message = f"Parser error.\n" + f"Where: line:{lineNr}, column:{columnNr}\n" + f"What: {message}\n" + f"Got {currentToken}.\n"
            super().__init__(self.message)


class InterpreterError(IError):
    def __init__(self, message: str, currentInstruction: str = None) -> None:
        self.message = message
        if currentInstruction is None:
            super().__init__("Interpreter error.\n" + self.message)
        else:
            self.message = f"On instruction: {currentInstruction}\n" + f"What: {message}\n"
            super().__init__(self.message)


class InterpreterRuntimeError(IError):
    def __init__(self, message: str, currentFunction: str) -> None:
        self.message = f"Interpreter error in function: {currentFunction}.\n" + f"What: {message}\n"
        super().__init__(self.message)

from HelperModules.sourcehandler import FileHandler, DirectInputHandler
from HelperModules.errorhandler import *
from HelperModules.symbols import SymbolsTable
from Lexer.lexer import Lexer
from Parser.parser import Parser
from Interpreter.interpreter import Interpreter

import argparse
import pathlib


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Built-in fractions - interpreted language")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t",
                       "--text",
                       help="source code as plain text",
                       type=str)
    group.add_argument("-f",
                       "--file",
                       help="path to file with code",
                       type=pathlib.Path)

    return parser.parse_args()


def run() -> None:
    args = get_arguments()
    try:
        if args.text is not None:
            sourceHandler = DirectInputHandler(args.text)
        elif args.file is not None:
            sourceHandler = FileHandler(str(args.file))
        else:
            print("Invalid arguments.")
            print("Use -h for more information about usage.")
            return
    except OSError:
        print("File not found. Invalid file name.")
        return

    try:
        lexer = Lexer(sourceHandler=sourceHandler, symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        interpreter = Interpreter(parser)
        interpreter.interpret()

    except IError as error:
        print(error)


if __name__ == "__main__":
    run()
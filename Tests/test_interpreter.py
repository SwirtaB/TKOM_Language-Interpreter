import unittest
from HelperModules.symbols import SymbolsTable
from HelperModules.sourcehandler import DirectInputHandler
from HelperModules.errorhandler import *
from Lexer.lexer import Lexer
from Parser.parser import Parser
from Interpreter.interpreter import Interpreter


def build_interpreter(sourceCode: str) -> Interpreter:
    lexer = Lexer(sourceHandler=DirectInputHandler(sourceCode),
                  symbolsTable=SymbolsTable())
    parser = Parser(lexer=lexer)

    return Interpreter(parser)


class InterpreterPositiveTestSuite(unittest.TestCase):
    def test_simple_return(self):
        sourceCode = "fn main() -> int return 1;"
        interpreter = build_interpreter(sourceCode)
        result = interpreter.interpret(returnResult=True)
        self.assertEqual(result, 1)

    def test_simple_return_expression(self):
        sourceCode = "fn main() -> int return 1 + 2 + 3;"
        interpreter = build_interpreter(sourceCode)
        result = interpreter.interpret(returnResult=True)
        self.assertEqual(result, 6)

    def test_simple_main(self):
        sourceCode = "fn main() -> int {" + "int n = 1 + 2;" + "return n + 3;}"
        interpreter = build_interpreter(sourceCode)
        result = interpreter.interpret(returnResult=True)
        self.assertEqual(result, 6)

    def test_simple_expression(self):
        sourceCode = "fn main() -> int {" + "int n = 1 + 2 * 3;" + "return 4 + n * 5;}"
        interpreter = build_interpreter(sourceCode)
        result = interpreter.interpret(returnResult=True)
        self.assertEqual(result, 39)

    def test_subexpression_negation(self):
        sourceCode = "fn main() -> int {" + "int n = 1 + 2 * 3;" + "return -n;}"
        interpreter = build_interpreter(sourceCode)
        result = interpreter.interpret(returnResult=True)
        self.assertEqual(result, -7)

    def test_simple_assignment(self):
        sourceCode = "fn main() -> int {" + "int n = 1;" + "n = 1 + 2;" + "return n;}"
        interpreter = build_interpreter(sourceCode)
        result = interpreter.interpret(returnResult=True)
        self.assertEqual(result, 3)

    def test_simple_if_statement(self):
        sourceCode = "fn main() -> int {" + "int n = 1;" + "if (n == 1) n = 0;" + "return n;}"
        interpreter = build_interpreter(sourceCode)
        result = interpreter.interpret(returnResult=True)
        self.assertEqual(result, 0)

    def test_simple_while_statement(self):
        sourceCode = "fn main() -> int {" + "int n = 1;" + "while (n != 100) n = n + 1;" + "return n;}"
        interpreter = build_interpreter(sourceCode)
        result = interpreter.interpret(returnResult=True)
        self.assertEqual(result, 100)

    def test_simple_function(self):
        sourceCode = ("fn add(int a, int b) -> int return a + b;"
                      "fn main() -> int {"
                      "int a = 1;"
                      "int b = 2;"
                      "int c = add(a,b);"
                      "return c;}")
        interpreter = build_interpreter(sourceCode)
        result = interpreter.interpret(returnResult=True)
        self.assertEqual(result, 3)

    def test_simple_program(self):
        sourceCode = ("int a = 1;"
                      "fn add(int x, int y) -> int return x + y;"
                      "fn main() -> int {"
                      "int b = 2;"
                      "int c = add(2, a + b);"
                      "return c;}")
        interpreter = build_interpreter(sourceCode)
        result = interpreter.interpret(returnResult=True)
        self.assertEqual(result, 5)

    def test_else_if(self):
        sourceCode = ("fn main() -> int {"
                      "int i = 0;"
                      "if(i == 1) return i;"
                      "else return 2;"
                      "}")
        interpreter = build_interpreter(sourceCode)
        result = interpreter.interpret(returnResult=True)
        self.assertEqual(result, 2)

    def test_recursion(self):
        sourceCode = ("fn fibonacci(int n) -> int {"
                      "if (n <= 1) {"
                      "return n;"
                      "}"
                      "return fibonacci(n-1) + fibonacci(n-2);"
                      "}"
                      "fn main() -> int {"
                      "int n = 9;"
                      "return fibonacci(n);"
                      "}")
        interpreter = build_interpreter(sourceCode)
        result = interpreter.interpret(returnResult=True)
        self.assertEqual(result, 34)


class InterpreterTestStdLib(unittest.TestCase):
    def test_print(self):
        sourceCode = ("fn main() -> int {"
                      "string s = \"Hello world!\";"
                      "print(s);"
                      "return 0;"
                      "}")
        interpreter = build_interpreter(sourceCode)
        interpreter.interpret()

    def test_frc(self):
        sourceCode = ("fn main() -> int {"
                      "frc frac_1 = frc(1,2);"
                      "return 0;"
                      "}")
        interpreter = build_interpreter(sourceCode)
        interpreter.interpret()

    def test_frc_to_string(self):
        sourceCode = ("fn main() -> int {"
                      "frc frac = frc(1,2);"
                      "print(frc_to_string(frac));"
                      "return 0;"
                      "}")
        interpreter = build_interpreter(sourceCode)
        interpreter.interpret()

    def test_float_to_string(self):
        sourceCode = ("fn main() -> int {"
                      "float f = 0.12345;"
                      "print(float_to_string(f));"
                      "return 0;"
                      "}")
        interpreter = build_interpreter(sourceCode)
        interpreter.interpret()

    def test_int_to_string(self):
        sourceCode = ("fn main() -> int {"
                      "int i = 1;"
                      "print(int_to_string(i));"
                      "return 0;"
                      "}")
        interpreter = build_interpreter(sourceCode)
        interpreter.interpret()

    def test_int_to_frc(self):
        sourceCode = ("fn main() -> int {"
                      "int i = 1;"
                      "print(frc_to_string(int_to_frc(i)));"
                      "return 0;"
                      "}")
        interpreter = build_interpreter(sourceCode)
        interpreter.interpret()

    def test_int_to_float(self):
        sourceCode = ("fn main() -> int {"
                      "int i = 1;"
                      "print(float_to_string(int_to_float(i)));"
                      "return 0;"
                      "}")
        interpreter = build_interpreter(sourceCode)
        interpreter.interpret()

    def test_frc_to_float(self):
        sourceCode = ("fn main() -> int {"
                      "frc frac = frc(1,3);"
                      "print(float_to_string(frc_to_float(frac)));"
                      "return 0;"
                      "}")
        interpreter = build_interpreter(sourceCode)
        interpreter.interpret(returnResult=True)

    def test_float_to_int(self):
        sourceCode = ("fn main() -> int {"
                      "float f = 1.0;"
                      "print(int_to_string(float_to_int(f)));"
                      "return 0;"
                      "}")
        interpreter = build_interpreter(sourceCode)
        interpreter.interpret(returnResult=True)

    def test_frc_to_int(self):
        sourceCode = ("fn main() -> int {"
                      "frc frac = frc(1,3);"
                      "print(int_to_string(frc_to_int(frac)));"
                      "return 0;"
                      "}")
        interpreter = build_interpreter(sourceCode)
        interpreter.interpret()


class InterpreterNegativeTestSuite(unittest.TestCase):
    def test_empty_input(self):
        sourceCode = ""
        interpreter = build_interpreter(sourceCode)
        interpreter.interpret()

    def test_no_main(self):
        sourceCode = ("fn fun() return 0;")
        interpreter = build_interpreter(sourceCode)
        self.assertRaises(InterpreterError, interpreter.interpret)

    def test_undefined_functions(self):
        sourceCode = ("fn main() print(int_to_string(add(1, 2)));")
        interpreter = build_interpreter(sourceCode)
        self.assertRaises(InterpreterRuntimeError, interpreter.interpret)

    def test_undefined_variable(self):
        sourceCode = ("fn main() undefinedStr = \"test\";")
        interpreter = build_interpreter(sourceCode)
        self.assertRaises(InterpreterRuntimeError, interpreter.interpret)

    def test_wrong_type_define(self):
        sourceCode = ("fn main() int i = 0.0;")
        interpreter = build_interpreter(sourceCode)
        self.assertRaises(InterpreterRuntimeError, interpreter.interpret)

    def test_wrong_type_assigne(self):
        sourceCode = ("fn main() {" "int i = 1;" "i = 0.0;" "}")
        interpreter = build_interpreter(sourceCode)
        self.assertRaises(InterpreterRuntimeError, interpreter.interpret)

    def test_invalid_return(self):
        sourceCode = ("fn main() -> int{"
                      "frc frac = frc(1,3);"
                      "print(int_to_string(frc_to_int(frac)));"
                      "return 0.0;"
                      "}")
        interpreter = build_interpreter(sourceCode)
        self.assertRaises(InterpreterRuntimeError, interpreter.interpret)

    def test_invalid_argument_type(self):
        sourceCode = ("fn main() -> int{"
                      "frc frac = frc(1,3);"
                      "print(frc_to_int(frac));"
                      "return 0;"
                      "}")
        interpreter = build_interpreter(sourceCode)
        self.assertRaises(InterpreterRuntimeError, interpreter.interpret)

    def test_variable_redefinition(self):
        sourceCode = ("fn main() {" "int i;" "float i = 0.0;" "}")
        interpreter = build_interpreter(sourceCode)
        self.assertRaises(InterpreterRuntimeError, interpreter.interpret)

    def test_invalid_expression(self):
        sourceCode = ("fn main() -> int return 1 + 2 + a;")
        interpreter = build_interpreter(sourceCode)
        self.assertRaises(InterpreterRuntimeError, interpreter.interpret)

    def test_invalid_subexpression(self):
        sourceCode = ("fn main() -> int return a * b;")
        interpreter = build_interpreter(sourceCode)
        self.assertRaises(InterpreterRuntimeError, interpreter.interpret)

    def test_invalid_operation_1(self):
        sourceCode = ("fn main() print(\"test\" - \"test\");")
        interpreter = build_interpreter(sourceCode)
        self.assertRaises(InterpreterRuntimeError, interpreter.interpret)

    def test_invalid_operation_2(self):
        sourceCode = ("fn main() print(\"test\" * 3);")
        interpreter = build_interpreter(sourceCode)
        self.assertRaises(InterpreterRuntimeError, interpreter.interpret)

    def test_invalid_operands(self):
        sourceCode = ("fn main() -> int{"
                      "frc frac = frc(1,3);"
                      "return 1 * frac;"
                      "}")
        interpreter = build_interpreter(sourceCode)
        self.assertRaises(InterpreterRuntimeError, interpreter.interpret)

    def test_multiple_functionsDef(self):
        sourceCode = ("fn main() {}" "fn main() {}")
        interpreter = build_interpreter(sourceCode)
        self.assertRaises(InterpreterError, interpreter.interpret)

    def test_multiple_global_var_definitions(self):
        sourceCode = ("int i = 0;" "int i = 0;" "fn main() {}")
        interpreter = build_interpreter(sourceCode)
        self.assertRaises(InterpreterError, interpreter.interpret)
import unittest
from HelperModules.symbols import SymbolsTable, TokenTypes
from HelperModules.sourcehandler import FileHandler, DirectInputHandler
from HelperModules.errorhandler import ParserError
from Lexer.lexer import Lexer
from Lexer.token import Token
from Parser.parser import Parser
from Parser.types import *


class ParserUnitTestSuitPovitive(unittest.TestCase):
    #Positive tests
    def test_simple_return_statement(self):
        lexer = Lexer(sourceHandler=DirectInputHandler("return 5;"),
                      symbolsTable=SymbolsTable())

        parser = Parser(lexer=lexer)
        parserObject = parser._Parser__try_parse_return_statement()
        self.assertEqual(parserObject, ReturnStatement(5))

    def test_simple_assignemt(self):
        lexer = Lexer(sourceHandler=DirectInputHandler("sampleVar = 0;"),
                      symbolsTable=SymbolsTable())

        parser = Parser(lexer=lexer)
        parserObject = parser._Parser__try_parse_assign_or_function_call()
        self.assertEqual(parserObject, AssignStatement(Variable("sampleVar"),
                                                       0))

    def test_simple_define_statement(self):
        lexerOne = Lexer(sourceHandler=DirectInputHandler("frc testFrc;"),
                         symbolsTable=SymbolsTable())
        lexerTwo = Lexer(
            sourceHandler=DirectInputHandler("float testFloat = 0.15;"),
            symbolsTable=SymbolsTable())

        parserOne = Parser(lexer=lexerOne)
        parserTwo = Parser(lexer=lexerTwo)
        parserObjectOne = parserOne._Parser__try_parse_define_statement()
        parserObjectTwo = parserTwo._Parser__try_parse_define_statement()
        self.assertEqual(parserObjectOne, DefineStatement("frc", "testFrc"))
        self.assertEqual(parserObjectTwo,
                         DefineStatement("float", "testFloat", float(0.15)))

    def test_no_parameters(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(""),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        parserObject = parser._Parser__try_parse_parameters()
        self.assertFalse(parserObject)

    def test_parameters(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "int i, float f, frc frac, string s"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        parserObject = parser._Parser__try_parse_parameters()
        self.assertEqual(parserObject, [
            Parameter("int", "i"),
            Parameter("float", "f"),
            Parameter("frc", "frac"),
            Parameter("string", "s")
        ])

    def test_no_arguments(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(""),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        parserObject = parser._Parser__try_parse_arguments()
        self.assertFalse(parserObject)

    def test_simple_arguments(self):
        lexer = Lexer(
            sourceHandler=DirectInputHandler("0, 0.01, \"stringLiteral\""),
            symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        parserObject = parser._Parser__try_parse_arguments()
        self.assertEqual(parserObject, [int(0), float(0.01), "stringLiteral"])

    def test_factor(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "testID 0 0.01 \"stringLiteral\" test_fun_call() (testExpr)"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObjects = [
            Variable("testID"),
            int(0),
            float(0.01),
            str("stringLiteral"),
            FunctionCall("test_fun_call", list()),
            Variable("testExpr")
        ]
        for i in range(len(expectedObjects)):
            parserObject = parser._Parser__try_parse_factor()
            self.assertEqual(parserObject, expectedObjects[i])

    def test_simple_subexpression(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "-0.01 1 * 15 -fun_call() 1*2*3*4 "),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObjects = [
            SubExpression(leftFactor=0.01, isNegated=True),
            SubExpression(leftFactor=1, operator='*', rightFactor=15),
            SubExpression(leftFactor=FunctionCall("fun_call", list()),
                          isNegated=True),
            SubExpression(leftFactor=SubExpression(leftFactor=SubExpression(
                leftFactor=1, operator='*', rightFactor=2),
                                                   operator='*',
                                                   rightFactor=3),
                          operator='*',
                          rightFactor=4)
        ]
        for i in range(len(expectedObjects)):
            parserObject = parser._Parser__try_parse_subexpression()
            self.assertEqual(parserObject, expectedObjects[i])

    def test_simple_expression(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "-0.01 1 * 15 fun_call() 1+2-3 test_fun() + fun_call(2) + 1*2 "),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObjects = [
            SubExpression(leftFactor=0.01, isNegated=True),
            SubExpression(leftFactor=1, operator='*', rightFactor=15),
            FunctionCall("fun_call", list()),
            Expression(leftExpression=Expression(leftExpression=1,
                                                 operator='+',
                                                 rightExpression=2),
                       operator='-',
                       rightExpression=3),
            Expression(leftExpression=Expression(
                leftExpression=FunctionCall("test_fun", list()),
                operator='+',
                rightExpression=FunctionCall("fun_call", [2])),
                       operator='+',
                       rightExpression=SubExpression(leftFactor=1,
                                                     operator='*',
                                                     rightFactor=2))
        ]
        for i in range(len(expectedObjects)):
            parserObject = parser._Parser__try_parse_expression()
            self.assertEqual(parserObject, expectedObjects[i])

    def test_expression(self):
        lexer = Lexer(
            sourceHandler=DirectInputHandler("5*(fun(n - 1) + fun(n - 2))"),
            symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)

        expectedObject = SubExpression(
            leftFactor=5,
            operator='*',
            rightFactor=Expression(
                leftExpression=FunctionCall(
                    identifier="fun",
                    arguments=[
                        Expression(leftExpression=Variable(identifier='n'),
                                   operator='-',
                                   rightExpression=1)
                    ]),
                operator='+',
                rightExpression=FunctionCall(
                    identifier="fun",
                    arguments=[
                        Expression(leftExpression=Variable(identifier='n'),
                                   operator='-',
                                   rightExpression=2)
                    ])))
        parserObject = parser._Parser__try_parse_expression()
        self.assertEqual(parserObject.leftFactor, expectedObject.leftFactor)
        self.assertEqual(parserObject.rightFactor.leftExpression,
                         expectedObject.rightFactor.leftExpression)
        self.assertEqual(parserObject.rightFactor.operator,
                         expectedObject.rightFactor.operator)
        self.assertEqual(parserObject.rightFactor.rightExpression,
                         expectedObject.rightFactor.rightExpression)

    def test_simple_subcondition(self):
        lexer = Lexer(sourceHandler=DirectInputHandler("1 - ret_one_fun()"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = SubCondition(
            value=Expression(1, '-', FunctionCall("ret_one_fun", list())))
        parserObject = parser._Parser__try_parse_subcondition()
        self.assertEqual(parserObject, expectedObject)

    def test_simple_and_condition(self):
        lexer = Lexer(sourceHandler=DirectInputHandler("1 && ret_one_fun()"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = Condition(
            SubCondition(value=1), "&&",
            SubCondition(value=FunctionCall(identifier="ret_one_fun",
                                            arguments=list())))
        parserObject = parser._Parser__try_parse_condition()
        self.assertEqual(parserObject, expectedObject)

    def test_simple_operator_condition(self):
        lexer = Lexer(sourceHandler=DirectInputHandler("1 < 5 "),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = Condition(SubCondition(value=1), "<",
                                   SubCondition(value=5))
        parserObject = parser._Parser__try_parse_condition()
        self.assertEqual(parserObject, expectedObject)

    def test_parentheses_condition(self):
        lexer = Lexer(sourceHandler=DirectInputHandler("(1 < 5)"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = Condition(SubCondition(value=1), "<",
                                   SubCondition(value=5))
        parserObject = parser._Parser__try_parse_parentheses_condition()
        self.assertEqual(parserObject, expectedObject)

    def test_condition(self):
        lexer = Lexer(
            sourceHandler=DirectInputHandler("fun_call() && (1 < 5)"),
            symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = Condition(
            SubCondition(
                value=FunctionCall(identifier="fun_call", arguments=list())),
            "&&",
            SubCondition(value=Condition(SubCondition(
                value=1), "<", SubCondition(value=5))))
        parserObject = parser._Parser__try_parse_condition()
        self.assertEqual(parserObject, expectedObject)

    def test_one_line_statement_define(self):
        lexer = Lexer(sourceHandler=DirectInputHandler("int i = 0;"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = DefineStatement("int", 'i', 0)
        parserObject = parser._Parser__try_parse_statement()
        self.assertEqual(parserObject, expectedObject)

    def test_one_line_statement_assign(self):
        lexer = Lexer(sourceHandler=DirectInputHandler("i = 0;"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = AssignStatement(Variable('i'), 0)
        parserObject = parser._Parser__try_parse_statement()
        self.assertEqual(parserObject, expectedObject)

    def test_one_line_statement_function_call(self):
        lexer = Lexer(sourceHandler=DirectInputHandler("fun_call(0, 0, 7);"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = FunctionCall("fun_call", [0, 0, 7])
        parserObject = parser._Parser__try_parse_statement()
        self.assertEqual(parserObject, expectedObject)

    def test_one_line_statement_return(self):
        lexer = Lexer(
            sourceHandler=DirectInputHandler("return fun_call(0, 0, 7) + 1;"),
            symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = ReturnStatement(
            Expression(FunctionCall("fun_call", [0, 0, 7]), '+', 1))
        parserObject = parser._Parser__try_parse_statement()
        self.assertEqual(parserObject, expectedObject)

    def test_statement_block(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "{int n = 0; m = 0; return fun_call(n, m, 7) + 1;}"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = StatementBlock(statements=[
            DefineStatement(type='int', identifier='n', expression=0),
            AssignStatement(identifier=Variable('m'), expression=0),
            ReturnStatement(expression=Expression(leftExpression=FunctionCall(
                "fun_call", [Variable('n'), Variable('m'), 7]),
                                                  operator='+',
                                                  rightExpression=1))
        ])
        parserObject = parser._Parser__try_parse_statement()
        self.assertEqual(parserObject, expectedObject)

    def test_one_line_if_statement(self):
        lexer = Lexer(sourceHandler=DirectInputHandler("if (a < b) return a;"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = IfStatement(
            condition=Condition(
                leftCondition=SubCondition(value=Variable('a')),
                operator='<',
                rightCondition=SubCondition(value=Variable('b'))),
            statement=ReturnStatement(expression=Variable('a')))

        parserObject = parser._Parser__try_parse_statement()
        self.assertEqual(parserObject, expectedObject)

    def test_if_else_statement(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "if (a < b) return a; else return b;"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = IfStatement(
            condition=Condition(
                leftCondition=SubCondition(value=Variable('a')),
                operator='<',
                rightCondition=SubCondition(value=Variable('b'))),
            statement=ReturnStatement(expression=Variable('a')),
            elseStatement=ReturnStatement(expression=Variable('b')))

        parserObject = parser._Parser__try_parse_statement()
        self.assertEqual(parserObject, expectedObject)

    def test_if_statement(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "if (a < b){ a = a + 1; return a;}"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = IfStatement(
            condition=Condition(
                leftCondition=SubCondition(value=Variable('a')),
                operator='<',
                rightCondition=SubCondition(value=Variable('b'))),
            statement=StatementBlock([
                AssignStatement(identifier=Variable('a'),
                                expression=Expression(
                                    leftExpression=Variable('a'),
                                    operator='+',
                                    rightExpression=1)),
                ReturnStatement(expression=Variable('a'))
            ]))

        parserObject = parser._Parser__try_parse_statement()
        self.assertEqual(parserObject, expectedObject)

    def test_else_if_statement(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "if (a < b){ a = a + 1; return a;} else if(!b){ return b; }"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = IfStatement(
            condition=Condition(
                leftCondition=SubCondition(value=Variable('a')),
                operator='<',
                rightCondition=SubCondition(value=Variable('b'))),
            statement=StatementBlock([
                AssignStatement(identifier=Variable('a'),
                                expression=Expression(
                                    leftExpression=Variable('a'),
                                    operator='+',
                                    rightExpression=1)),
                ReturnStatement(expression=Variable('a'))
            ]),
            elseStatement=IfStatement(
                condition=SubCondition(value=Variable('b'), isNegated=True),
                statement=StatementBlock(
                    [ReturnStatement(expression=Variable('b'))])))

        parserObject = parser._Parser__try_parse_statement()
        self.assertEqual(parserObject, expectedObject)

    def test_while_statement(self):
        lexer = Lexer(
            sourceHandler=DirectInputHandler("while(a < b){ a = a + 1;}"),
            symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = WhileStatement(
            condition=Condition(
                leftCondition=SubCondition(value=Variable('a')),
                operator='<',
                rightCondition=SubCondition(value=Variable('b'))),
            statement=StatementBlock([
                AssignStatement(identifier=Variable('a'),
                                expression=Expression(
                                    leftExpression=Variable('a'),
                                    operator='+',
                                    rightExpression=1))
            ]))

        parserObject = parser._Parser__try_parse_statement()
        self.assertEqual(parserObject, expectedObject)

    def test_one_line_function_definition(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "fn fun(int i, frc f) print(i + int(f));"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = FunctionDef(
            identifier='fun',
            parameters=[Parameter('int', 'i'),
                        Parameter('frc', 'f')],
            statement=FunctionCall(identifier='print',
                                   arguments=[
                                       Expression(
                                           leftExpression=Variable('i'),
                                           operator='+',
                                           rightExpression=FunctionCall(
                                               identifier='int',
                                               arguments=[Variable('f')]))
                                   ]))

        parserObject = parser._Parser__try_parse_function_definition()
        self.assertEqual(parserObject.identifier, expectedObject.identifier)
        self.assertEqual(parserObject.parameters, expectedObject.parameters)
        self.assertEqual(parserObject.statement, expectedObject.statement)
        self.assertEqual(parserObject.returnType, expectedObject.returnType)

    def test_function_definition(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "fn fun(int i, frc f) -> frc { return frc(i) + f; }"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = FunctionDef(
            identifier='fun',
            parameters=[Parameter('int', 'i'),
                        Parameter('frc', 'f')],
            statement=StatementBlock([
                ReturnStatement(
                    expression=Expression(leftExpression=FunctionCall(
                        identifier='frc', arguments=[Variable('i')]),
                                          operator='+',
                                          rightExpression=Variable('f')))
            ]),
            returnType='frc')

        parserObject = parser._Parser__try_parse_function_definition()
        self.assertEqual(parserObject.identifier, expectedObject.identifier)
        self.assertEqual(parserObject.parameters, expectedObject.parameters)
        self.assertEqual(parserObject.statement, expectedObject.statement)
        self.assertEqual(parserObject.returnType, expectedObject.returnType)

    def test_program(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "string globStr = \"global string\";" +
            "fn fun(int i, frc f) -> frc { return frc(i) + f;}"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        expectedObject = Program(functionDefList=[
            FunctionDef(
                identifier='fun',
                parameters=[Parameter('int', 'i'),
                            Parameter('frc', 'f')],
                statement=StatementBlock([
                    ReturnStatement(
                        expression=Expression(leftExpression=FunctionCall(
                            identifier='frc', arguments=[Variable('i')]),
                                              operator='+',
                                              rightExpression=Variable('f')))
                ]),
                returnType='frc')
        ],
                                 defineStatementList=[
                                     DefineStatement('string', 'globStr',
                                                     "global string")
                                 ])

        parserObject = parser.try_parse_program()
        self.assertEqual(parserObject.defineStatementList,
                         expectedObject.defineStatementList)
        self.assertEqual(len(parserObject.functionDefList),
                         len(expectedObject.functionDefList))
        self.assertEqual(parserObject.functionDefList[0].identifier,
                         expectedObject.functionDefList[0].identifier)
        self.assertEqual(parserObject.functionDefList[0].parameters,
                         expectedObject.functionDefList[0].parameters)
        self.assertEqual(parserObject.functionDefList[0].statement,
                         expectedObject.functionDefList[0].statement)
        self.assertEqual(parserObject.functionDefList[0].returnType,
                         expectedObject.functionDefList[0].returnType)


class ParserUnitTestSuitNegative(unittest.TestCase):
    def test_closing_brace(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "fn fun(int i, frc f -> frc { return frc(i) + f;}"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        self.assertRaises(ParserError, parser.try_parse_program)

    def test_closing_parentheses(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "string globStr = \"global string\";" +
            "fn fun(int i, frc f) -> frc { return frc(i) + f;"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        self.assertRaises(ParserError, parser.try_parse_program)

    def test_missing_semicolon(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "string globStr = \"global string\";" +
            "fn fun(int i, frc f) -> frc { return frc(i) + f}"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        self.assertRaises(ParserError, parser.try_parse_program)

    def test_incorrect_type(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "sting globStr = \"global string\";" +
            "fn fun(int i, frc f) -> frc { return frc(i) + f;}"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        self.assertRaises(ParserError, parser.try_parse_program)

    def test_missing_identifier(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "string = \"global string\";" +
            "fn fun(int i, frc f) -> frc { return frc(i) + f;}"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        self.assertRaises(ParserError, parser.try_parse_program)

    def test_incorrect_parameters(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "string globStr = \"global string\";" +
            "fn fun(int i frc f) -> frc { return frc(i) + f;}"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        self.assertRaises(ParserError, parser.try_parse_program)

    def test_incorrect_arguments(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "string globStr = \"global string\";" +
            "fn fun(int i, frc f) -> frc { return frc(i,) + f;}"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        self.assertRaises(ParserError, parser.try_parse_program)

    def test_missing_right_side_expression(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "string globStr = \"global string\";" +
            "fn fun(int i, frc f) -> frc { return frc(i) + ;}"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        self.assertRaises(ParserError, parser.try_parse_program)

    def test_missing_right_side_subexpression(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "string globStr = \"global string\";" +
            "fn fun(int i, frc f) -> frc { return frc(i) + f*;}"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        self.assertRaises(ParserError, parser.try_parse_program)

    def test_missing_right_side_condition(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "fn fun(int i, frc f) -> frc { if(i < ) return frc(i) + f;}"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        self.assertRaises(ParserError, parser.try_parse_program)

    def test_missing_return_value(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "fn fun(int i, frc f) -> { if(i < ) return frc(i) + f;}"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        self.assertRaises(ParserError, parser.try_parse_program)

    def test_sample(self):
        lexer = Lexer(sourceHandler=DirectInputHandler(
            "fn main(int i) {}; fn main() -> int return 1;"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        self.assertRaises(ParserError, parser.try_parse_program)


class ParserAcceptanceTestsSuit(unittest.TestCase):
    def test_fibonacci(self):
        lexer = Lexer(sourceHandler=FileHandler("Tests/grammar/fibonacci.txt"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        parserObject = parser.try_parse_program()
        self.assertIsNotNone(parserObject)

    def test_casting(self):
        lexer = Lexer(sourceHandler=FileHandler("Tests/grammar/casting.txt"),
                      symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        parserObject = parser.try_parse_program()
        self.assertIsNotNone(parserObject)

    def test_conditions(self):
        lexer = Lexer(
            sourceHandler=FileHandler("Tests/grammar/conditions.txt"),
            symbolsTable=SymbolsTable())
        parser = Parser(lexer=lexer)
        parserObject = parser.try_parse_program()
        self.assertIsNotNone(parserObject)
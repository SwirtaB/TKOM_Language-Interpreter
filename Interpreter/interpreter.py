import math

from Parser.parser import Parser
from Parser.types import *

from HelperModules.errorhandler import InterpreterError, InterpreterRuntimeError
from Interpreter.visitor import Visitor
import Interpreter.stdlib as std

from collections import namedtuple

Context = namedtuple("Context", ["variables", "functions", "specials"])
VariableInfo = namedtuple("VariableInfo", ["type", "value"])

EVAL_RETURN_EXP = "__eval_return_exp__"


class Interpreter(Visitor):
    def __init__(self, parser: Parser) -> None:
        if parser is None:
            raise InterpreterError("Parser module not provided.")

        self.__parser: Parser = parser
        self.__contextList: list[Context] = []
        self.__results = []
        self.__return = False

    def interpret(self, returnResult: bool = False):
        program = self.__parser.try_parse_program()
        if program is not None:
            program.accept(self)
        else:
            print("Parsed data are empty. No program to interpret.")

        if returnResult:
            return self.__get_result()

    def evaluate_program(self, element: Program):
        self.__build_global_context(element)
        mainFunction = self.__get_local_context().functions['main']
        try:
            mainFunction.accept(self)

            if EVAL_RETURN_EXP in self.__get_local_context().specials:
                if self.__get_local_context(
                ).specials[EVAL_RETURN_EXP] is not None:
                    result = self.__get_result()
                    self.__check_type(mainFunction.returnType, result)

                    print(f"Program finished with result: {result}")
                    self.__add_result(result)

            self.__pop_context()

        except InterpreterError as error:
            raise InterpreterRuntimeError(error.message, "main")

    def evaluate_function_definition(self, element: FunctionDef):
        try:
            element.statement.accept(self)
        except InterpreterError as error:
            raise InterpreterRuntimeError(error.message, element.identifier)

    def evaluate_function_call(self, element: FunctionCall):
        if element.identifier in self.__get_global_context().functions:
            function = self.__get_global_context().functions[
                element.identifier]

            self.__build_new_context(function, element)

            if element.identifier in std.functions:
                argumentsList = []
                for parameter in function.parameters:
                    argumentsList.append(self.__get_local_context().variables[
                        parameter.identifier].value)
                if (result := std.functions[element.identifier](argumentsList)
                    ) is not None:
                    self.__results.append(result)
            else:
                function.accept(self)

            self.__return = False
            self.__pop_context()
        else:
            raise InterpreterError(
                f"Function {element.identifier} is undefined.", str(element))

    def evaluate_statement_block(self, element: StatementBlock):
        for statement in element.statements:
            statement.accept(self)
            if self.__return:
                return

    def evaluate_return_statement(self, element: ReturnStatement):
        try:
            if EVAL_RETURN_EXP in self.__get_local_context().specials:
                self.__evaluate_expression(element.expression)
                # Gets function info from current context and
                # checks if actual expression type matches declared return type.
                # If not, exception is thrown.
                if self.__get_local_context(
                ).specials[EVAL_RETURN_EXP] is not None:
                    self.__check_type(
                        self.__get_local_context().specials[EVAL_RETURN_EXP],
                        self.__peek_result())

            self.__return = True
        except InterpreterError as error:
            raise InterpreterError(error.message, str(element))

    def evaluate_assigne_statement(self, element: AssignStatement):
        key = element.identifier.identifier
        context = self.__get_local_context()
        if key not in context.variables:
            context = self.__get_global_context()
            if key not in context.variables:
                raise InterpreterError(f"Variable {key} was not defined",
                                       str(element))

        self.__evaluate_expression(element.expression)
        value = self.__get_result()

        variableInfo = context.variables[key]

        #check if proper type is being assigne
        try:
            self.__check_type(variableInfo.type, value)
        except InterpreterError as error:
            raise InterpreterError(error.message, str(element))

        context.variables[key] = VariableInfo(variableInfo.type, value)

    def evaluate_define_statement(self, element: DefineStatement):
        key = element.identifier
        if (key in self.__get_local_context().variables) or (
                key in self.__get_global_context().variables):
            raise InterpreterError(f"Variable redefinition: {key}.",
                                   str(element))

        if element.expression is None:
            value = self.__defaultValue(element.type)
        else:
            self.__evaluate_expression(element.expression)
            value = self.__get_result()

        #check if types match
        try:
            self.__check_type(element.type, value)
        except InterpreterError as error:
            raise InterpreterError(error.message, str(element))

        self.__contextList[-1].variables[key] = VariableInfo(
            element.type, value)

    def evaluate_if_statement(self, element: IfStatement):
        if isinstance(element.condition, INode):
            element.condition.accept(self)
            value = self.__get_result()
        else:
            value = element.condition

        if bool(value):
            if isinstance(element.statement, INode):
                element.statement.accept(self)
        elif element.elseStatement is not None:
            if isinstance(element.elseStatement, INode):
                element.elseStatement.accept(self)

    def evaluate_while_statement(self, element: WhileStatement):
        while True:
            if isinstance(element.condition, INode):
                element.condition.accept(self)
                value = self.__get_result()
            else:
                value = element.condition

            if bool(value):
                if isinstance(element.statement, INode):
                    element.statement.accept(self)
            else:
                return

    def evaluate_expression(self, element: Expression):
        try:
            if isinstance(element.leftExpression, INode):
                element.leftExpression.accept(self)
                leftValue = self.__get_result()
            else:
                leftValue = element.leftExpression

            if isinstance(element.rightExpression, INode):
                element.rightExpression.accept(self)
                rightValue = self.__get_result()
            else:
                rightValue = element.rightExpression

            self.__check_operands_type(leftValue, rightValue)
        except InterpreterError as error:
            raise InterpreterError(error.message, str(element))

        try:
            if element.operator == '+':
                self.__results.append(leftValue + rightValue)
            else:
                self.__results.append(leftValue - rightValue)
        except TypeError as error:
            raise InterpreterError(
                f"Unsupported operand type(s) for operator: {element.operator}",
                str(element))

    def evaluate_subsexpression(self, element: SubExpression):
        try:
            if isinstance(element.leftFactor, INode):
                element.leftFactor.accept(self)
                leftValue = self.__get_result()
            else:
                leftValue = element.leftFactor

            if isinstance(element.rightFactor, INode):
                element.rightFactor.accept(self)
                rightValue = self.__get_result()
            else:
                rightValue = element.rightFactor
        except InterpreterError as error:
            raise InterpreterError(error.message, str(element))

        if (type(leftValue).__name__ == 'str'):
            raise InterpreterError(
                f"Invalid operation: {element.operator}, on string value: {leftValue}"
            )
        elif (type(rightValue).__name__ == 'str'):
            raise InterpreterError(
                f"Invalid operation: {element.operator}, on string value: {rightValue}"
            )

        if rightValue is None:
            result = leftValue
        else:
            try:
                self.__check_operands_type(leftValue, rightValue)
            except InterpreterError as error:
                raise InterpreterError(error.message, str(element))

            if element.operator == '*':
                result = leftValue * rightValue
            else:
                result = leftValue / rightValue

            #because Python automaticly converts to float if int/int is fractions
            if isinstance(leftValue, int):
                result = math.floor(result)

        if element.isNegated:
            result = result * -1
        self.__results.append(result)

    def evaluate_parentheses_expression(self, element: ParenthesesExpression):
        element.expression.accept(self)

    def evaluate_condition(self, element: Condition):
        if isinstance(element.leftCondition, INode):
            element.leftCondition.accept(self)
            leftValue = self.__get_result()
        else:
            leftValue = element.leftCondition

        if isinstance(element.rightCondition, INode):
            element.rightCondition.accept(self)
            rightValue = self.__get_result()
        elif element.rightCondition is not None:
            rightValue = element.rightCondition

        if element.operator == '&&':
            self.__results.append(bool(leftValue and rightValue))
        elif element.operator == '||':
            self.__results.append(bool(leftValue or rightValue))
        elif element.operator == '<':
            self.__results.append(bool(leftValue < rightValue))
        elif element.operator == '<=':
            self.__results.append(bool(leftValue <= rightValue))
        elif element.operator == '>=':
            self.__results.append(bool(leftValue >= rightValue))
        elif element.operator == '>':
            self.__results.append(bool(leftValue > rightValue))
        elif element.operator == '==':
            self.__results.append(bool(leftValue == rightValue))
        elif element.operator == '!=':
            self.__results.append(bool(leftValue != rightValue))
        else:
            raise InterpreterError(
                f"Invalid operator: {element.operator}. Probably caused by error in parser implementation."
            )

    def evaluate_subcondition(self, element: SubCondition):
        if isinstance(element.value, INode):
            element.value.accept(self)
            value = self.__get_result()
        else:
            value = element.value

        if element.isNegated:
            self.__results.append(not bool(value))
        else:
            self.__results.append(value)

    def evaluate_parentheses_condition(self, element: ParenthesesCondition):
        if isinstance(element.value, INode):
            element.value.accept(self)
            value = self.__get_result()
        else:
            value = element.value

        self.__results.append(bool(value))

    def evaluate_variable(self, element: Variable) -> None:
        key = element.identifier
        if key in self.__get_local_context().variables:
            value = self.__get_local_context().variables[key].value
        elif key in self.__get_global_context().variables:
            value = self.__get_global_context().variables[key].value
        else:
            raise InterpreterError(message=f"Undefined variable: {key}.")

        self.__results.append(value)

    def __build_global_context(self, program: Program) -> None:
        declarationDict = {}
        specialsDict = {}
        for declaration in program.defineStatementList:
            key = declaration.identifier
            if key in declarationDict:
                raise InterpreterError(
                    f"Multiple definitions of the variable {key}.",
                    f"{declaration.type} {declaration.identifier} = {declaration.expression}"
                )
            else:
                declarationDict[key] = VariableInfo(declaration.type,
                                                    declaration.expression)

        functionDefDict = self.__import_stdlib()
        for functionDef in program.functionDefList:
            key = functionDef.identifier
            if key in functionDefDict:
                raise InterpreterError(
                    f"Multiple definitions of the function {key}.")
            else:
                functionDefDict[key] = functionDef
        try:
            specialsDict[EVAL_RETURN_EXP] = functionDefDict["main"].returnType
        except KeyError:
            raise InterpreterError("Not found 'main' function.")

        self.__contextList.append(
            Context(variables=declarationDict,
                    functions=functionDefDict,
                    specials=specialsDict))

    def __build_new_context(self, function: FunctionDef,
                            element: FunctionCall):

        #check number of call arguments
        if len(function.parameters) != len(element.arguments):
            raise InterpreterError(
                f"Expected {len(function.parameters)} arguments, {len(element.arguments)} was provided.",
                str(element))

        try:
            variablesDict = {}
            specialsDict = {}
            #function params to context
            for i in range(len(function.parameters)):
                variable = function.parameters[i]
                argument = element.arguments[i]

                if isinstance(element.arguments[i], INode):
                    argument.accept(self)
                    value = self.__get_result()
                else:
                    value = argument

                #check if argument type match declared type in function definition
                self.__check_type(variable.type, value)

                variablesDict[variable.identifier] = VariableInfo(
                    variable.type, value)
        except InterpreterError as error:
            raise InterpreterError(error.message, str(element))

        specialsDict[EVAL_RETURN_EXP] = function.returnType

        self.__contextList.append(
            Context(variables=variablesDict,
                    functions={},
                    specials=specialsDict))

    def __get_local_context(self) -> Context:
        return self.__contextList[-1]

    def __get_global_context(self) -> Context:
        return self.__contextList[0]

    def __pop_context(self) -> None:
        self.__contextList.pop()

    def __check_type(self, expectedType: str, value):
        valueType = type(value).__name__
        if expectedType == 'string' and valueType == 'str':
            return
        elif expectedType == 'frc' and valueType == 'Fraction':
            return
        #int and float case
        elif valueType == expectedType:
            return

        raise InterpreterError(
            f"Type mismatch. Expected type: {expectedType}, provided type: {valueType}"
        )

    def __check_operands_type(self, leftOperand, rightOperand):
        if not type(leftOperand).__name__ == type(rightOperand).__name__:
            raise InterpreterError(
                f"Invalid operands types. Got: {type(leftOperand).__name__} and {type(rightOperand).__name__}"
            )

    def __add_result(self, result) -> None:
        self.__results.append(result)

    def __get_result(self):
        if not self.__results:
            raise InterpreterError("Expected return value.")

        return self.__results.pop()

    def __peek_result(self):
        return self.__results[-1]

    def __evaluate_expression(self, expression):
        if isinstance(expression, INode):
            expression.accept(self)
        else:
            self.__results.append(expression)

    def __defaultValue(self, type: str):
        if type == 'int': return 0
        elif type == 'float': return 0.0
        elif type == 'frc': return std.functions['frc'](1, 1)
        elif type == 'string': return ""

    def __import_stdlib(self) -> dict:
        functionDefDict = {}
        functionDefDict['print'] = FunctionDef(
            identifier='print',
            parameters=[Parameter(type='string', identifier='number')],
            statement=None)

        functionDefDict['frc'] = FunctionDef(
            identifier='frc',
            parameters=[
                Parameter(type='int', identifier='numerator'),
                Parameter(type='int', identifier='denominator')
            ],
            statement=None,
            returnType='frc')

        functionDefDict['int_to_frc'] = FunctionDef(
            identifier='int_to_frc',
            parameters=[Parameter(type='int', identifier='number')],
            statement=None,
            returnType='frc')

        functionDefDict['int_to_float'] = FunctionDef(
            identifier='int_to_float',
            parameters=[Parameter(type='int', identifier='number')],
            statement=None,
            returnType='float')

        functionDefDict['frc_to_float'] = FunctionDef(
            identifier='frc_to_float',
            parameters=[Parameter(type='frc', identifier='fraction')],
            statement=None,
            returnType='float')

        functionDefDict['float_to_int'] = FunctionDef(
            identifier='float_to_int',
            parameters=[Parameter(type='float', identifier='number')],
            statement=None,
            returnType='int')

        functionDefDict['frc_to_int'] = FunctionDef(
            identifier='frc_to_int',
            parameters=[Parameter(type='frc', identifier='fraction')],
            statement=None,
            returnType='int')

        functionDefDict['frc_to_string'] = FunctionDef(
            identifier='frc_to_string',
            parameters=[Parameter(type='frc', identifier='fraction')],
            statement=None,
            returnType='string')

        functionDefDict['float_to_string'] = FunctionDef(
            identifier='float_to_string',
            parameters=[Parameter(type='float', identifier='number')],
            statement=None,
            returnType='string')

        functionDefDict['int_to_string'] = FunctionDef(
            identifier='int_to_string',
            parameters=[Parameter(type='int', identifier='number')],
            statement=None,
            returnType='string')

        return functionDefDict
from Parser.ast import INode
from collections import namedtuple

Parameter = namedtuple("Parameter", ["type", "identifier"])


class Program(INode):
    def __init__(self, functionDefList: list,
                 defineStatementList: list) -> None:
        self.functionDefList = functionDefList
        self.defineStatementList = defineStatementList

    def __repr__(self):
        program = "Program:\n"
        functions = f"Functions definitions:{self.functionDefList}\n"
        statements = f"Statements:{self.defineStatementList}\n"
        return program + statements + functions

    def accept(self, visitor) -> None:
        visitor.evaluate_program(self)


class FunctionDef(INode):
    def __init__(self,
                 identifier: str,
                 parameters: list[Parameter],
                 statement,
                 returnType: str = None) -> None:
        self.identifier = identifier
        self.parameters = parameters
        self.statement = statement
        self.returnType = returnType

    def __repr__(self):
        identifier = f"identifier:{self.identifier}\n"
        returnType = f"return type:{self.returnType}\n"
        parameters = f"parameters:{self.parameters}\n"
        statement = f"statement:{self.statement}\n"
        return "\n    Function definition:\n" + identifier + returnType + parameters + statement

    def accept(self, visitor) -> None:
        visitor.evaluate_function_definition(self)


class FunctionCall(INode):
    def __init__(self, identifier: str, arguments: list) -> None:
        self.identifier = identifier
        self.arguments = arguments

    def __repr__(self):
        identifier = f"identifier:{self.identifier}\n"
        arguments = f"arguments:{self.arguments}\n"
        return "\n    Function call:\n" + identifier + arguments

    def __str__(self) -> str:
        argumentsStr = ''
        for argument in self.arguments:
            argumentsStr += str(argument) + ','

        argumentsStr = argumentsStr[:-1]
        return "{id}({args})".format(id=self.identifier, args=argumentsStr)

    def accept(self, visitor) -> None:
        visitor.evaluate_function_call(self)


class StatementBlock(INode):
    def __init__(self, statements: list) -> None:
        self.statements = statements

    def __repr__(self):
        statements = f"statements:{self.statements}\n"
        return "\n    Statement block:\n" + statements

    def accept(self, visitor) -> None:
        visitor.evaluate_statement_block(self)


class ReturnStatement(INode):
    def __init__(self, expression) -> None:
        self.expression = expression

    def __repr__(self):
        expression = f"expression:{self.expression}\n"
        return "\n    Return statement:\n" + expression

    def __str__(self) -> str:
        return "return {exp};".format(exp=str(self.expression))

    def accept(self, visitor) -> None:
        visitor.evaluate_return_statement(self)


class AssignStatement(INode):
    def __init__(self, identifier, expression) -> None:
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        identifier = f"identifier:{self.identifier}\n"
        expression = f"expression:{self.expression}\n"
        return "\n    Assigne statement:\n" + identifier + expression

    def __str__(self) -> str:
        return "{id} = {exp};".format(id=str(self.identifier),
                                      exp=str(self.expression))

    def accept(self, visitor) -> None:
        visitor.evaluate_assigne_statement(self)


class DefineStatement(INode):
    def __init__(self, type, identifier, expression=None) -> None:
        self.type = type
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        type = f"type:{self.type}\n"
        identifier = f"identifier:{self.identifier}\n"
        expression = f"expression:{self.expression}\n"
        return "\n    Define statement:\n" + type + identifier + expression

    def __str__(self) -> str:
        return "{type} {id} = {exp};".format(type=str(self.type),
                                             id=str(self.identifier),
                                             exp=str(self.expression))

    def accept(self, visitor) -> None:
        visitor.evaluate_define_statement(self)


class IfStatement(INode):
    def __init__(self, condition, statement, elseStatement=None) -> None:
        self.condition = condition
        self.statement = statement
        self.elseStatement = elseStatement

    def __repr__(self):
        condition = f"condition:{self.condition}\n"
        statement = f"statement:{self.statement}\n"
        elseStatement = f"else statement:{self.elseStatement}\n"
        return "\n    If statement:\n" + condition + statement + elseStatement

    def accept(self, visitor) -> None:
        visitor.evaluate_if_statement(self)


class WhileStatement(INode):
    def __init__(self, condition, statement) -> None:
        self.condition = condition
        self.statement = statement

    def __repr__(self):
        condition = f"condition:{self.condition}\n"
        statement = f"statement:{self.statement}\n"
        return "\n    While statement:\n" + condition + statement

    def accept(self, visitor) -> None:
        visitor.evaluate_while_statement(self)


class Expression(INode):
    def __init__(self,
                 leftExpression,
                 operator=None,
                 rightExpression=None) -> None:
        self.leftExpression = leftExpression
        self.rightExpression = rightExpression
        self.operator = operator

    def __repr__(self):
        leftExpression = f"left expression:{self.leftExpression}\n"
        rightExpression = f"right expression:{self.rightExpression}\n"
        operator = f"operator:{self.operator}\n"
        return "\n    Expression:\n" + operator + leftExpression + rightExpression

    def __str__(self) -> str:
        return "{le} {op} {re}".format(le=str(self.leftExpression),
                                       op=str(self.operator or ''),
                                       re=str(self.rightExpression or ''))

    def accept(self, visitor) -> None:
        visitor.evaluate_expression(self)


class SubExpression(INode):
    def __init__(self,
                 leftFactor,
                 operator=None,
                 rightFactor=None,
                 isNegated: bool = False) -> None:
        self.leftFactor = leftFactor
        self.rightFactor = rightFactor
        self.operator = operator
        self.isNegated = isNegated

    def __repr__(self):
        leftFactor = f"left factor:{self.leftFactor}\n"
        rightFactor = f"right factor:{self.rightFactor}\n"
        operator = f"operator:{self.operator}\n"
        isNegated = "Negation:No\n" if not self.isNegated else "Negation:Yes\n"
        return "\n    Multiplicative expression:\n" + isNegated + operator + leftFactor + rightFactor

    def __str__(self) -> str:
        return "{lf} {op} {rf}".format(lf=str(self.leftFactor),
                                       op=str(self.operator or ''),
                                       rf=str(self.rightFactor or ''))

    def accept(self, visitor) -> None:
        visitor.evaluate_subsexpression(self)


class ParenthesesExpression(INode):
    def __init__(self, expression) -> None:
        self.expression = expression

    def __repr__(self):
        return f"\n    Parentheses expression:{self.expression}\n"

    def __str__(self) -> str:
        return "({exp})".format(exp=str(self.expression))

    def accept(self, visitor) -> None:
        visitor.evaluate_parentheses_expression(self)


class Variable(INode):
    def __init__(self, identifier: str) -> None:
        self.identifier = identifier

    def __repr__(self):
        return f"\n    Variable:{self.identifier}\n"

    def __str__(self) -> str:
        return self.identifier

    def accept(self, visitor) -> None:
        visitor.evaluate_variable(self)


class Condition(INode):
    def __init__(self,
                 leftCondition,
                 operator=None,
                 rightCondition=None) -> None:
        self.leftCondition = leftCondition
        self.rightCondition = rightCondition
        self.operator = operator

    def __repr__(self):
        leftCondition = f"left condition:{self.leftCondition}\n"
        rightCondition = f"right condition:{self.rightCondition}\n"
        operator = f"operator:{self.operator}\n"
        return "\n    Condition:\n" + operator + leftCondition + rightCondition

    def accept(self, visitor) -> None:
        visitor.evaluate_condition(self)


class SubCondition(INode):
    def __init__(self, value, isNegated: bool = False) -> None:
        self.value = value
        self.isNegated = isNegated

    def __repr__(self):
        isNegated = "Negation:No\n" if not self.isNegated else "Negation:Yes\n"
        return f"\n    Parentheses condition:\n{isNegated}\n{self.value}\n"

    def accept(self, visitor) -> None:
        visitor.evaluate_subcondition(self)


class ParenthesesCondition(INode):
    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self):
        return f"\n    Parentheses condition:{self.value}\n"

    def accept(self, visitor) -> None:
        visitor.evaluate_parentheses_condition(self)
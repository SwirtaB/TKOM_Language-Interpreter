from HelperModules.errorhandler import ParserError
from HelperModules.symbols import TokenTypes
from Lexer.lexer import Lexer
from Lexer.token import Token
from Parser.types import *
from typing import Optional


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        if lexer is None:
            raise ParserError("Lexer module not provided.")

        self.lexer: Lexer = lexer
        self.currentToken: Token = self.lexer.get_token()

    def __get_next_token(self) -> Token:
        self.currentToken = self.lexer.get_token()
        return self.currentToken

    def __get_current_token(self) -> Token:
        return self.currentToken

    def __token_required(self, tokenTypes: list[TokenTypes]) -> bool:
        if self.__get_current_token().type in tokenTypes:
            return True
        else:
            raise ParserError(
                message=f'Expected one of: {str(*tokenTypes, )}.',
                currentToken=self.__get_current_token())

    def __token_required_consume(self, tokenTypes: list[TokenTypes]) -> bool:
        result = self.__token_required(tokenTypes)
        self.__get_next_token()
        return result

    def __try_parse_operator(
            self, possibleOperators: list[TokenTypes]) -> Optional[str]:
        if not self.__get_current_token().type in possibleOperators:
            return None

        result = self.__get_current_token().value
        self.__get_next_token()
        return result

    def __try_parse_type(self) -> Optional[str]:
        lexerToken = self.__get_current_token()
        if lexerToken.value in ["int", "float", "frc", "string"]:
            self.__get_next_token()
            return lexerToken.value
        else:
            return None

    def __try_parse_literal(self):
        if not self.__get_current_token().type in [
                TokenTypes.INTEGER_LITERAL, TokenTypes.FLOAT_LITERAL,
                TokenTypes.STRING_LITERAL
        ]:
            return None

        result = self.__get_current_token().value
        self.__get_next_token()
        return result

    def __try_parse_identifier(self) -> Optional[str]:
        lexerToken = self.__get_current_token()
        if lexerToken.type == TokenTypes.IDENTIFIER:
            self.__get_next_token()
            return lexerToken.value
        elif (type := self.__try_parse_type()) is not None:
            return type
        else:
            return None

    def __try_parse_function_call_or_identifier(self):
        if (identifier := self.__try_parse_identifier()) is None:
            return None

        if self.__get_current_token().type != TokenTypes.OPEN_PARENTHESES:
            return Variable(identifier)
        else:
            self.__get_next_token()
            arguments = self.__try_parse_arguments()
            if self.__token_required_consume(
                    tokenTypes=[TokenTypes.CLOSE_PARENTHESES]):
                return FunctionCall(identifier=identifier, arguments=arguments)

    def __try_parse_arguments(self) -> list:
        argumentsList = []
        if (argument := self.__try_parse_expression()) is not None:
            argumentsList.append(argument)

        while self.__get_current_token().type == TokenTypes.COMMA:
            self.__get_next_token()
            if (argument := self.__try_parse_expression()) is not None:
                argumentsList.append(argument)
            else:
                raise ParserError(message="Expected expression after \',\'.",
                                  currentToken=self.__get_current_token())

        return argumentsList

    def __try_parse_single_parameter(self) -> Parameter:
        if (type := self.__try_parse_type()) is None:
            return None

        if (identifier := self.__try_parse_identifier()) is None:
            raise ParserError(message="Expected identifier after type.",
                              currentToken=self.__get_current_token())

        return Parameter(type, identifier)

    def __try_parse_parameters(self) -> list[Parameter]:
        parametersList = []
        if (parameter := self.__try_parse_single_parameter()) is not None:
            parametersList.append(parameter)
        while self.__get_current_token().type == TokenTypes.COMMA:
            self.__get_next_token()
            if (parameter := self.__try_parse_single_parameter()) is not None:
                parametersList.append(parameter)
            else:
                raise ParserError(message="Expected parameter after \',\'.",
                                  currentToken=self.__get_current_token())

        return parametersList

    def __try_parse_factor(self):
        for try_parse in [
                self.__try_parse_literal,
                self.__try_parse_function_call_or_identifier,
                self.__try_parse_parentheses_expression
        ]:
            if (result := try_parse()) is not None:
                return result

        return None

    def __try_parse_subexpression(self) -> Optional[SubExpression]:
        isNegated = False
        if self.__get_current_token().type == TokenTypes.MINUS:
            isNegated = True
            self.__get_next_token()

        if (left := self.__try_parse_factor()) is None:
            if isNegated:
                raise ParserError(message="Expected factor after \'-\'.",
                                  currentToken=self.__get_current_token())
            else:
                return None

        if isNegated and self.__get_current_token().type not in [
                TokenTypes.MULTIPLY, TokenTypes.DIVIDE
        ]:
            return SubExpression(leftFactor=left, isNegated=isNegated)

        while operator := self.__try_parse_operator(
                possibleOperators=[TokenTypes.MULTIPLY, TokenTypes.DIVIDE]):
            if (right := self.__try_parse_factor()) is None:
                raise ParserError(
                    message="Expected factor after operator ( \'*\' or \'/\').",
                    currentToken=self.__get_current_token())

            left = SubExpression(leftFactor=left,
                                 operator=operator,
                                 rightFactor=right,
                                 isNegated=isNegated)

        return left

    def __try_parse_expression(self) -> Optional[Expression]:
        if (left := self.__try_parse_subexpression()) is None:
            return None

        while operator := self.__try_parse_operator(
                possibleOperators=[TokenTypes.PLUS, TokenTypes.MINUS]):
            if (right := self.__try_parse_subexpression()) is None:
                raise ParserError(
                    message=
                    "Expected expression after operator ( \'+\' or \'-\').",
                    currentToken=self.__get_current_token())

            left = Expression(leftExpression=left,
                              operator=operator,
                              rightExpression=right)

        return left

    def __try_parse_parentheses_expression(self) -> Optional[Expression]:
        if self.__get_current_token().type != TokenTypes.OPEN_PARENTHESES:
            return None

        self.__get_next_token()
        if (expression := self.__try_parse_expression()) is None:
            raise ParserError(message="Expected expression after \'(\'.",
                              currentToken=self.__get_current_token())

        if not self.__token_required(
                tokenTypes=[TokenTypes.CLOSE_PARENTHESES]):
            raise ParserError(message="Expected \')\' after expression",
                              currentToken=self.__get_current_token())

        self.__get_next_token()
        return expression

    def __try_parse_assign_or_function_call(self):
        result = self.__try_parse_function_call_or_identifier()
        if result is None:
            return None
        elif type(result) is FunctionCall:
            self.__token_required_consume(tokenTypes=[TokenTypes.SEMICOLON])
            return result

        #result is type Variable
        self.__token_required_consume(tokenTypes=[TokenTypes.ASSIGNMENT])
        if (expression := self.__try_parse_expression()) is None:
            raise ParserError(message="Expected expression after \'=\'.",
                              currentToken=self.__get_current_token())

        self.__token_required_consume(tokenTypes=[TokenTypes.SEMICOLON])
        return AssignStatement(result, expression)

    def __try_parse_parentheses_condition(self):
        if self.__get_current_token().type != TokenTypes.OPEN_PARENTHESES:
            return None

        self.__get_next_token()
        if (condition := self.__try_parse_condition()) is None:
            raise ParserError(message="Expected condition after \'(\'.",
                              currentToken=self.__get_current_token())

        self.__token_required_consume(
            tokenTypes=[TokenTypes.CLOSE_PARENTHESES])
        return condition

    def __try_parse_subcondition(self):
        isNegated = False
        if self.__get_current_token().type == TokenTypes.NEGATION:
            isNegated = True
            self.__get_next_token()

        if self.__get_current_token().type != TokenTypes.OPEN_PARENTHESES:
            condition = self.__try_parse_expression()
        else:
            condition = self.__try_parse_parentheses_condition()

        if condition is None:
            if isNegated:
                raise ParserError(message="Expected condition after \'!\'.",
                                  currentToken=self.__get_current_token())
            else:
                return None

        return SubCondition(value=condition, isNegated=isNegated)

    def __try_parse_condition(self):
        if (left := self.__try_parse_subcondition()) is None:
            return None

        if operator := self.__try_parse_operator(possibleOperators=[
                TokenTypes.LESS, TokenTypes.LESS_OR_EQUAL, TokenTypes.EQUAL,
                TokenTypes.GREATER, TokenTypes.GREATER_OR_EQUAL,
                TokenTypes.NOT_EQUAL, TokenTypes.AND, TokenTypes.OR
        ]):
            if (right := self.__try_parse_subcondition()) is None:
                raise ParserError(
                    message=
                    "Expected parenthesis condition or expression after logical operator.",
                    currentToken=self.__get_current_token())

            left = Condition(leftCondition=left,
                             operator=operator,
                             rightCondition=right)

        return left

    def __try_parse_if_statement(self):
        if self.__get_current_token().type != TokenTypes.IF:
            return None

        self.__get_next_token()
        self.__token_required_consume(tokenTypes=[TokenTypes.OPEN_PARENTHESES])
        if (condition := self.__try_parse_condition()) is None:
            raise ParserError(message="Expected condition after \'(\'.",
                              currentToken=self.__get_current_token())

        self.__token_required_consume(
            tokenTypes=[TokenTypes.CLOSE_PARENTHESES])
        if (statement := self.__try_parse_statement()) is None:
            raise ParserError(message="Expected statement.",
                              currentToken=self.__get_current_token())

        if self.__get_current_token().type == TokenTypes.ELSE:
            self.__get_next_token()
            if (elseStatement := self.__try_parse_statement()) is None:
                raise ParserError(
                    message="Expected statement after \'else\' keyword.",
                    currentToken=self.__get_current_token())
            return IfStatement(condition, statement, elseStatement)

        return IfStatement(condition, statement)

    def __try_parse_while_statement(self):
        if self.__get_current_token().type != TokenTypes.WHILE:
            return None

        self.__get_next_token()
        self.__token_required_consume(tokenTypes=[TokenTypes.OPEN_PARENTHESES])
        if (condition := self.__try_parse_condition()) is None:
            raise ParserError(message="Expected condition after \'(\'.",
                              currentToken=self.__get_current_token())

        self.__token_required_consume(
            tokenTypes=[TokenTypes.CLOSE_PARENTHESES])
        if (statement := self.__try_parse_statement()) is None:
            raise ParserError(message="Expected statement.",
                              currentToken=self.__get_current_token())

        return WhileStatement(condition, statement)

    def __try_parse_return_statement(self) -> ReturnStatement:
        if self.__get_current_token().type != TokenTypes.RETURN:
            return None

        self.__get_next_token()
        if (expression := self.__try_parse_expression()) is None:
            raise ParserError(
                message="Expected expression after \'return\' keyword.",
                currentToken=self.__get_current_token())

        self.__token_required_consume(tokenTypes=[TokenTypes.SEMICOLON])
        return ReturnStatement(expression)

    def __try_parse_define_statement(self) -> Optional[DefineStatement]:
        if type := self.__try_parse_type():
            if identifier := self.__try_parse_identifier():
                if self.__get_current_token().type == TokenTypes.ASSIGNMENT:
                    self.__get_next_token()
                    assignement = self.__try_parse_expression()
                    if assignement is None:
                        raise ParserError(
                            message="Expected expression after \'=\'.",
                            currentToken=self.__get_current_token())

                    defineStatement = DefineStatement(type, identifier,
                                                      assignement)
                else:
                    defineStatement = DefineStatement(type, identifier)

                self.__token_required_consume(
                    tokenTypes=[TokenTypes.SEMICOLON])
                return defineStatement

            else:
                raise ParserError(message="Expected identifier after type.",
                                  currentToken=self.__get_current_token())
        else:
            return None

    def __try_parse_function_definition(self) -> Optional[FunctionDef]:
        if self.__get_current_token().type != TokenTypes.FUNCTION:
            return None

        self.__get_next_token()
        if (identifier := self.__try_parse_identifier()) is None:
            raise ParserError(message="Expected identifier after \'fn\'.",
                              currentToken=self.__get_current_token())

        self.__token_required_consume(tokenTypes=[TokenTypes.OPEN_PARENTHESES])
        parameters = self.__try_parse_parameters()
        self.__token_required_consume(
            tokenTypes=[TokenTypes.CLOSE_PARENTHESES])

        returnType = None
        if self.__get_current_token().type == TokenTypes.RETURN_SIGN:
            self.__get_next_token()
            if (returnType := self.__try_parse_type()) is None:
                raise ParserError(
                    message="Expected type after return sign \'->\'.",
                    currentToken=self.__get_current_token())

        if (statement := self.__try_parse_statement()) is None:
            raise ParserError(
                message="Expected statement after function declaration",
                currentToken=self.__get_current_token())

        return FunctionDef(identifier=identifier,
                           parameters=parameters,
                           statement=statement,
                           returnType=returnType)

    def __try_parse_statement(self):
        for try_parse in [
                self.__try_parse_define_statement,
                self.__try_parse_assign_or_function_call,
                self.__try_parse_if_statement,
                self.__try_parse_while_statement,
                self.__try_parse_return_statement
        ]:
            if (statement := try_parse()) is not None:
                return statement

        self.__token_required_consume(tokenTypes=[TokenTypes.OPEN_BRACE])
        statements = []
        while self.__get_current_token().type != TokenTypes.CLOSE_BRACE:
            if (statement := self.__try_parse_statement()) is None:
                raise ParserError(message="Expected statement.",
                                  currentToken=self.__get_current_token())

            statements.append(statement)

        self.__token_required_consume(tokenTypes=[TokenTypes.CLOSE_BRACE])
        return StatementBlock(statements)

    def try_parse_program(self) -> Optional[Program]:
        self.__functionDefList = []
        self.__defineStatementList = []

        while self.__get_current_token().type != TokenTypes.EOF:
            if result := self.__try_parse_function_definition():
                self.__functionDefList.append(result)
            elif result := self.__try_parse_define_statement():
                self.__defineStatementList.append(result)

            if ((not bool(self.__functionDefList)) or
                (not bool(self.__defineStatementList))) and result is None:
                raise ParserError(message="Invalid token.",
                                  currentToken=self.__get_current_token())

        if (not bool(self.__functionDefList)) and (not bool(
                self.__defineStatementList)):
            return None
        else:
            return Program(self.__functionDefList, self.__defineStatementList)

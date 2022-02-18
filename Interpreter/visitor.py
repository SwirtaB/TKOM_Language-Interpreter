from abc import ABC, abstractmethod
from Parser.types import *


class Visitor(ABC):
    @abstractmethod
    def evaluate_program(self, element: Program):
        pass

    @abstractmethod
    def evaluate_function_definition(self, element: FunctionDef):
        pass

    @abstractmethod
    def evaluate_function_call(self, element: FunctionCall):
        pass

    @abstractmethod
    def evaluate_statement_block(self, element: StatementBlock):
        pass

    @abstractmethod
    def evaluate_return_statement(self, element: ReturnStatement):
        pass

    @abstractmethod
    def evaluate_assigne_statement(self, element: AssignStatement):
        pass

    @abstractmethod
    def evaluate_define_statement(self, element: DefineStatement):
        pass

    @abstractmethod
    def evaluate_if_statement(self, element: IfStatement):
        pass

    @abstractmethod
    def evaluate_while_statement(self, element: WhileStatement):
        pass

    @abstractmethod
    def evaluate_expression(self, element: Expression):
        pass

    @abstractmethod
    def evaluate_subsexpression(self, element: SubExpression):
        pass

    @abstractmethod
    def evaluate_parentheses_expression(self, element: ParenthesesExpression):
        pass

    @abstractmethod
    def evaluate_condition(self, element: Condition):
        pass

    @abstractmethod
    def evaluate_subcondition(self, element: SubCondition):
        pass

    @abstractmethod
    def evaluate_parentheses_condition(self, element: ParenthesesCondition):
        pass

    @abstractmethod
    def evaluate_variable(self, element: Variable):
        pass

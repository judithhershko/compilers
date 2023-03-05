from generated.input.ExpressionVisitor import *
from HelperFunctions import *
from .ast.node import Value, BinaryOperator,AST_node
from .ast.AST import *


# replace with result for optimisation
class EvalVisitor(ExpressionVisitor):
    def __init__(self):
        self.trees=[]
        self.ctree=None
        self.parent=None
        self.current=None
        self.count=0
    def visitDec(self, ctx:ParserRuleContext):
        pass


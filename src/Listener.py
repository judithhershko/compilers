from .ast.AST import *
from generated.input.ExpressionListener import *


def create_tree():
    expression_tree = AST()
    expression_tree.setRoot(None)
    return expression_tree


class Expression(ExpressionListener):
    def __init__(self):
        print("enter expression")
        self.asT = create_tree()
        self.current = None
        self.parent = None

    def enterExpr(self, ctx):
        print("enter expression is:" + ctx.getText())
        # print(ctx.getToken(int))

        if (ctx.binop()):
            print("enter xpr")

    def exitExpr(self, ctx):
        pass

    def enterDec(self, ctx):
        print("enter declaration is: " + ctx.getText())

    def enterBinop(self, ctx):
        print("enter declaration is: " + ctx.getText())

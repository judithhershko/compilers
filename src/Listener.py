from AST_.AST import *
from AST_.node import BinaryOperator
from generated.input.ExpressionListener import *


def create_tree():
    expression_tree = AST()
    expression_tree.setRoot(None)
    return expression_tree


class Expression(ExpressionListener):
    def __init__(self):
        self.trees = []  # A stack containing all subtrees
        self.scope_count = 0  # The current scope we are finding ourselves in
        self.asT = create_tree()
        self.count = 0
        self.nr = 0
        self.left = False
        self.right = False
        self.lParent = None
        self.rParent = None
        self.parent = None
        self.root = True

    def add(self, ast):
        self.trees.append(ast)

    def enterExpr(self, ctx):
        self.count += 1
        self.nr += 1
        print("enter expression is:" + ctx.getText())
        # print(ctx.getToken(int))
        if (ctx.binop()):
            self.count = 1
            # print("val:"+ ctx.expr(0).getText()+ "op:" +ctx.binop().getText()+"val2:"+ctx.expr(1).getText() )
            node = BinaryOperator(ctx.getText())
            self.left = True
            if self.root:
                self.parent = node
                self.root = False
                self.left = True
                self.asT.setRoot(self.parent)
            elif (self.left):
                self.lParent = self.parent
                self.parent.setLeftChild(node)
                self.left = False
                self.right = True
            elif (self.right):
                self.rParent = self.parent
                self.parent.setRightChild(node)
                self.right = False

            self.asT.setRoot(node)
        elif self.left == True:
            node = BinaryOperator(ctx.getText())
            self.parent.setLeftChild(node)
            self.left = False
            self.right = True
        elif self.right == True:
            node = BinaryOperator(ctx.getText())
            self.parent.setRightChild(node)
            self.left = False
            self.right = False

        if self.left:
            left = BinaryOperator(ctx.getText())
            self.parent.setLeftChild(left)
            self.left = False
        if self.count == 3:
            right = BinaryOperator(ctx.getText())
            self.parent.setRightChild(right)
            self.right = True

    def exitExpr(self, ctx):
        print("leaving: " + ctx.getText())

    def enterDec(self, ctx):
        print("enter declaration is: " + ctx.getText())

    def enterBinop(self, ctx):
        print("enter declaration is: " + ctx.getText())

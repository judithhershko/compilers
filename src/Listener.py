from AST_.AST import *
from AST_.node import *
from generated.input.ExpressionListener import *


def create_tree():
    expression_tree = AST()
    expression_tree.setRoot(None)
    return expression_tree


def find_parent(nodes) -> BinaryOperator:
    parent = nodes
    while parent.has_left_chid():
        parent = parent.LeftChild
    return parent


def has_children(ctx: ParserRuleContext):
    return ctx.getChildCount() > 1


def nr_children(ctx: ParserRuleContext):
    return ctx.getChildCount()


class Expression(ExpressionListener):
    def __init__(self):
        self.trees = []  # A stack containing all subtrees
        self.label_trees=[]
        self.path = []  # 0 left 1 right
        self.asT = create_tree()
        self.c_level=0
        self.c_child=0
        self.count = 0
        self.nr = 0
        self.left = False
        self.right = False
        self.lParent = None
        self.rParent = None
        self.parent = BinaryOperator("")
        self.root = True
        self.low_level = None
        self.top_level = None
        self.tijdL = None
        self.tijdR = None


    def search_left(self, left: BinaryOperator):
        if left.leftChild is None:
            return left
        else:
            return self.search_left(left.leftChild)

    def search_right(self, right: BinaryOperator):
        if right.rightChild is None:
            return right
        else:
            return self.search_left(right.rightChild)

    def add(self, ast):
        self.trees.append(ast)

    def enterExpr(self, ctx):
        #print("expression entered:"+ ctx.getText())
        print("has children/"+ has_children(ctx))

    def exitExpr(self, ctx):
        # print("leaving: " + ctx.getText())
        pass

    def enterDec(self, ctx):
        # print("enter declaration is: " + ctx.getText())
        pass

    def enterBinop(self, ctx):
        # print("enter declaration is: " + ctx.getText())
        pass

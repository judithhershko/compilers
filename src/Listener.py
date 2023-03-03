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
        self.count += 1
        self.nr += 1
        # print(ctx.getToken(int))
        if ctx.binop():
            self.count = 1
            tnode = BinaryOperator(ctx.getText())
            self.left = True
            if self.root:
                self.parent = tnode
                self.root = False
                self.left = True
                self.asT.setRoot(self.parent)
                self.asT.setNodeIds(self.asT.root)
                print(self.asT.root.operator)

            elif self.parent.leftChild and not self.parent.rightChild and self.lParent is None:
                self.parent.setLeftChild(tnode)
                self.lParent = self.parent
                self.asT.setRoot(self.parent)
                self.asT.setNodeIds(self.root)
                print("l", self.c_level,"left")
                if not has_children(ctx):
                    self.left = False
                    self.right = True
            elif self.left and not self.right:
                self.lParent.setLeftChild(tnode)
                self.asT.setRoot(self.lParent)
                """
                probleem
                """
                self.lParent = self.lParent.leftChild
                if not has_children(ctx):
                    self.left = False
                    self.right = True

            elif self.right and self.lParent is None:
                self.parent.setRightChild(tnode)
                self.asT.setRoot(self.parent)
                self.rParent = self.parent.rightChild
                if not has_children(ctx):
                    self.right = False
                    self.left = True

            self.asT.setRoot(tnode)
        elif self.left:
            print("left nr:", nr_children(ctx))
            lnode = BinaryOperator(ctx.getText())
            if self.parent.leftChild is None:
                self.parent.setLeftChild(lnode)
                self.asT.setRoot(self.parent)
                if nr_children(ctx) == 1:
                    self.left = False
                    self.right = True
            elif self.rParent is not None:
                self.rParent.setLeftChild(lnode)
                self.parent.rightChild=self.rParent
                self.asT.setRoot(self.parent)
                if has_children(ctx):
                    print("hier geraakt")
                    self.parent=self.rParent
                    self.rParent=None
                    ###########
            elif self.parent.leftChild.leftChild is None:
                self.parent.leftChild.setLeftChild(lnode)
                self.asT.setRoot(self.parent)
                self.left = False
                self.right = True

        elif self.right:
            """
            find current level
            """
            if self.parent.leftChild is not None and self.parent.leftChild.leftChild is not None:
                print("tot hier")
                rnode = BinaryOperator(ctx.getText())
                self.parent.leftChild.setRightChild(rnode)
                self.asT.setRoot(self.parent)
                self.left = True
                self.right = False
            if self.parent.leftChild is not None and self.parent.leftChild.leftChild is None:
                rnode = BinaryOperator(ctx.getText())
                self.parent.setRightChild(rnode)
                self.asT.setRoot(self.parent)
                print(
                    "right: root" + self.asT.root.operator + "left=" + self.asT.root.leftChild.operator + "right=" + self.asT.root.rightChild.operator)
                if has_children(ctx):
                    self.c_level+=1
                    self.rParent = self.parent.rightChild
                    self.lParent = None
                self.left = True
                self.right = False

    def exitExpr(self, ctx):
        # print("leaving: " + ctx.getText())
        pass

    def enterDec(self, ctx):
        # print("enter declaration is: " + ctx.getText())
        pass

    def enterBinop(self, ctx):
        # print("enter declaration is: " + ctx.getText())
        pass

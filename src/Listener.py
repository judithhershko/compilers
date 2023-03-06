from .ast.AST import *
from generated.input.ExpressionListener import *
from .ast.node import Value, BinaryOperator
from HelperFunctions import *


class Expression(ExpressionListener):
    def __init__(self):
        self.asT = create_tree()
        self.current = None
        self.parent = None
        self.need_token = False
        self.trees = []
        self.left = True
        self.right = False

    def has_children(self, ctx: ParserRuleContext):
        return ctx.getChildCount() > 1

    def set_val(self, ctx: ParserRuleContext):
        self.current = Value(ctx.getText(), node.LiteralType.STR, self.parent)
        if self.left and not self.right:
            self.parent.setLeftChild(self.current)
        else:
            self.parent.setRightChild(self.current)
        self.current.parent = self.parent

    def enterExpr(self, ctx):
        print("enter expr:"+ctx.getText())
        if self.has_children(ctx):
            self.left = True
            if self.parent is None:
                self.parent = BinaryOperator("")
                self.current = BinaryOperator("")
                self.current.parent = self.parent
                self.parent.setLeftChild(self.current)
                self.parent.setRightChild(self.current)

            elif self.right:
                self.current = BinaryOperator(ctx.getText(), self.parent)
                self.current.parent = self.parent
                self.parent.setRightChild(self.current)
                self.parent = self.current
                self.current = self.parent.leftChild
                self.right = False

            else:
                self.current = BinaryOperator(ctx.getText(), self.parent)
                self.current.parent = self.parent
                self.parent.setLeftChild(self.current)
                self.parent = self.current
                self.current = self.parent.leftChild
        else:
            self.set_val(ctx)
            if self.left:
                self.need_token = True

    def exitExpr(self, ctx):
        if self.has_children(ctx):
            if self.parent.rightChild is None:
                self.parent.setRightChild(Value("", node.LiteralType.STR))
            self.current = self.current.parent
            self.parent = self.current.parent

    def enterDec(self, ctx):
        print("enter dec:" + ctx.getText())
        if self.parent or self.current is not None:
            self.asT.setRoot(self.current)
            self.trees.append(self.asT)
        self.asT = create_tree()
        self.parent = BinaryOperator("=")
        var = getVariable(ctx.getText())
        self.current = Value(var, node.LiteralType.VAR, self.parent)
        self.parent.setLeftChild(self.current)
        self.current = self.parent.rightChild
        self.right = True

        """
        if self.current is not None:
            self.asT.setRoot(self.current)
            self.trees.append(self.asT)
        self.asT = create_tree()
        self.parent = BinaryOperator("=")
        self.parent.leftChild = Value(getVariable(ctx.getText()), node.LiteralType.VAR)
        self.parent.rightChild = Value(ctx.getText(), node.LiteralType.STR, self.parent)
        self.current=self.parent.rightChild
        self.right=True
        """

    def exitDec(self, ctx):
        print("exit dec:" + ctx.getText())
        if isinstance(self.current, Value):
            print("current:" + self.current.value)
        if isinstance(self.current, BinaryOperator):
            print("current:" + self.current.operator)
        f=True
        while f:
            if isinstance(self.current,BinaryOperator) and self.current.operator=="=":
                f=False
            else:
                self.current = self.current.parent
        print("op:"+self.current.operator)
        print("lchild:"+self.current.leftChild.value)
        self.asT.setRoot(self.current)
        self.trees.append(self.asT)
        self.parent = None
        self.current = None
        self.asT = create_tree()
        """
        self.asT.setRoot(self.current)
        self.trees.append(self.asT)
        self.asT = create_tree()
        """

    def enterBinop(self, ctx):
        if self.need_token:
            self.parent.operator = ctx.getText()
            self.current.parent = self.parent
            self.parent.setLeftChild(self.current)
            rchild = self.parent.getRightChild()
            if rchild is None:
                rchild = Value("", node.LiteralType.STR)
            rchild.parent = self.parent
            self.parent.setRightChild(rchild)
            self.current = self.parent.getRightChild()
            self.left = False
            self.right = True

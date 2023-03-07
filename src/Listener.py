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
        self.declaration=False

    def has_children(self, ctx: ParserRuleContext):
        return ctx.getChildCount() > 1
    def enterTyped_var(self, ctx:ParserRuleContext):
        if not self.declaration:
            return
        self.parent.leftChild.setType(find_type(ctx.getText()))
        self.parent.leftChild.setValue(separate_type_variable(self.parent.leftChild.getValue(),ctx.getText()))
        self.declaration=False

    def set_val(self, ctx: ParserRuleContext):
        self.current = Value(ctx.getText(), node.LiteralType.STR, self.parent)
        if self.left and not self.right:
            self.parent.setLeftChild(self.current)
            self.right=True
        else:
            self.parent.setRightChild(self.current)
            self.right=False
        self.current.parent = self.parent
        if self.left:
            self.need_token = True

    def enterExpr(self, ctx):
        if self.has_children(ctx):
            self.left = True
            if self.parent is None:
                self.parent = BinaryOperator("")
                self.current = BinaryOperator("",self.parent)
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
            """
            self.set_val(ctx)
            if self.left:
                self.need_token = True
            """
            return

    def exitExpr(self, ctx):
        #print("exit expr:"+ctx.getText())
        return self.move_up(ctx)

    def enterDec(self, ctx):
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
        self.declaration=True

    def exitDec(self, ctx):
        f=True
        while f:
            if isinstance(self.current,BinaryOperator) and self.current.operator=="=":
                f=False
            else:
                self.current = self.current.parent
        self.asT.setRoot(self.current)
        self.trees.append(self.asT)
        self.parent = None
        self.current = None
        self.asT = create_tree()

    def enterBinop(self, ctx):
        return self.set_token(ctx)
    # Enter a parse tree produced by ExpressionParser#binop_md.
    def set_token(self,ctx):
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
    def enterBinop_md(self, ctx):
        return self.set_token(ctx)

    # Exit a parse tree produced by ExpressionParser#binop_md.
    def exitBinop_md(self, ctx):
        pass
    def enterTerm(self, ctx:ParserRuleContext):
        #print("enter term:"+ctx.getText())
        self.set_exptr(ctx)

    # Exit a parse tree produced by ExpressionParser#term.
    def exitTerm(self, ctx:ParserRuleContext):
        #print("exit term:"+ctx.getText())
        self.move_up(ctx)
    def enterPri(self, ctx:ParserRuleContext):
        print("enter pri:"+ctx.getText())
        return self.set_val(ctx)

    # Exit a parse tree produced by ExpressionParser#pri.
    def exitPri(self, ctx:ParserRuleContext):
        #print("exit pri:"+ctx.getText())
        pass
    def set_exptr(self,ctx:ParserRuleContext):
        if self.has_children(ctx):
            self.left = True
            if self.parent is None:
                self.parent = BinaryOperator("")
                self.current = BinaryOperator("",self.parent)
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
            """
            self.set_val(ctx)
            if self.left:
                self.need_token = True
            """
    def move_up(self,ctx:ParserRuleContext):
        if self.has_children(ctx):
            if self.parent.rightChild is None:
                self.parent.setRightChild(Value("", node.LiteralType.STR))
            self.current = self.current.parent
            self.parent = self.current.parent



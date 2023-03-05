from .ast.AST import *
from generated.input.ExpressionListener import *
from .ast.node import Value, BinaryOperator


def create_tree():
    expression_tree = AST()
    expression_tree.setRoot(None)
    return expression_tree


class Expression(ExpressionListener):
    def __init__(self):
        self.asT = create_tree()
        self.lcurrent=None
        self.rcurrent=None
        self.current = None
        self.parent = None
        self.p_token = ""
        self.need_token = False
        self.trees = []
        self.count = 0
        self.left = True
        self.right = False

    def has_children(self, ctx: ParserRuleContext):
        return ctx.getChildCount() > 1

    def set_val(self, ctx: ParserRuleContext):
        self.current = Value(ctx.getText(), node.LiteralType.STR)
        if self.left:
            print("left value")
            self.parent.setLeftChild(self.current)
        else:
            print("right value")
            self.parent.setRightChild(self.current)
        self.current.parent=self.parent

    def print_val(self,v):
        if isinstance(v,Value):
            return print(v.value)
        elif isinstance(v,BinaryOperator):
            return print(v.operator)
        else:
            return ""
    def enterExpr(self, ctx):
        print("enter expr:"+ctx.getText())
        if self.has_children(ctx):
            self.left=True
            if self.parent is None:
                print("parent is none")
                self.parent=BinaryOperator("")
                self.current = BinaryOperator("")
                self.current.parent = self.parent
                self.parent.setLeftChild(self.current)
                self.parent.setRightChild(self.current)
                """
                self.parent.setRightChild(Value("",node.LiteralType.STR))
                """
            elif self.right:
                print("right side")
                #if self.current is None:
                self.current=BinaryOperator(ctx.getText())
                self.current.parent=self.parent
                print("right child parent:", self.parent.getValue())
                self.parent.setRightChild(self.current)
                """
                    if self.parent.leftChild is None:
                        self.parent.setLeftChild(Value("",node.LiteralType.STR))
                """
                self.parent=self.current
                self.current=self.parent.leftChild
                self.right = False

            else:
                if self.current is None:
                    print("current is none")
                self.current=BinaryOperator(ctx.getText())
                self.current.parent=self.parent
                self.parent.setLeftChild(self.current)
                """
                if self.parent.rightChild is None:
                    self.parent.setRightChild(Value("",node.LiteralType.STR))
                """
                self.parent=self.current
                self.current=self.parent.leftChild
        else:
            print("no children")
            self.set_val(ctx)
            if self.left:
                self.need_token = True



    def exitExpr(self, ctx):
        print("exit expression is:" + ctx.getText())
        if self.has_children(ctx):
            #print("current:",self.current.getValue())
            print("parent:", self.parent.getValue())
            if self.parent.rightChild is None:
                self.parent.setRightChild(Value("",node.LiteralType.STR))
            print("lchild:",self.parent.leftChild.getValue())
            print("rchild:", self.parent.rightChild.getValue())
            self.current=self.current.parent
            self.parent=self.current.parent

    def enterDec(self, ctx):
        pass

    def enterBinop(self, ctx):
        #print("token is:"+ ctx.getText())
        if self.need_token:
            #print("need token")
            self.parent.operator= ctx.getText()
            self.current.parent=self.parent
            self.parent.setLeftChild(self.current)
            rchild=self.parent.getRightChild()
            if rchild is None:
                rchild=Value("",node.LiteralType.STR)
            rchild.parent=self.parent
            self.parent.setRightChild(rchild)
            self.current=self.parent.getRightChild()
            self.left=False
            self.right=True

from AST_.AST import *
from generated.input.ExpressionListener import *


def create_tree():
    expression_tree = AST()
    expression_tree.setRoot(None)
    return expression_tree

class Expression(ExpressionListener):
    def __init__(self):
        self.asT=create_tree()
        self.count=0
        self.nr=0
    def enterExpr(self, ctx):
        self.count+=1
        self.nr+=1
        print("enter expression is:" + ctx.getText())
        #print(ctx.getToken(int))
        if(ctx.binop()):
            print("val:"+ ctx.expr(0).getText()+ "op:" +ctx.binop().getText()+"val2:"+ctx.expr(1).getText() )
            node=BinaryOperator(ctx.binop().getText(),ctx.expr(0).getText(),ctx.expr(1).getText())
            node.setNumber(self.nr)
            node.setLevel(self.count)
            self.asT.setNodeIds(node)
    def exitExpr(self, ctx):
        self.count = 1
    def enterDec(self, ctx):
        print("enter declaration is: " +ctx.getText())
    def enterBinop(self, ctx):
        print("enter declaration is: " + ctx.getText())





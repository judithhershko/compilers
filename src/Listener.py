from generated.input.ExpressionListener import *

class Expression_(ExpressionListener):
    def enterExpr(self, ctx):
        print("expression is:" + ctx.getText())
    def exitExpr(self, ctx):
        pass





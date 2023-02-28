from generated.input.ExpressionVisitor import *

nr_levels = 0


# replace with result for optimisation
class EvalVisitor(ExpressionVisitor):
    """
    def visitExpr(self, ctx):
        left = self.visitChildren(ctx.expr(0))
        right = self.visitChildren(ctx.expr(1))
        op = ctx.getRuleContext().getText()

        #op='+'
        if op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '+':
            return left + right
        elif op == '-':
            return left - right
        else:
            raise Exception("Unknown operator :"+op)
"""

"""    
    def visitStart_rule(self, ctx):
        return self.visitChildren(ctx.expr())

    def visitDec(self, ctx):
        return self.visitChildren(ctx.getText())
"""
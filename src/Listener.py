from .ast.AST import *
from generated.input.ExpressionListener import *
from .ast.node import Value, BinaryOperator
from src.HelperFunctions import *


class Expression(ExpressionListener):
    def __init__(self):
        self.asT = create_tree()
        self.current = None
        self.parent = None
        self.need_token = False
        self.trees = []
        self.declarations=[]
        self.left = True
        self.right = False
        self.declaration = False

    def has_children(self, ctx: ParserRuleContext):
        return ctx.getChildCount() > 1

    def enterTyped_var(self, ctx: ParserRuleContext):
        if not self.declaration:
            return
        self.parent.leftChild.setType(find_type(ctx.getText()))
        v = self.parent.leftChild.getValue()
        v = v[len(ctx.getText()):]

        # self.parent.leftChild.setValue(separate_type_variable(self.parent.leftChild.getValue(),ctx.getText()))
        self.parent.leftChild.setValue(v)
        self.declaration = False

    def set_val(self, ctx: ParserRuleContext):
        print("set val:"+ctx.getText())
        type_ = find_value_type(ctx.getText())
        #print("val type")
        #print(type_)
        self.current = Value(ctx.getText(), type_, self.parent)
        self.current.parent=self.parent
        if self.left and not self.right:
            print("left")
            self.parent.setLeftChild(self.current)
            self.right = True
        else:
            print("right")
            self.parent.setRightChild(self.current)
            self.right = False
        self.current.parent = self.parent
        if self.left:
            self.need_token = True

    def set_operatipon(self,operation):
        if self.parent is not None and self.parent.parent:
            self.parent.operator=operation
        else:
            p=BinaryOperator(operation)
            p.leftChild=self.parent
            self.parent=p
            self.current=self.parent.rightChild
            self.right=True
        """
        self.current=BinaryOperator(operation,self.parent)
        self.parent.leftChild(self.current)
        self.parent=self.current
        self.current=self.parent.leftChild
        """
    def set_expression(self,ctx:ParserRuleContext):
        #if self.has_children(ctx):
        self.left = True
        if self.parent is None:
            self.parent = BinaryOperator("")
            self.current = BinaryOperator("", self.parent)
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
            #self.current.parent = self.parent
            self.parent.setLeftChild(self.current)
            self.parent = self.current
            self.current = self.parent.leftChild
    def enterExpr(self, ctx):
        print("enter expr:"+ctx.getText())
        return self.set_expression(ctx)


    def exitExpr(self, ctx):
        # print("exit expr:"+ctx.getText())
        return self.move_up(ctx)

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
        self.declaration = True

    def exitDec(self, ctx):
        #print("exit declaration:" + ctx.getText())
        f = True
        """
        while f:
            if isinstance(self.current, BinaryOperator) and self.current.operator == "=":
                f = False
            else:
                self.current = self.current.parent
        """
        while self.parent is not None:
            self.current = self.parent
            self.parent = self.current.parent
        #print("current:")
        if isinstance(self.current, BinaryOperator) or isinstance(self.current,Declaration):
            #print(self.current.leftChild.getValue())
            pass

        self.asT.setRoot(self.current)
        self.trees.append(self.asT)
        self.parent = None
        self.current = None
        self.asT = create_tree()
    def enterOr_and(self, ctx):
        print("or and/"+ctx.getText())
        self.set_operatipon(ctx.getText())
    def enterBinop(self, ctx):
        print("bin op:"+ctx.getText() )
        #return self.set_token(ctx)
        #self.set_expression(ctx)
        self.set_operatipon(ctx.getText())
    def enterEquality(self, ctx):
        #print("equality"+ctx.getText())
        #self.set_expression(ctx)
        print("equal:"+ctx.getText())
        self.set_operatipon(ctx.getText())
    def enterComparator(self, ctx):
        #self.set_expression(ctx)
        print("comparator:"+ctx.getText())
        self.set_operatipon(ctx.getText())
    # Enter a parse tree produced by ExpressionParser#binop_md.
    def set_token(self, ctx):
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
        print("op mult and div"+ctx.getText())
        #self.set_expression(ctx)
        self.set_operatipon(ctx.getText())
        #self.set_expression(ctx)
        #return self.set_token(ctx)

    # Exit a parse tree produced by ExpressionParser#binop_md.
    def exitBinop_md(self, ctx):
        pass

    def enterCterm(self, ctx: ParserRuleContext):
        #print("ctermexpr:"+ctx.getText())
        #self.set_exptr(ctx)
        pass
    def exitCterm(self, ctx):
        #print("xit cterm")
        #self.move_up(ctx)
        pass
    def enterTerm(self, ctx: ParserRuleContext):
        #print("term:"+ctx.getText())
        #self.set_exptr(ctx)
        pass

    # Exit a parse tree produced by ExpressionParser#term.
    def exitTerm(self, ctx: ParserRuleContext):
        #print("exit term:" + ctx.getText())
        #self.move_up(ctx)
        pass
    # Enter a parse tree produced by ExpressionParser#term_1.
    def enterTerm_1(self, ctx: ParserRuleContext):
        #print("term1:"+ctx.getText())
        #self.set_exptr(ctx)
        pass

    # Exit a parse tree produced by ExpressionParser#term_1.
    def exitTerm_1(self, ctx: ParserRuleContext):
        #print("exit term 1:" + ctx.getText())
        #self.move_up(ctx)
        pass


    # Enter a parse tree produced by ExpressionParser#term_2.
    def enterTerm_2(self, ctx: ParserRuleContext):
        #print("term2"+ctx.getText())
        #self.set_exptr(ctx)
        pass

    # Exit a parse tree produced by ExpressionParser#term_2.
    def exitTerm_2(self, ctx: ParserRuleContext):
        #print("exit term 2:" + ctx.getText())
        #self.move_up(ctx)
        pass

    # Enter a parse tree produced by ExpressionParser#term_3.
    def enterTerm_3(self, ctx: ParserRuleContext):
        #print("term3"+ctx.getText())
        #self.set_exptr(ctx)
        pass

    # Exit a parse tree produced by ExpressionParser#term_3.
    def exitTerm_3(self, ctx: ParserRuleContext):
        #print("exit term 3:" + ctx.getText())
        #self.move_up(ctx)
        pass


    # Enter a parse tree produced by ExpressionParser#term_4.
    def enterTerm_4(self, ctx: ParserRuleContext):
        #print("term4" + ctx.getText())
        #self.set_exptr(ctx)
        pass

    # Exit a parse tree produced by ExpressionParser#term_4.
    def exitTerm_4(self, ctx: ParserRuleContext):
        #print("exit term 4:" + ctx.getText())
        #self.move_up(ctx)
        pass


    # Enter a parse tree produced by ExpressionParser#term_5.
    def enterTerm_5(self, ctx: ParserRuleContext):
        #print("term5" + ctx.getText())
        #self.set_exptr(ctx)
        pass

    # Exit a parse tree produced by ExpressionParser#term_5.
    def exitTerm_5(self, ctx: ParserRuleContext):
        #print("exit term 5:" + ctx.getText())
        #self.move_up(ctx)
        pass


    # Enter a parse tree produced by ExpressionParser#term_6.
    def enterTerm_6(self, ctx: ParserRuleContext):
        #print("term6" + ctx.getText())
        #self.set_exptr(ctx)
        pass

    # Exit a parse tree produced by ExpressionParser#term_6.
    def exitTerm_6(self, ctx: ParserRuleContext):
        #print("exit term 6:" + ctx.getText())
        #self.move_up(ctx)
        pass


    # Enter a parse tree produced by ExpressionParser#term_7.
    def enterTerm_7(self, ctx: ParserRuleContext):
        #print("term7" + ctx.getText())
        #self.set_exptr(ctx)
        pass

    # Exit a parse tree produced by ExpressionParser#term_7.
    def exitTerm_7(self, ctx: ParserRuleContext):
        #print("exit term 7:"+ctx.getText())
        #self.move_up(ctx)
        pass
    def enterPri(self, ctx: ParserRuleContext):
        return self.set_val(ctx)

    # Exit a parse tree produced by ExpressionParser#pri.
    def exitPri(self, ctx: ParserRuleContext):
        # print("exit pri:"+ctx.getText())
        pass

    def set_exptr(self, ctx: ParserRuleContext):
        #print("enter expr:"+ctx.getText())
        if self.has_children(ctx):
            self.left = True
            if self.parent is None:
                self.parent = BinaryOperator("")
                self.current = BinaryOperator("", self.parent)
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
            return

    def move_up(self, ctx: ParserRuleContext):
        if self.has_children(ctx):
            #print("has children")
            if self.parent.rightChild is None:
                self.parent.setRightChild(Value("", node.LiteralType.STR))
            self.current = self.current.parent
            self.parent = self.current.parent

    def enterConst(self, ctx: ParserRuleContext):
        print("const:"+ctx.getText())
        if isinstance(self.parent, BinaryOperator) or isinstance(self.parent, LogicalOperator):
            self.parent.leftChild.const = True
            self.parent.leftChild.setValue(self.parent.leftChild.getValue()[5:])

    def enterPointer(self, ctx: ParserRuleContext):
        #print("enter pointer:" + ctx.getText())
        pass

    def enterPointer_variable(self, ctx: ParserRuleContext):
        #print("pointer var:" + ctx.getText())
        pass

    def enterChar_pri(self, ctx: ParserRuleContext):
        #print("enter char op:" + ctx.getText())
        self.set_val(ctx)

    def enterChar_expr(self, ctx: ParserRuleContext):
        return self.set_expression(ctx)
    def enterChar_op(self, ctx: ParserRuleContext):
        return self.set_token(ctx)

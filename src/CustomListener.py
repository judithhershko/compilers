from generated.input.ExpressionListener import *
from src.HelperFunctions import *
from .ast.Program import *
from .ast.block import *


class CustomListener(ExpressionListener):
    def __init__(self):
        self.hierarchy = None
        self.asT = create_tree()
        self.current = None
        self.parent = None
        self.trees = []
        self.left = True
        self.right = False
        self.declaration = False
        self.dec_op = None
        self.is_char = False
        self.counter = 0
        self.program = Program.program()
        self.c_block = block(None)
        self.line_nr = 0
        self.comments = []
        self.print = False
        self.line=0

    def descend(self, operator: BinaryOperator):
        operator.parent = self.parent
        operator.leftChild = self.parent.rightChild
        self.parent.rightChild = operator

    def has_children(self, ctx: ParserRuleContext):
        return ctx.getChildCount() > 1

    def set_val(self, ctx: ParserRuleContext):

        print("set val:" + ctx.getText())
        type_ = find_value_type(ctx.getText())
        self.current = Value(ctx.getText(), type_, self.parent)
        if type_ == LiteralType.NUM:
            if isFloat(ctx.getText()):
                self.current = Value(float(ctx.getText()), type_, self.parent)
            else:
                self.current = Value(int(ctx.getText()), type_, self.parent)

        if self.print:
            val = self.current.getValue()
            if self.current.type == LiteralType.VAR:
                val = self.c_block.getSymbolTable().findSymbol(self.current.getValue())
            p = Print(val)
            self.asT = create_tree()
            self.asT.setRoot(p)
            self.c_block.trees.append(self.asT)
            self.asT = create_tree()
            return
        if self.right:
            print("right")
            self.parent.setRightChild(self.current)
            self.right = False
            self.left = True
        elif self.left:
            print("left")
            self.parent.setLeftChild(self.current)
            self.right = True

    def set_operation(self, operation):
        print("set operation")
        if self.parent is not None and self.parent.parent:
            self.parent.operator = operation
        else:
            p = BinaryOperator(operation)
            p.leftChild = self.parent
            self.parent = p
            self.current = self.parent.rightChild
            self.right = True

    def set_expression(self, ctx: ParserRuleContext):
        if self.declaration and isinstance(self.parent, Declaration):
            self.dec_op = self.parent
            self.parent = BinaryOperator("")
            self.current = self.parent.leftChild
            self.left = True
            self.right = False
        elif self.parent is None:
            self.line_nr += 1
            self.parent = BinaryOperator("")
            self.left = True
            self.right = False

    def set_token(self, ctx, Operator=None):
        if isinstance(Operator, LogicalOperator):
            self.hierarchy = True
        if Operator is not None:
            operator = Operator
        else:
            operator = BinaryOperator(ctx.getText())
        if self.hierarchy and not isinstance(operator, LogicalOperator):
            if isinstance(self.parent, LogicalOperator):
                r = self.parent.rightChild
                r.parent = operator
                operator.parent = self.parent
                operator.leftChild = r
                self.parent.rightChild = operator
            else:
                if order(self.parent.operator)<order(operator.operator):
                    t = self.parent
                    operator.parent = self.parent.parent
                    self.parent.parent.rightChild = operator
                    t.parent = operator
                    operator.leftChild = t
                else:
                    operator.parent=self.parent
                    operator.leftChild=self.parent.rightChild
                    self.parent.rightChild=operator



        elif self.parent is not None and not isinstance(self.parent, Declaration) and self.parent.operator == "":
            self.current.parent = operator
            operator.leftChild = self.current
        else:
            if order(self.parent.operator) > order(operator.operator):
                self.descend(operator)
            else:
                operator.leftChild = self.parent

        self.parent = operator
        self.current = self.parent.rightChild
        self.right = True
        self.left = False

    ########################################################################
    # Enter a parse tree produced by ExpressionParser#start_rule.
    def enterStart_rule(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#start_rule.
    def exitStart_rule(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#print.
    def enterPrint(self, ctx: ParserRuleContext):
        print("enter print:" + ctx.getText())
        self.print = True

    # Exit a parse tree produced by ExpressionParser#print.
    def exitPrint(self, ctx: ParserRuleContext):
        self.print = False

    # Enter a parse tree produced by ExpressionParser#typed_var.
    def enterTyped_var(self, ctx: ParserRuleContext):
        self.parent.leftChild.setType(find_type(ctx.getText()))
        v = self.parent.leftChild.getValue()
        v = v[len(ctx.getText()):]
        self.parent.leftChild.setValue(v)

    # Exit a parse tree produced by ExpressionParser#typed_var.
    def exitTyped_var(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#const.
    def enterConst(self, ctx: ParserRuleContext):
        print("const:" + ctx.getText())
        if isinstance(self.parent, Declaration):
            self.parent.leftChild.const = True
            self.parent.leftChild.setValue(self.parent.leftChild.getValue()[5:])

    # Exit a parse tree produced by ExpressionParser#const.
    def exitConst(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#pointer_variable.
    def enterPointer_variable(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#pointer_variable.
    def exitPointer_variable(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#pointer.
    def enterPointer(self, ctx: ParserRuleContext):
        print("pointer is" + ctx.getText())
        self.dec_op.leftChild.nr_pointers += 1
        self.dec_op.leftChild.setValue(self.dec_op.leftChild.getValue()[1:])

    # Exit a parse tree produced by ExpressionParser#pointer.
    def exitPointer(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#to_pointer.
    def enterTo_pointer(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#to_pointer.
    def exitTo_pointer(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#to_reference.
    def enterTo_reference(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#to_reference.
    def exitTo_reference(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#dec.
    def enterDec(self, ctx: ParserRuleContext): #TODO: declaration needs to get right type
        print("enter dec")
        self.line_nr += 1
        self.asT = create_tree()
        self.parent = Declaration()
        var = getVariable(ctx.getText())
        type = getType(var)
        self.current = Value(var, type, self.parent, variable=True)
        self.parent.leftChild = self.current
        self.current = self.parent.rightChild
        self.dec_op = self.parent
        self.declaration = True

    # Exit a parse tree produced by ExpressionParser#dec.
    def exitDec(self, ctx: ParserRuleContext):
        print("exit dec")
        while self.current.parent is not None:
            print("current parent" + str(self.current.getValue()))
            self.current = self.current.parent
        if isinstance(self.current, BinaryOperator) and self.current.operator == "":
            print("parentop is """)
            self.current = self.current.leftChild
        print(isinstance(self.current, BinaryOperator))

        self.dec_op.rightChild = self.current
        self.current = self.dec_op
        self.asT.setRoot(self.current)
        self.trees.append(self.asT)
        self.asT.setNodeIds(self.asT.root)
        self.asT.generateDot("no_fold_expression_dot" + str(self.counter))
        self.asT.foldTree()
        self.asT.setNodeIds(self.asT.root)
        self.asT.generateDot("yes_fold_expression_dot" + str(self.counter))
        pointer = ""
        level = 0
        if self.asT.root.leftChild.nr_pointers > 0:
            pointer = "*"
            level = self.asT.root.leftChild.nr_pointers
        self.c_block.getSymbolTable().addSymbol(self.asT.root.leftChild.getValue(), self.asT.root.rightChild.getValue(),
                                                self.asT.root.leftChild.type, self.asT.root.leftChild.const,
                                                pointer, level)
        self.counter += 1
        self.parent = None
        self.current = None
        self.declaration = False
        self.asT = create_tree()

    # Enter a parse tree produced by ExpressionParser#variable_dec.
    def enterVariable_dec(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#variable_dec.
    def exitVariable_dec(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#binop.
    def enterBinop(self, ctx: ParserRuleContext):
        # self.set_operation(ctx.getText())
        print("bin op:" + ctx.getText())
        self.set_token(ctx)

    # Exit a parse tree produced by ExpressionParser#binop.
    def exitBinop(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#binop_md.
    def enterBinop_md(self, ctx: ParserRuleContext):
        # self.set_operation(ctx.getText())
        print("bin op md:" + ctx.getText())
        self.set_token(ctx)

    # Exit a parse tree produced by ExpressionParser#binop_md.
    def exitBinop_md(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#equality.
    def enterEquality(self, ctx: ParserRuleContext):
        # self.set_operation(ctx.getText())
        print("bin eq:" + ctx.getText())
        self.set_token(ctx, LogicalOperator(ctx.getText()))

    # Exit a parse tree produced by ExpressionParser#equality.
    def exitEquality(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#comparator.
    def enterComparator(self, ctx: ParserRuleContext):
        print("comparator:" + ctx.getText())
        # self.set_operation(ctx.getText())
        self.set_token(ctx, LogicalOperator(ctx.getText()))

    # Exit a parse tree produced by ExpressionParser#comparator.
    def exitComparator(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#or_and.
    def enterOr_and(self, ctx: ParserRuleContext):
        # self.set_operation(ctx.getText())
        print("or and:" + ctx.getText())
        self.set_token(ctx, LogicalOperator(ctx.getText()))

    # Exit a parse tree produced by ExpressionParser#or_and.
    def exitOr_and(self, ctx: ParserRuleContext):
        # self.set_operation(ctx.getText())
        # self.set_token(ctx)
        pass

    # Enter a parse tree produced by ExpressionParser#expr.
    def enterExpr(self, ctx: ParserRuleContext):
        print("enter expr:" + ctx.getText())
        return self.set_expression(ctx)

    # Exit a parse tree produced by ExpressionParser#expr.
    def exitExpr(self, ctx: ParserRuleContext):
        print("exit epr:" + ctx.getText())
        if not self.declaration:
            while self.current.parent is not None:
                self.current = self.current.parent
            self.asT.setRoot(self.current)
            self.c_block.trees.append(self.asT)
            self.trees.append(self.asT)
            self.asT.setNodeIds(self.asT.root)
            self.asT.generateDot("expression_dot" + str(self.counter))
            self.counter += 1
            self.parent = None
            self.current = None
            self.asT = create_tree()

    # Enter a parse tree produced by ExpressionParser#term_1.
    def enterTerm_1(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#term_1.
    def exitTerm_1(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#term_2.
    def enterTerm_2(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#term_2.
    def exitTerm_2(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#term_3.
    def enterTerm_3(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#term_3.
    def exitTerm_3(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#term_4.
    def enterTerm_4(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#term_4.
    def exitTerm_4(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#term_5.
    def enterTerm_5(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#term_5.
    def exitTerm_5(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#term_6.
    def enterTerm_6(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#term_6.
    def exitTerm_6(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#term_7.
    def enterTerm_7(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#term_7.
    def exitTerm_7(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#fac.
    def enterFac(self, ctx: ParserRuleContext):
        # self.set_operation(ctx.getText())
        # print("fac:" + ctx.getText())
        # self.set_token(ctx)
        pass

    # Exit a parse tree produced by ExpressionParser#fac.
    def exitFac(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#pri.
    def enterPri(self, ctx: ParserRuleContext):
        self.set_val(ctx)

    # Exit a parse tree produced by ExpressionParser#pri.
    def exitPri(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#char_op.
    def enterChar_op(self, ctx: ParserRuleContext):
        print("char token" + ctx.getText())
        self.set_token(ctx)

    # Exit a parse tree produced by ExpressionParser#char_op.
    def exitChar_op(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#char_expr.
    def enterChar_expr(self, ctx: ParserRuleContext):
        print("char expr:" + ctx.getText())
        self.is_char = True
        return self.set_expression(ctx)

    # Exit a parse tree produced by ExpressionParser#char_expr.
    def exitChar_expr(self, ctx: ParserRuleContext):
        self.is_char = False
        print("exit char expr:" + ctx.getText())

    # Enter a parse tree produced by ExpressionParser#char_pri.
    def enterChar_pri(self, ctx: ParserRuleContext):
        self.set_val(ctx)

    # Exit a parse tree produced by ExpressionParser#char_pri.
    def exitChar_pri(self, ctx: ParserRuleContext):
        pass

    def enterComments(self, ctx: ParserRuleContext):
        type = commentType(ctx.getText())
        comment = Comment(ctx.getText(), type)
        self.comments.append(comment)

    # Exit a parse tree produced by ExpressionParser#comments.
    def exitComments(self, ctx: ParserRuleContext):
        pass
    # Enter a parse tree produced by ExpressionParser#line.
    def enterLine(self, ctx: ParserRuleContext):
        print("new line:"+str(self.line))
        self.line+=1

    # Exit a parse tree produced by ExpressionParser#line.
    def exitLine(self, ctx: ParserRuleContext):
        pass

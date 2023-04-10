from generated.input.ExpressionListener import *
from src.HelperFunctions import *
from .ast.block import *


class CustomListener(ExpressionListener):
    def __init__(self, pathName):
        self.is_ref = False
        self.is_loop=False
        self.start_rule = None
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
        self.line = 1
        self.comments = []
        self.print = False
        self.expr_layer = 0
        self.bracket_stack = stack()
        self.bracket_layer = stack()
        self.bracket_count = 0
        self.bracket_start = None
        self.scope_stack = stack()
        self.scope_count = 0
        self.nr_pointers = 0
        self.ref_pointers = 0
        self.pointer = False
        self.end_bracket = False
        self.nr_expressions = 0
        self.pathName = pathName
        self.rhs_pointer = False
        self.loop = None

    def is_declaration(self, var: str):
        if var[:3] == "int" or var[:5] == "float" or var[:4] == "bool" or var[:5] == "const":
            return True
        else:
            return False

    def check_brackets(self, non_brack):
        if non_brack.leftChild is None:
            non_brack.leftChild = self.parent
            self.parent = non_brack
            return True
        elif non_brack.rightChild is None:
            non_brack.rightChild = self.parent
            self.parent = non_brack
            return True
        return False

    def set_bracket(self):
        if self.bracket_stack.__len__() == 0:
            return

        non_brack = self.bracket_stack.pop()
        layer = self.bracket_layer.pop()
        if non_brack is None:
            return
        if layer != self.bracket_count:
            self.bracket_layer.push(layer)
            self.bracket_stack.push(non_brack)
            return
        while self.parent.parent is not None:
            self.parent = self.parent.parent
        self.parent.parent = non_brack

        if not isinstance(non_brack, UnaryOperator) and non_brack.leftChild is None:
            non_brack.leftChild = self.parent
            self.parent = non_brack
        elif non_brack.rightChild is None:
            non_brack.rightChild = self.parent
            self.parent = non_brack
        else:
            while non_brack.rightChild is not None:
                non_brack = non_brack.rightChild
                self.parent.parent = non_brack
            non_brack.rightChild = self.parent
            self.parent = non_brack

    def descend(self, operator: BinaryOperator):
        operator.parent = self.parent
        operator.leftChild = self.parent.rightChild
        self.parent.rightChild = operator

    def has_children(self, ctx: ParserRuleContext):
        return ctx.getChildCount() > 1

    def set_print(self, ctx: ParserRuleContext, type_):
        if type_ == LiteralType.INT:
            self.current = Print(int(ctx.getText()))
        elif type_ == LiteralType.FLOAT:
            self.current = Print(float(ctx.getText()))
        elif type_ == LiteralType.STR:
            self.current = Print(ctx.getText())
        else:
            var = self.c_block.getSymbolTable().findSymbol(ctx.getText())
            self.current = Print(str(var))
        self.asT.root = self.current
        self.c_block.trees.append(self.asT)
        self.current = None
        self.asT = create_tree()
        return

    def set_pointer(self, ctx: ParserRuleContext, type_):
        self.line = ctx.start.line
        if self.dec_op.rightChild is None:
            self.dec_op.rightChild = Value(ctx.getText(), type_, self.dec_op, ctx.start.line, True)
        else:
            # print("former value:")
            # print(self.dec_op.rightChild.getValue())
            self.dec_op.rightChild.setValue(ctx.getText())

    def set_val(self, ctx: ParserRuleContext):
        print("set val:" + ctx.getText())
        self.line = ctx.start.line
        type_ = find_value_type(ctx.getText())
        v = ctx.getText()
        if self.print:
            return self.set_print(ctx, type_)
        if self.pointer:
            return self.set_pointer(ctx, type_)
        if type_ == LiteralType.VAR:
            var = True
        else:
            var = False
        self.current = Value(ctx.getText(), type_, ctx.start.line, self.parent, variable=var)
        if type_ == LiteralType.INT:
            self.current = Value(int(ctx.getText()), type_, ctx.start.line, self.parent)
        elif type_ == LiteralType.FLOAT:
            self.current = Value(float(ctx.getText()), type_, ctx.start.line, self.parent)
        elif type_ == LiteralType.DOUBLE:
            self.current = Value(float(ctx.getText()), type_, ctx.start.line, self.parent)
        elif type_ == LiteralType.CHAR:
            if len(ctx.getText()) > 3:
                raise CharSize(ctx.getText(), ctx.start.line)

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
        if self.right or (self.parent.rightChild is None and self.parent.leftChild is not None):
            self.parent.setRightChild(self.current)
            self.right = False
            self.left = True
        elif self.left:
            self.parent.setLeftChild(self.current)
            self.right = True

    def set_operation(self, operation):
        if self.parent is not None and self.parent.parent:
            self.parent.operator = operation
        else:
            p = BinaryOperator(operation, self.line)
            p.leftChild = self.parent
            self.parent = p
            self.current = self.parent.rightChild
            self.right = True

    def set_expression(self, ctx: ParserRuleContext):
        self.expr_layer += 1
        print("expression :" + ctx.getText() + "with layer:" + str(self.expr_layer))
        self.line = ctx.start.line
        if self.declaration and isinstance(self.parent, Declaration):
            self.dec_op = self.parent
            self.parent = BinaryOperator("", ctx.start.line)
            self.current = self.parent.leftChild
            self.left = True
            self.right = False
        elif self.parent is None:
            self.parent = BinaryOperator("", ctx.start.line)
            self.left = True
            self.right = False

    def set_token(self, ctx, operator=None):
        self.line = ctx.start.line
        if operator is None:
            operator = BinaryOperator(ctx.getText(), self.line)
        if self.parent is not None and not isinstance(self.parent, Declaration) and self.parent.operator == "":
            if isinstance(operator, UnaryOperator):
                self.parent = operator
                self.right = True
                self.left = False
                return
            self.current.parent = operator
            if not isinstance(operator, UnaryOperator):
                operator.leftChild = self.current
            self.parent = operator
        elif self.parent.operator == "":
            lc = self.parent.leftChild
            lc.parent = operator
            operator.leftChild = self.parent.leftChild
            self.parent = operator
        elif self.end_bracket:
            while self.parent.parent is not None:
                self.parent = self.parent.parent
            self.parent.parent = operator
            operator.leftChild = self.parent
            self.parent = operator
            self.end_bracket = False
            self.right = True
            self.left = False

        else:
            while order_prec[operator.operator] >= order_prec[self.parent.operator] and self.parent.parent is not None:
                self.parent = self.parent.parent
            # is operator >parent.op?
            if order_prec[operator.operator] > order_prec[self.parent.operator]:
                # has parents
                if self.parent.parent is None:

                    if self.current is not None and self.parent.rightChild is None:
                        self.current.parent = self.parent
                        self.parent.rightChild = self.current
                    self.parent.parent = operator
                    operator.leftChild = self.parent
                    self.parent = operator
                else:
                    # doesn't have parents
                    pp = self.parent.parent
                    self.parent.parent = operator
                    operator.leftChild = self.parent
                    operator.parent = pp
                    pp.rightChild = operator
                    # parent op> operator op
            elif order_prec[operator.operator] < order_prec[self.parent.operator]:
                # richtchild none
                if self.parent.rightChild is None:
                    operator.parent = self.parent
                    self.current.parent = operator
                    operator.leftChild = self.current
                    self.parent.rightChild = operator
                    self.parent = operator
                # richtchild needs to be reattached
                else:
                    rc = self.parent.rightChild
                    rc.parent = operator
                    operator.leftChild = rc
                    operator.parent = self.parent
                    self.parent.rightChild = operator
                    self.parent = operator
            # parent op==operator op
            elif order_prec[self.parent.operator] == order_prec[operator.operator]:
                # parent is None:
                if self.parent.parent is None:
                    if self.parent.rightChild is None:
                        self.current.parent = self.parent
                        self.parent.rightChild = self.current
                    self.parent.parent = operator
                    operator.leftChild = self.parent
                    self.parent = operator
                else:
                    rc = self.parent.parent.rightChild
                    rc.parent = operator
                    operator.parent = self.parent.parent
                    operator.leftChild = rc
                    self.parent.parent.rightChild = operator
                    self.parent = operator
            self.right = True
            self.left = False

    ########################################################################
    # Enter a parse tree produced by ExpressionParser#start_rule.
    def enterStart_rule(self, ctx: ParserRuleContext):
        self.start_rule = ctx.getText()

    # Exit a parse tree produced by ExpressionParser#start_rule.
    def exitStart_rule(self, ctx: ParserRuleContext):
        if self.c_block.trees is not None:
            self.program.blocks.append(self.c_block)
            self.c_block = block(None)

    # Enter a parse tree produced by ExpressionParser#print.
    def enterPrint(self, ctx: ParserRuleContext):
        self.print = True

    # Exit a parse tree produced by ExpressionParser#print.
    def exitPrint(self, ctx: ParserRuleContext):
        self.print = False

    # Enter a parse tree produced by ExpressionParser#typed_var.
    def enterTyped_var(self, ctx: ParserRuleContext):
        self.parent.leftChild.type = getType(ctx.getText())
        v = self.parent.leftChild.getValue()
        v = v[len(ctx.getText()):]
        self.parent.leftChild.setValue(v)
        self.parent.leftChild.declaration = True

    # Exit a parse tree produced by ExpressionParser#typed_var.
    def exitTyped_var(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#const.
    def enterConst(self, ctx: ParserRuleContext):
        if isinstance(self.parent, Declaration):
            self.parent.leftChild.const = True
            self.parent.leftChild.setValue(self.parent.leftChild.getValue()[5:])
            type_ = getType(self.parent.leftChild.getValue())
            self.parent.leftChild.setType(type_)

    # Exit a parse tree produced by ExpressionParser#const.
    def exitConst(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#pointer_variable.
    def enterPointer_variable(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#pointer_variable.
    def exitPointer_variable(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#pointer_val.
    def enterPointer_val(self, ctx: ParserRuleContext):
        self.rhs_pointer = True
        pval = ctx.getText()
        while len(pval) > 0 and pval[0] == '*':
            pval = pval[1:]
        val = self.c_block.getSymbolTable().findSymbol(pval)
        cval = ''
        if val[1] == LiteralType.INT:
            cval = int(val[0])
        elif val[1] == LiteralType.FLOAT:
            cval = float(val[0])
        self.current = Value(cval, val[1], self.line, self.parent)
        self.parent.rightChild = self.current

    # Exit a parse tree produced by ExpressionParser#pointer_val.
    def exitPointer_val(self, ctx: ParserRuleContext):
        # print("exit pointer val")
        self.rhs_pointer = False

    # Enter a parse tree produced by ExpressionParser#pointer.
    def enterPointer(self, ctx: ParserRuleContext):
        self.line = ctx.start.line
        if self.rhs_pointer:
            return
        self.nr_pointers += 1
        self.dec_op.leftChild.setValue(self.dec_op.leftChild.getValue()[1:])
        if isinstance(self.dec_op.leftChild, Pointer):
            self.dec_op.leftChild.setPointerLevel(self.nr_pointers)
        else:
            pointer = Pointer(self.dec_op.leftChild.getValue(), self.dec_op.leftChild.getType(), self.line,
                              self.nr_pointers, self.dec_op, self.dec_op.leftChild.const,
                              self.dec_op.leftChild.declaration)
            self.dec_op.leftChild = pointer

    # Exit a parse tree produced by ExpressionParser#pointer.
    def exitPointer(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#ref.
    def enterRef(self, ctx: ParserRuleContext):
        # print("ref is :" + ctx.getText())
        self.dec_op.leftChild.setValue(self.dec_op.leftChild.getValue()[1:])

    # Exit a parse tree produced by ExpressionParser#ref.
    def exitRef(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#pointer_ref.
    def enterPointer_ref(self, ctx: ParserRuleContext):
        self.ref_pointers += 1
        # print("pointer rightside:" + ctx.getText())

    # Exit a parse tree produced by ExpressionParser#pointer_ref.
    def exitPointer_ref(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#ref_ref.
    def enterRef_ref(self, ctx: ParserRuleContext):
        self.ref_pointers += 1
        self.line = ctx.start.line
        var = ctx.getText()
        is_ref = False
        if var[0] == "&":
            var = var[1:]
            self.is_ref = True
        ref = self.c_block.getSymbolTable().findSymbol(var)
        # print(self.nr_pointers)
        if isinstance(self.dec_op.leftChild,
                      Pointer) and self.is_ref and self.nr_pointers > 0 and not self.dec_op.leftChild.declaration:
            raise PointerError(self.dec_op.leftChild.getValue(), self.line)
        if isinstance(self.dec_op.leftChild,
                      Pointer) and not self.is_ref and self.nr_pointers == 0 and not self.dec_op.leftChild.declaration:
            raise PointerError(self.dec_op.leftChild.getValue(), self.line)
        try:
            if not ref:
                raise NotDeclared(var, self.line)
            else:
                # self.parent.rightChild=Value(var,self.c_block.getSymbolTable().findSymbol(var)[1],self.line,self.parent,variable=True)
                self.parent.rightChild = Value(var, ref[1], self.line, self.parent, variable=True)
                self.current = self.parent.rightChild
                return

        except NotDeclared:
            raise

    # Exit a parse tree produced by ExpressionParser#ref_ref.
    def exitRef_ref(self, ctx: ParserRuleContext):
        self.is_ref = False

    # Enter a parse tree produced by ExpressionParser#dec.
    def enterDec(self, ctx: ParserRuleContext):  # TODO: declaration needs to get right type
        print("ente dec:" + ctx.getText())
        self.line = ctx.start.line
        # print("new dec:" + ctx.getText())
        # print("line is:" + str(self.line))
        self.start_rule = self.start_rule[len(ctx.getText()) + 1:]
        self.asT = create_tree()
        # self.parent = Declaration()
        var = getVariable(ctx.getText())

        if var == '':
            if str(self.start_rule[-1]).isdigit():
                raise RightValRef(self.line)
            else:
                raise ReservedWord(self.line, variable=var)
            pass

        type = getType(var)
        if type is False:
            # print("val is :" + var)
            if self.c_block.getSymbolTable().findSymbol(var) is not None:
                if self.c_block.getSymbolTable().findSymbol(var)[2] >= 1:
                    self.current = Pointer(var, self.c_block.getSymbolTable().findSymbol(var)[1], self.line,
                                           self.c_block.getSymbolTable().findSymbol(var)[2], self.parent)
                else:
                    self.current = Value(var, self.c_block.getSymbolTable().findSymbol(var)[1], self.line, self.parent,
                                         variable=True)
            #    raise Redefinition(self.line, variable=var)
            else:
                self.current = Value(var, LiteralType.FLOAT, self.line, self.parent, variable=True, decl=False)


        else:
            self.current = Value(var, type, self.line, self.parent, variable=True, decl=True)
        # self.parent.leftChild = self.current
        self.parent = Declaration(self.current, self.line)
        self.current = self.parent.rightChild
        self.dec_op = self.parent
        self.declaration = True

    # Exit a parse tree produced by ExpressionParser#dec.
    def exitDec(self, ctx: ParserRuleContext):
        print("exit dec:"+ctx.getText())
        """
        TODO:
        eerst fill literals
        fold
        add to symboltable
        :param ctx:
        :return:
        """
        self.line = ctx.start.line
        if self.bracket_stack.__len__() > 0:
            self.set_bracket()
        if not isinstance(self.parent, UnaryOperator) and isinstance(self.parent.leftChild, Pointer):
            self.dec_op.rightChild = self.parent.rightChild
            if self.dec_op.rightChild is None:
                self.dec_op.rightChild = EmptyNode(self.line, self.dec_op, self.dec_op.leftChild.getType())
        elif self.current is None:
            self.dec_op.rightChild = Value(0, self.dec_op.leftChild.getType(), self.dec_op, self.line, False)

        else:
            while self.current.parent is not None:
                self.current = self.current.parent
            if isinstance(self.current, BinaryOperator) and self.current.operator == "":
                self.current = self.current.leftChild
            if isinstance(self.current, Declaration):
                self.dec_op.rightChild = self.current.rightChild
            else:
                self.dec_op.rightChild = self.current
        self.current = self.dec_op
        """
        get the correct type from table if redeclaration
        """
        if self.c_block.getSymbolTable().findSymbol(self.current.leftChild.getValue()) is not None:
            self.current.leftChild.setType(
                self.c_block.getSymbolTable().findSymbol(self.current.leftChild.getValue())[1])
        self.asT.setRoot(self.current)
        if isinstance(self.asT.root.leftChild, Pointer):
            self.asT.root.leftChild.setLevel(self.nr_pointers)
            self.nr_pointers = 0

        self.asT.setNodeIds(self.asT.root)
        self.asT.generateDot(self.pathName + str(self.counter) + ".dot")
        #todo : dont fill if block needs info previous block
        if self.is_loop:
            if isinstance(self.loop,For) and self.loop.f_dec is None:
                self.loop.f_dec=self.asT
            elif isinstance(self.loop,For) and self.loop.f_incr is None:
                self.loop.f_incr = self.asT
            else:
                self.c_block.trees.append(self.asT)
            self.counter += 1
            self.parent = None
            self.current = None
            self.declaration = False
            self.asT = create_tree()
            return

        if not isinstance(self.asT.root.leftChild, Pointer):
            self.c_block.fillLiterals(self.asT)
        self.asT.foldTree()
        self.asT.setNodeIds(self.asT.root)
        self.asT.generateDot(self.pathName + str(self.counter) + ".dot")
        self.trees.append(self.asT)
        self.asT.foldTree()
        self.asT.setNodeIds(self.asT.root)

        self.asT.generateDot(self.pathName + str(self.counter) + ".dot")
        pointer = ""
        level = 0
        self.c_block.trees.append(self.asT)
        # if self.current.leftChild.declaration:
        self.c_block.getSymbolTable().addSymbol(self.asT.root, False)  # TODO: make bool depend on current scope
        # else:
        #    #TODO: replace value
        #    pass
        # self.c_block.getSymbolTable().findSymbol(self.current.leftChild.getValue())
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
        self.set_token(ctx)

    # Exit a parse tree produced by ExpressionParser#binop.
    def exitBinop(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#binop_md.
    def enterBinop_md(self, ctx: ParserRuleContext):
        # self.set_operation(ctx.getText())
        self.set_token(ctx)

    # Exit a parse tree produced by ExpressionParser#binop_md.
    def exitBinop_md(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#equality.
    def enterEquality(self, ctx: ParserRuleContext):
        # self.set_operation(ctx.getText())
        self.set_token(ctx, LogicalOperator(ctx.getText()))

    # Exit a parse tree produced by ExpressionParser#equality.
    def exitEquality(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#comparator.
    def enterComparator(self, ctx: ParserRuleContext):
        # self.set_operation(ctx.getText())
        self.set_token(ctx, LogicalOperator(ctx.getText()))

    # Exit a parse tree produced by ExpressionParser#comparator.
    def exitComparator(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#or_and.
    def enterOr_and(self, ctx: ParserRuleContext):
        # self.set_operation(ctx.getText())
        self.set_token(ctx, LogicalOperator(ctx.getText()))

    # Exit a parse tree produced by ExpressionParser#or_and.
    def exitOr_and(self, ctx: ParserRuleContext):
        # self.set_operation(ctx.getText())
        # self.set_token(ctx)
        pass

    # Enter a parse tree produced by ExpressionParser#expr.
    def enterExpr(self,
                  ctx: ParserRuleContext):  # TODO: start contains line and column values of where the token is located in the original code
        self.line = ctx.start.line
        # print("enter expr:" + ctx.getText())
        return self.set_expression(ctx)

    # Exit a parse tree produced by ExpressionParser#expr.
    def exitExpr(self, ctx: ParserRuleContext):
        self.expr_layer -= 1
        print("exit expression:" + ctx.getText() + "with layer " + str(self.expr_layer))
        """
        if (isinstance(self.loop, While) or isinstance(self.loop,For)) and self.loop.Condition is None and self.expr_layer == 0:
            while self.current.parent is not None:
                self.current = self.current.parent
            self.loop.Condition = self.current
            self.current = None
            self.parent = None
        """
        # (isinstance(self.loop, While) and self.loop.c_block is None and self.expr_layer==2)
        if self.declaration is False and isinstance(self.loop,For) and self.expr_layer == 0 and self.loop.Condition is None and self.loop.f_dec is not None:
            self.loop.Condition = self.parent
        elif not self.declaration and isinstance(self.loop,For) and self.expr_layer == 0 and self.loop.Condition is not None and self.loop.f_dec is not None and self.loop.f_incr is None:
            self.loop.f_incr = self.parent
        elif not self.declaration and self.expr_layer == 0:
            self.set_bracket()
            while self.current.parent is not None:
                self.current = self.current.parent
            self.asT.setRoot(self.current)
            if self.is_loop and self.loop.Condition is None:
                self.loop.Condition=self.asT
                print("fill condition")
            else:
                # self.c_block.trees.append(self.asT)
                self.trees.append(self.asT)
                self.asT.setNodeIds(self.asT.root)
                self.asT.generateDot(self.pathName + str(self.counter) + ".dot")
                self.c_block.fillLiterals(self.asT)
                self.asT.foldTree()
                self.asT.setNodeIds(self.asT.root)
                self.asT.generateDot(self.pathName + str(self.counter) + ".dot")
                self.c_block.trees.append(self.asT)
            self.counter += 1
            self.parent = None
            self.current = None
            self.asT = create_tree()

    # Enter a parse tree produced by ExpressionParser#pri.
    def enterPri(self, ctx: ParserRuleContext):
        self.set_val(ctx)

    # Exit a parse tree produced by ExpressionParser#pri.
    def exitPri(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#char_op.
    def enterChar_op(self, ctx: ParserRuleContext):
        self.set_token(ctx)

    # Exit a parse tree produced by ExpressionParser#char_op.
    def exitChar_op(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#char_expr.
    def enterChar_expr(self, ctx: ParserRuleContext):
        self.is_char = True
        return self.set_expression(ctx)

    # Exit a parse tree produced by ExpressionParser#char_expr.
    def exitChar_expr(self, ctx: ParserRuleContext):
        self.is_char = False

    # Enter a parse tree produced by ExpressionParser#char_pri.
    def enterChar_pri(self, ctx: ParserRuleContext):
        self.set_val(ctx)

    # Exit a parse tree produced by ExpressionParser#char_pri.
    def exitChar_pri(self, ctx: ParserRuleContext):
        pass

    def enterComments(self, ctx: ParserRuleContext):
        # print("comment detected")
        type = commentType(ctx.getText())
        self.line += 1
        if type == CommentType.ML:
            # print("muti line comment detected")
            for i in ctx.getText():
                if i == "\n":
                    self.line += 1

        comment = Comment(ctx.getText(), type)
        self.asT = create_tree()
        self.asT.root = comment
        self.comments.append(comment)
        self.c_block.trees.append(self.asT)
        self.asT = create_tree()

    # Exit a parse tree produced by ExpressionParser#comments.
    def exitComments(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#line.
    def enterLine(self, ctx: ParserRuleContext):
        # print("new line:" + str(self.line))
        self.line += 1

    # Exit a parse tree produced by ExpressionParser#line.
    def exitLine(self, ctx: ParserRuleContext):
        pass

    def enterBrackets(self, ctx: ParserRuleContext):
        self.bracket_count += 1
        # print("enter brackets: " + ctx.getText())
        # print("layer:" + str(self.bracket_count))
        if self.parent is None or self.parent.operator == "":
            return
        while self.parent.parent is not None:
            self.parent = self.parent.parent
        else:
            self.bracket_stack.push(self.parent)
            self.bracket_layer.push(self.bracket_count)
        self.parent = None
        self.current = None

    # Exit a parse tree produced by ExpressionParser#brackets.
    def exitBrackets(self, ctx: ParserRuleContext):
        # print("exit brackets: " + ctx.getText())
        # print("layer:" + str(self.bracket_count))
        if self.bracket_stack.__len__() == 0:
            self.end_bracket = True
            return
        self.set_bracket()
        self.bracket_count -= 1
        return

    # Enter a parse tree produced by ExpressionParser#prefix_op.
    def enterPrefix_op(self, ctx: ParserRuleContext):
        # print("prefix token:" + ctx.getText())
        self.line = ctx.start.line
        op = UnaryOperator(ctx.getText(), None, self.line)
        return self.set_token(ctx, op)

    # Exit a parse tree produced by ExpressionParser#prefix_op.
    def exitPrefix_op(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#suffix_op.
    def enterSuffix_op(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#suffix_op.
    def exitSuffix_op(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#pointers.
    def enterPointers(self, ctx: ParserRuleContext):
        # print("pointer def is:" + ctx.getText())
        self.line = ctx.start.line
        self.pointer = True
        self.nr_pointers += 1
        var = getVariable(ctx.getText())
        type_ = getType(var)
        # TODO: check what is needed here
        self.current = Pointer(var, type_, self.line, self.nr_pointers, self.parent, False, self.is_declaration(var))
        self.parent.leftChild = self.current
        self.current = self.parent.rightChild
        self.dec_op = self.parent
        self.declaration = True
        # TODO: is declaration a declaration ? (check via self.is_declaration()
        pointer = Pointer(self.dec_op.leftChild.getValue(), self.dec_op.leftChild.getType(), self.dec_op.leftChild.line,
                          1, self.dec_op, self.dec_op.leftChild.const, self.dec_op.leftChild.declaration)
        self.dec_op.leftChild = pointer

    # Exit a parse tree produced by ExpressionParser#pointers.
    def exitPointers(self, ctx: ParserRuleContext):
        self.pointer = False
        # print("pointers exited")

    # Enter a parse tree produced by ExpressionParser#scope.
    def enterScope(self, ctx: ParserRuleContext):
        if self.c_block.trees is None:
            return
        self.scope_stack.push(self.c_block)
        self.c_block = block(None)

    # Exit a parse tree produced by ExpressionParser#scope.
    def exitScope(self, ctx: ParserRuleContext):
        if self.c_block.trees is None:
            return
        if self.scope_stack.__len__() == 0:
            self.program.blocks.append(self.c_block)
            self.c_block = block(None)
        else:
            sblock = self.scope_stack.pop()
            sblock.blocks.append(self.c_block)
            self.c_block = sblock

    # Enter a parse tree produced by ExpressionParser#lrules.
    def enterLrules(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#lrules.
    def exitLrules(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#lscope.
    def enterLscope(self, ctx: ParserRuleContext):
        print("enter lscope:" + ctx.getText())
        if self.c_block.trees is not None:
            self.scope_stack.push(self.c_block)
            self.c_block = block(None)

    # Exit a parse tree produced by ExpressionParser#lscope.
    def exitLscope(self, ctx: ParserRuleContext):
        if isinstance(self.loop, While) or isinstance(self.loop,For) or isinstance(self.loop,If):
            self.loop.c_block = self.c_block
            self.c_block = block(None)
        # todo append a block not loop?
        if self.scope_stack.__len__() == 0:
            self.program.blocks.append(self.loop)
        else:
            sblock = self.scope_stack.pop()
            sblock.blocks.append(self.loop)
            self.c_block = sblock
        self.loop = None

    # Enter a parse tree produced by ExpressionParser#loop.
    def enterLoop(self, ctx: ParserRuleContext):
        self.is_loop=True

    # Exit a parse tree produced by ExpressionParser#loop.
    def exitLoop(self, ctx: ParserRuleContext):
        self.is_loop=False

    # Enter a parse tree produced by ExpressionParser#while.
    def enterWhile(self, ctx: ParserRuleContext):
        self.loop = While(line=ctx.start.line, parent=None)
        self.current = self.loop.Condition

    # Exit a parse tree produced by ExpressionParser#while.
    def exitWhile(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#for.
    def enterFor(self, ctx: ParserRuleContext):
        self.loop=For(line=ctx.start.line)
        self.current=self.loop.f_dec

    # Exit a parse tree produced by ExpressionParser#for.
    def exitFor(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#if.
    def enterIf(self, ctx: ParserRuleContext):
        self.loop = If(line=ctx.start.line,operator=getIftype(ctx.getText()))
        self.current = self.loop.Condition

    # Exit a parse tree produced by ExpressionParser#if.
    def exitIf(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#break.
    def enterBreak(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#break.
    def exitBreak(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#continue.
    def enterContinue(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#continue.
    def exitContinue(self, ctx: ParserRuleContext):
        pass

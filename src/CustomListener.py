from generated.input.ExpressionListener import *
from src.HelperFunctions import *
from .ast.block import block
from .ast.Program import program
import string


# TODO: zet alles in trees (unnamed scopes in scope node) --> volgorde probleem llvm --> ok
# TODO: ook program enkel trees niet block gebruiken                                 --> ok
# TODO : vorm for om in while lus                                                    --> ok
# TODO :nieuwe block aanmaken--> parent block meegeven aan nieuwe block.             --> ok
class CustomListener(ExpressionListener):
    def __init__(self, pathName):

        self.is_ref = False
        self.is_loop = False
        self.is_char = False
        self.is_parameter = False
        self.is_print = False
        self.is_scan = False
        self.is_array = False

        self.a_dec = False
        self.a_val = None
        self.stop_fold = False
        self.start_rule = None
        self.asT = create_tree()
        self.current = None
        self.parent = None
        self.left = True
        self.right = False
        self.declaration = False
        self.dec_op = None
        self.counter = 0
        self.program = program()
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
        self.return_function = False
        self.function_scope = False
        self.c_scope = Scope(0, None)
        self.call_function = False
        self.param = []

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
        """
        if type_ == LiteralType.INT:
            self.current = Print(Value(ctx.getText(), LiteralType.INT, ctx.start.line, None))
        elif type_ == LiteralType.FLOAT:
            self.current = Print(Value(ctx.getText(), LiteralType.FLOAT, ctx.start.line, None))
        elif type_ == LiteralType.STR:
            self.current = Print(Value(ctx.getText(), LiteralType.CHAR, ctx.start.line, None))
        else:
            self.current = Print(Value(ctx.getText(), LiteralType.VAR, ctx.start.line, None))

        self.asT.root = self.current
        self.c_scope.block.trees.append(self.asT)
        self.current = None
        self.asT = create_tree()
        """
        i = Value(ctx.getText(), type_, ctx.start.line)
        if isinstance(self.current, Print) or isinstance(self.current, Scan):
            self.current.addParam(i)
        return

    def set_pointer(self, ctx: ParserRuleContext, type_):
        if self.dec_op.rightChild is None:
            self.dec_op.rightChild = Value(ctx.getText(), type_, self.dec_op, ctx.start.line, True)
        else:
            # print("former value:")
            # print(self.dec_op.rightChild.getValue())
            self.dec_op.rightChild.setValue(ctx.getText())

    def set_val(self, ctx: ParserRuleContext):
        # print("set val:" + ctx.getText())
        type_ = find_value_type(ctx.getText())
        v = ctx.getText()
        if self.is_print or self.is_scan:
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

        if self.is_print:
            val = self.current.getValue()
            if self.current.type == LiteralType.VAR:
                val = self.c_scope.block.getSymbolTable().findSymbol(self.current.getValue())
            p = Print(val)
            self.asT = create_tree()
            self.asT.setRoot(p)
            self.c_scope.block.trees.append(self.asT)
            self.asT = create_tree()
            return
        if self.right or (self.parent.rightChild is None and self.parent.leftChild is not None):
            self.parent.setRightChild(self.current)
            self.right = False
            self.left = True
        elif self.left:
            self.parent.setLeftChild(self.current)
            self.right = True

    def set_expression(self, ctx: ParserRuleContext):
        self.expr_layer += 1
        # print("expression :" + ctx.getText() + "with layer:" + str(self.expr_layer))
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
        if operator is None:
            operator = BinaryOperator(ctx.getText(), ctx.start.line)
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
        # print("start rule"+ctx.getText())
        self.start_rule = ctx.getText()
        # GLOBAL SCOPE
        self.c_scope = Scope(ctx.start.line)
        self.c_scope.global_ = True
        self.c_scope.block = block(None)
        self.c_scope.block.name = "program"
        self.c_scope.block.setParent(self.program)

        self.program.tree = self.c_scope

    # Exit a parse tree produced by ExpressionParser#start_rule.
    def exitStart_rule(self, ctx: ParserRuleContext):
        # todo : IF NOT GLOBAL?
        if self.c_scope.global_:
            # self.c_scope.block = self.c_block
            self.program.tree = self.c_scope
            self.program.tree.block.setParent(self.program)
        return
        # self.program.blocks = self.c_block
        # self.c_block = block(None)

    # Enter a parse tree produced by ExpressionParser#print.
    def enterPrint(self, ctx: ParserRuleContext):
        self.is_print = True
        if not self.program.include_added:
            raise NotDeclared("printf", ctx.start.line)
        self.current = Print("")

    # Exit a parse tree produced by ExpressionParser#print.
    def exitPrint(self, ctx: ParserRuleContext):
        self.is_print = False
        self.asT = create_tree()
        self.asT.root = self.current
        self.c_scope.block.trees.append(self.asT)
        self.asT = create_tree()
        self.current = None

    # Enter a parse tree produced by ExpressionParser#format_string.
    def enterFormat_string(self, ctx: ParserRuleContext):
        if isinstance(self.current, Print):
            self.current.setParamString(ctx.getText())

    # Exit a parse tree produced by ExpressionParser#format_string.
    def exitFormat_string(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#scan.
    def enterScan(self, ctx: ParserRuleContext):
        self.is_scan = True
        self.current = Scan("")
        if not self.program.include_added:
            raise NotDeclared("scanf", ctx.start.line)

    # Exit a parse tree produced by ExpressionParser#scan.
    def exitScan(self, ctx: ParserRuleContext):
        self.is_scan = False

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
        val = self.c_scope.block.getSymbolTable().findSymbol(pval)
        cval = ''
        if val[1] == LiteralType.INT:
            cval = int(val[0])
        elif val[1] == LiteralType.FLOAT:
            cval = float(val[0])
        self.current = Value(cval, val[1], ctx.start.line, self.parent)
        self.parent.rightChild = self.current

    # Exit a parse tree produced by ExpressionParser#pointer_val.
    def exitPointer_val(self, ctx: ParserRuleContext):
        # print("exit pointer val")
        self.rhs_pointer = False

    # Enter a parse tree produced by ExpressionParser#pointer.
    def enterPointer(self, ctx: ParserRuleContext):
        if self.rhs_pointer:
            return
        self.nr_pointers += 1
        self.dec_op.leftChild.setValue(self.dec_op.leftChild.getValue()[1:])
        if isinstance(self.dec_op.leftChild, Pointer):
            self.dec_op.leftChild.setPointerLevel(self.nr_pointers)
        else:
            pointer = Pointer(self.dec_op.leftChild.getValue(), self.dec_op.leftChild.getType(), ctx.start.line,
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
        var = ctx.getText()
        is_ref = False
        if var[0] == "&":
            var = var[1:]
            self.is_ref = True
        ref = self.c_scope.block.getSymbolTable().findSymbol(var)
        # print(self.nr_pointers)
        if isinstance(self.dec_op.leftChild,
                      Pointer) and self.is_ref and self.nr_pointers > 0 and not self.dec_op.leftChild.declaration:
            raise PointerError(self.dec_op.leftChild.getValue(), ctx.start.line)
        if isinstance(self.dec_op.leftChild,
                      Pointer) and not self.is_ref and self.nr_pointers == 0 and not self.dec_op.leftChild.declaration:
            raise PointerError(self.dec_op.leftChild.getValue(), ctx.start.line)
        try:
            if not ref:
                raise NotDeclared(var, ctx.start.line)
            else:
                # self.parent.rightChild=Value(var,self.c_block.getSymbolTable().findSymbol(var)[1],self.line,self.parent,variable=True)
                self.parent.rightChild = Value(var, ref[1], ctx.start.line, self.parent, variable=True)
                self.current = self.parent.rightChild
                return

        except NotDeclared:
            raise

    # Exit a parse tree produced by ExpressionParser#ref_ref.
    def exitRef_ref(self, ctx: ParserRuleContext):
        self.is_ref = False

    # Enter a parse tree produced by ExpressionParser#dec.
    def enterDec(self, ctx: ParserRuleContext):  # TODO: declaration needs to get right type
        # print("ente dec:" + ctx.getText())
        # print("new dec:" + ctx.getText())
        self.start_rule = self.start_rule[len(ctx.getText()) + 1:]
        self.asT = create_tree()
        # self.parent = Declaration()
        var = getVariable(ctx.getText())

        if var == '':
            if str(self.start_rule[-1]).isdigit():
                raise RightValRef(ctx.start.line)
            else:
                raise ReservedWord(ctx.start.line, variable=var)
            pass

        type = getType(var)
        self.a_dec = not (type is False)
        self.a_val = var
        if type is False:
            # print("val is :" + var)
            if self.c_scope.block.getSymbolTable().findSymbol(var) is not None:
                if self.c_scope.block.getSymbolTable().findSymbol(var)[2] >= 1:
                    self.current = Pointer(var, self.c_scope.block.getSymbolTable().findSymbol(var)[1], ctx.start.line,
                                           self.c_scope.block.getSymbolTable().findSymbol(var)[2], self.parent)
                else:
                    self.current = Value(var, self.c_scope.block.getSymbolTable().findSymbol(var)[1], ctx.start.line,
                                         self.parent,
                                         variable=True)
            else:
                self.current = Value(var, LiteralType.FLOAT, ctx.start.line, self.parent, variable=True, decl=False)


        else:
            self.current = Value(var, type, ctx.start.line, self.parent, variable=True, decl=True)
        # self.parent.leftChild = self.current
        self.parent = Declaration(self.current, ctx.start.line)
        self.current = self.parent.rightChild
        self.dec_op = self.parent
        self.declaration = True

    # Exit a parse tree produced by ExpressionParser#dec.
    def exitDec(self, ctx: ParserRuleContext):
        self.a_dec = False
        self.a_val = None
        if self.is_parameter:
            self.current = None
            self.dec_op = None
            self.parent = None
            self.asT = create_tree()
            return
        # print("exit dec:"+ctx.getText())
        """
        TODO:
        eerst fill literals
        fold
        add to symboltable
        :param ctx:
        :return:
        """
        if self.bracket_stack.__len__() > 0:
            self.set_bracket()
        if not isinstance(self.parent, UnaryOperator) and isinstance(self.parent.leftChild, Pointer):
            self.dec_op.rightChild = self.parent.rightChild
            if self.dec_op.rightChild is None:
                self.dec_op.rightChild = EmptyNode(ctx.start.line, self.dec_op, self.dec_op.leftChild.getType())
        elif self.current is None:
            if isinstance(self.dec_op.leftChild, Array):
                self.dec_op = self.dec_op.leftChild
                # self.dec_op.rightChild = EmptyNode(ctx.start.line, self.dec_op, self.dec_op.leftChild.getType())
            else:
                self.dec_op.rightChild = Value(0, self.dec_op.leftChild.getType(), self.dec_op, ctx.start.line, False)

        else:
            while self.current.parent is not None:
                self.current = self.current.parent
            if isinstance(self.current, BinaryOperator) and self.current.operator == "":
                self.current = self.current.leftChild
            if isinstance(self.current, Declaration):
                if self.current.rightChild is None:
                    self.current.leftChild.parent = self.dec_op
                    self.dec_op.leftChild = self.current.leftChild
                    if self.dec_op.rightChild is None:
                        if isinstance(self.dec_op.leftChild, Array):
                            self.dec_op = self.dec_op.leftChild
                        else:
                            self.dec_op.rightChild = EmptyNode(ctx.start.line, self.dec_op,
                                                               self.dec_op.leftChild.getType())
                else:
                    self.current.rightChild.parent = self.dec_op
                    self.dec_op.rightChild = self.current.rightChild
            else:
                self.dec_op.rightChild = self.current
        self.current = self.dec_op
        """
        get the correct type from table if redeclaration
        """
        if isinstance(self.dec_op, Array) and self.dec_op.declaration:
            self.c_scope.block.getSymbolTable().addSymbol(self.dec_op, self.c_scope.global_)
            self.parent = None
            self.current = None
            self.declaration = False
            self.asT = create_tree()
            return
        if self.c_scope.block.getSymbolTable().findSymbol(self.current.leftChild.getValue()) is not None:
            self.current.leftChild.setType(
                self.c_scope.block.getSymbolTable().findSymbol(self.current.leftChild.getValue())[1])
        self.asT.setRoot(self.current)
        if isinstance(self.asT.root.leftChild, Pointer):
            self.asT.root.leftChild.setLevel(self.nr_pointers)
            self.nr_pointers = 0

        self.asT.setNodeIds(self.asT.root)
        self.asT.generateDot(self.pathName + str(self.counter) + ".dot")
        # todo : dont fill if block needs info previous block
        if self.is_loop:
            if isinstance(self.loop, For) and self.loop.f_dec is None:
                self.loop.f_dec = self.asT
            elif isinstance(self.loop, For) and self.loop.f_incr is None:
                self.loop.f_incr = self.asT
            else:
                self.c_scope.block.trees.append(self.asT)
            self.counter += 1
            self.parent = None
            self.current = None
            self.declaration = False
            self.asT = create_tree()
            return
        if self.stop_fold:
            # TODO add to symboltable unfolded tree
            """
            if self.c_scope.f_name != "" and self.c_scope.f_return is None:
                self.parent = None
                self.current = None
                self.declaration = False
                self.asT = create_tree()
                return
            """
            self.c_scope.block.trees.append(self.asT)
            if self.c_scope.block.getSymbolTable().findSymbol(
                    self.current.leftChild.getValue()) is None and self.current.leftChild.declaration:
                """if self.current.rightChild is not Value:
                    self.asT.root.rightChild = EmptyNode(self.current.leftChild.line, self.current)"""
                self.c_scope.block.getSymbolTable().addSymbol(self.asT.root, self.c_scope.global_)
            self.counter += 1
            self.parent = None
            self.current = None
            self.declaration = False
            self.asT = create_tree()
            return

        if not isinstance(self.asT.root.leftChild, Pointer):
            self.c_scope.block.fillLiterals(self.asT)
        self.asT.foldTree()
        self.asT.setNodeIds(self.asT.root)
        self.asT.generateDot(self.pathName + str(self.counter) + ".dot")
        # self.c_block.trees.append(self.asT)
        self.asT.foldTree()
        self.asT.setNodeIds(self.asT.root)
        self.asT.generateDot(self.pathName + str(self.counter) + ".dot")
        pointer = ""
        level = 0
        self.c_scope.block.trees.append(self.asT)
        # if self.current.leftChild.declaration:
        self.c_scope.block.getSymbolTable().addSymbol(self.asT.root,
                                                      self.c_scope.global_)  # TODO: make bool depend on current scope
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
        self.set_token(ctx)

    # Exit a parse tree produced by ExpressionParser#binop.
    def exitBinop(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#binop_md.
    def enterBinop_md(self, ctx: ParserRuleContext):
        self.set_token(ctx)

    # Exit a parse tree produced by ExpressionParser#binop_md.
    def exitBinop_md(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#equality.
    def enterEquality(self, ctx: ParserRuleContext):
        self.set_token(ctx, LogicalOperator(ctx.getText()))

    # Exit a parse tree produced by ExpressionParser#equality.
    def exitEquality(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#comparator.
    def enterComparator(self, ctx: ParserRuleContext):
        self.set_token(ctx, LogicalOperator(ctx.getText()))

    # Exit a parse tree produced by ExpressionParser#comparator.
    def exitComparator(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#or_and.
    def enterOr_and(self, ctx: ParserRuleContext):
        self.set_token(ctx, LogicalOperator(ctx.getText()))

    # Exit a parse tree produced by ExpressionParser#or_and.
    def exitOr_and(self, ctx: ParserRuleContext):
        # self.set_token(ctx)
        pass

    # Enter a parse tree produced by ExpressionParser#expr.
    def enterExpr(self,
                  ctx: ParserRuleContext):  # TODO: start contains line and column values of where the token is located in the original code
        # print("enter expr:" + ctx.getText())
        return self.set_expression(ctx)

    # Exit a parse tree produced by ExpressionParser#expr.
    def exitExpr(self, ctx: ParserRuleContext):
        self.expr_layer -= 1
        if self.declaration is False and isinstance(self.loop,
                                                    For) and self.expr_layer == 0 and self.loop.Condition is None and self.loop.f_dec is not None:
            self.asT = create_tree()
            self.asT.setRoot(self.parent)
            self.loop.Condition = self.asT
        elif not self.declaration and isinstance(self.loop,
                                                 For) and self.expr_layer == 0 and self.loop.Condition is not None and self.loop.f_dec is not None and self.loop.f_incr is None:
            self.loop.f_incr = self.parent
        elif not self.declaration and self.expr_layer == 0:
            if isinstance(self.current.parent, BinaryOperator) and self.current.parent.operator == "":
                self.current.parent = None
                if isinstance(self.parent, BinaryOperator) and self.parent.operator == "":
                    self.parent = None
                elif isinstance(self.parent, BinaryOperator) or isinstance(self.parent, LogicalOperator):
                    self.current.parent = self.parent
                    if self.parent.leftChild is not None and isinstance(self.parent.leftChild, BinaryOperator) and \
                            self.parent.leftChild.operator == "":
                        self.parent.leftChild = self.current
                    if self.parent.rightChild is not None and isinstance(self.parent.rightChild, BinaryOperator) and \
                            self.parent.rightChild.operator == "":
                        self.parent.rightChild = self.current
            self.set_bracket()
            while self.current.parent is not None:
                self.current = self.current.parent
            if isinstance(self.current, BinaryOperator) and self.current.operator == "":
                self.current = self.current.leftChild
            self.asT.setRoot(self.current)
            if self.is_loop and self.loop.Condition is None:
                self.loop.Condition = self.asT
                # print("fill condition")
            else:
                # self.c_block.trees.append(self.asT)
                # self.c_block.trees.append(self.asT)
                self.asT.setNodeIds(self.asT.root)
                self.asT.generateDot(self.pathName + str(self.counter) + ".dot")
                if self.return_function:
                    self.c_scope.f_return = self.asT
                elif self.c_scope.f_name != "" and self.c_scope.f_return is not None:
                    return
                else:
                    self.c_scope.block.fillLiterals(self.asT)
                    self.asT.foldTree()
                    self.asT.setNodeIds(self.asT.root)
                    self.asT.generateDot(self.pathName + str(self.counter) + ".dot")
                    self.c_scope.block.trees.append(self.asT)

        elif self.return_function and self.expr_layer == 0:
            while self.current.parent is not None:
                self.current = self.current.parent
            self.asT = create_tree()
            self.asT.root = self.current
            self.c_scope.f_return = self.asT
            self.counter += 1
            self.parent = None
            self.current = None
            self.asT = create_tree()

    # Enter a parse tree produced by ExpressionParser#pri.
    def enterPri(self, ctx: ParserRuleContext):
        # print("pri is" + ctx.getText())
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
        comment = Comment(ctx.getText(), type, line=ctx.start.line)
        self.asT = create_tree()
        self.asT.root = comment
        self.c_scope.block.trees.append(self.asT)
        self.asT = create_tree()

    # Exit a parse tree produced by ExpressionParser#comments.
    def exitComments(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#line.
    def enterLine(self, ctx: ParserRuleContext):
        # print("new line:" + str(self.line))
        pass

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
        op = UnaryOperator(ctx.getText(), None, ctx.start.line)
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
        self.pointer = True
        self.nr_pointers += 1
        var = getVariable(ctx.getText())
        type_ = getType(var)
        # TODO: check what is needed here
        self.current = Pointer(var, type_, ctx.start.line, self.nr_pointers, self.parent, False,
                               self.is_declaration(var))
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
        if self.function_scope and ctx.getText()[0] != "{":
            return
        print("scope:" + ctx.getText())
        if self.function_scope:
            self.function_scope = False
            return
        self.scope_count += 1
        # self.c_scope.block = self.c_block
        self.scope_stack.push(self.c_scope)
        self.c_scope = Scope(ctx.start.line, self.scope_stack.peek())
        self.c_scope.block = block(None)
        self.c_scope.block.setParent(self.scope_stack.peek().block)

        self.asT = create_tree()

    # Exit a parse tree produced by ExpressionParser#scope.
    def exitScope(self, ctx: ParserRuleContext):
        print("exit scope:" + ctx.getText())
        self.scope_count -= 1
        # self.c_scope.block = self.c_block
        # TODO dit moet weg
        """if self.c_scope.f_name != "" and self.c_scope.f_name != "main":
           return"""
        # if self.c_block.parent is not None:
        #    self.c_block.parent.trees.append(self.c_scope)
        if self.scope_stack.__len__() > 0:
            n_scope = self.scope_stack.pop()
            self.c_scope.parent = n_scope
            self.c_scope.block.setParent(n_scope.block)
            ast = create_tree()
            ast.root = self.c_scope
            n_scope.block.trees.append(ast)
            self.c_scope = n_scope
        else:
            raise "getting out of scope without parent scope"

    # Enter a parse tree produced by ExpressionParser#lrules.
    def enterLrules(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#lrules.
    def exitLrules(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#lscope.
    def enterLscope(self, ctx: ParserRuleContext):
        print("enter lscope:" + ctx.getText())
        self.stop_fold = True
        self.scope_stack.push(self.c_scope.block)
        self.c_scope.block = block(self.scope_stack.peek())
        self.c_scope.block.setParent(self.scope_stack.peek())

    # Exit a parse tree produced by ExpressionParser#lscope.
    def exitLscope(self, ctx: ParserRuleContext):
        # for to while
        self.stop_fold = False
        if isinstance(self.loop, For):
            sblock = self.scope_stack.pop()
            sblock.trees.append(self.loop.f_dec)
            wloop = While(self.loop.line, self.loop.parent)
            wloop.Condition = self.loop.Condition
            self.c_scope.block.trees.append(self.loop.f_incr)
            wloop.c_block = self.c_scope.block
            ast = create_tree()
            ast.root = wloop
            sblock.trees.append(ast)
        else:
            self.loop.c_block = self.c_scope.block
            sblock = self.scope_stack.pop()
            ast = create_tree()
            ast.root = self.loop
            sblock.trees.append(ast)
        self.c_scope.block = sblock
        self.loop = None

    # Enter a parse tree produced by ExpressionParser#loop.
    def enterLoop(self, ctx: ParserRuleContext):
        self.is_loop = True

    # Exit a parse tree produced by ExpressionParser#loop.
    def exitLoop(self, ctx: ParserRuleContext):
        self.is_loop = False

    # Enter a parse tree produced by ExpressionParser#while.
    def enterWhile(self, ctx: ParserRuleContext):
        self.loop = While(line=ctx.start.line, parent=None)
        self.current = self.loop.Condition

    # Exit a parse tree produced by ExpressionParser#while.
    def exitWhile(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#for.
    def enterFor(self, ctx: ParserRuleContext):
        self.loop = For(line=ctx.start.line)
        self.current = self.loop.f_dec

    # Exit a parse tree produced by ExpressionParser#for.
    def exitFor(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#if.
    def enterIf(self, ctx: ParserRuleContext):
        self.loop = If(line=ctx.start.line, operator=getIftype(ctx.getText()))
        self.current = self.loop.Condition

    # Exit a parse tree produced by ExpressionParser#if.
    def exitIf(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#break.
    def enterBreak(self, ctx: ParserRuleContext):
        self.asT = create_tree()
        self.asT.setRoot(Break(line=ctx.start.line))
        self.c_scope.block.trees.append(self.asT)
        self.asT = create_tree()

    # Exit a parse tree produced by ExpressionParser#break.
    def exitBreak(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#continue.
    def enterContinue(self, ctx: ParserRuleContext):
        self.asT = create_tree()
        self.asT.setRoot(Continue(line=ctx.start.line))
        self.c_scope.block.trees.append(self.asT)
        self.asT = create_tree()

    # Exit a parse tree produced by ExpressionParser#continue.
    def exitContinue(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#function_definition.
    def enterFunction_definition(self, ctx: ParserRuleContext):
        # print("enter function definition:" + ctx.getText())
        self.enterScope(ctx)
        self.function_scope = True
        self.stop_fold = True
        return

    # Exit a parse tree produced by ExpressionParser#function_definition.
    def exitFunction_definition(self, ctx: ParserRuleContext):
        # print("exit function definition:" + ctx.getText())
        self.function_scope = False
        self.stop_fold = False
        if self.c_scope.f_name == "main":
            return
        #        self.c_scope.block.setParent(self.c_scope.parent.block)
        # self.program.getFunctionTable().addFunction(self.c_scope)
        if self.scope_stack.__len__() > 0:
            self.c_scope = self.scope_stack.pop()
        else:
            self.c_scope = self.program.tree

    # Enter a parse tree produced by ExpressionParser#function_name.
    def enterFunction_name(self, ctx: ParserRuleContext):
        # print("function name:" + ctx.getText())
        if self.function_scope:
            self.c_scope.f_name = ctx.getText()

    # Exit a parse tree produced by ExpressionParser#function_name.
    def exitFunction_name(self, ctx: ParserRuleContext):
        pass

    def enterFunction_dec(self, ctx: ParserRuleContext):
        # print("function declaration")
        self.call_function = True
        if self.dec_op is None or self.dec_op.leftChild is None:
            self.parent = None

        self.current = Function(f_name=getFunction(ctx.getText()), parent=self.parent, line=ctx.start.line)
        if self.declaration:
            self.current.parent = self.parent
            if self.parent is not None:
                if isinstance(self.parent, UnaryOperator) or isinstance(self.parent,
                                                                        Declaration) or self.parent.rightChild is not None:
                    self.parent.rightChild = self.current
                else:
                    self.parent.leftChild = self.current
        return

    # Exit a parse tree produced by ExpressionParser#function_dec.
    def exitFunction_dec(self, ctx: ParserRuleContext):
        if self.declaration:
            return
        self.c_scope.block.trees.append(self.current)
        self.call_function = False

    # Enter a parse tree produced by ExpressionParser#f_variables.
    def enterF_variables(self, ctx: ParserRuleContext):
        if isinstance(self.current, Function):
            self.current.addParameter(ctx.getText(), scope=self.c_scope, line=ctx.start.line)
        return

    # Exit a parse tree produced by ExpressionParser#f_variables.
    def exitF_variables(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#return_type.
    def enterReturn_type(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#return_type.
    def exitReturn_type(self, ctx: ParserRuleContext):
        self.c_scope.setReturnType(ctx.getText())

    # Enter a parse tree produced by ExpressionParser#return.
    def enterReturn(self, ctx: ParserRuleContext):
        # print("return is:" + ctx.getText())
        self.return_function = True

    # Exit a parse tree produced by ExpressionParser#return.
    def exitReturn(self, ctx: ParserRuleContext):
        self.return_function = False
        if self.current is not None and self.c_scope.f_return is None:
            while self.current.parent is not None:
                self.current = self.current.parent
            if isinstance(self.current, BinaryOperator) and self.current.operator=="":
                self.current=self.current.leftChild
            self.asT = create_tree()
            self.asT.root = self.current
            self.c_scope.f_return = self.asT
            self.asT = create_tree()
            self.current = None
        return

    # Enter a parse tree produced by ExpressionParser#parameters.
    def enterParameters(self, ctx: ParserRuleContext):
        #
        # print("enter param" + ctx.getText())
        v = ctx.getText()
        const = False
        if len(ctx.getText()) >= 5 and ctx.getText()[0:5] == 'const':
            const = True
            v = v[5:]
        ptype = getType(v)
        v = remove_type(ptype, v)
        plevel = 0
        if v[0] == "*":
            while v[0] == "*":
                plevel += 1
                v = v[1]
        if plevel > 0:
            val = Pointer(v, ptype, ctx.start.line, plevel, None, const, True)
        else:
            val = Value(v, ptype, ctx.start.line, None, True, const, True)
        self.c_scope.addParameter(val)
        symbol = Declaration(var=val, line=ctx.start.line, parent=None)
        symbol.leftChild = val
        symbol.rightChild = None
        self.c_scope.block.getSymbolTable().addSymbol(symbol, self.c_scope.global_)
        self.is_parameter = True
        self.enterDec(ctx)

    # Exit a parse tree produced by ExpressionParser#parameters.
    def exitParameters(self, ctx: ParserRuleContext):
        # print("exit paramaters:" + ctx.getText())
        self.exitDec(ctx)
        self.is_parameter = False
        #

    # Enter a parse tree produced by ExpressionParser#array.
    def enterArray(self, ctx: ParserRuleContext):
        self.is_array = True
        self.current = Array(getArrayName(ctx.getText()), line=ctx.start.line, pos=getArraySize(ctx.getText()),
                             parent=self.parent, valueType=self.dec_op.leftChild.getType(),
                             init=self.a_dec)
        if self.a_dec and getArrayName(self.a_val, self.dec_op.leftChild.getType()) == self.current.getValue():
            self.current.parent = self.dec_op
            self.current.declaration = True
            self.dec_op.leftChild = self.current
            self.current = None
        else:
            self.current.init = False
            if self.parent.rightChild is not None:
                self.parent.rightChild = self.current
            elif self.parent.leftChild is not None:
                self.parent.leftChild = self.current
        self.a_dec = False

    # Exit a parse tree produced by ExpressionParser#array.
    def exitArray(self, ctx: ParserRuleContext):
        self.is_array = False

    # Enter a parse tree produced by ExpressionParser#array_content.
    def enterArray_content(self, ctx: ParserRuleContext):
        pass

    # Exit a parse tree produced by ExpressionParser#array_content.
    def exitArray_content(self, ctx: ParserRuleContext):
        pass

    # Enter a parse tree produced by ExpressionParser#includes.
    def enterIncludes(self, ctx: ParserRuleContext):
        self.current = Include(ctx.getText(), ctx.start.line, None, None)
        self.asT = create_tree()
        self.asT.root = self.current
        self.c_scope.block.trees.append(self.asT)
        self.current = None
        self.asT = create_tree()
        self.program.include_added = True

    # Exit a parse tree produced by ExpressionParser#includes.
    def exitIncludes(self, ctx: ParserRuleContext):
        pass

    def get_program(self):
        self.program.ast.root = self.program.tree
        self.program.tree = None
        self.program.cleanProgram()
        self.program.setNodeIds()
        self.program.generateDot("generated/output/result.dot")

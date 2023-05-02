import ast
import struct

from src.LLVM.helper_functions import stack, remove_last_line_from_string
from src.ast.AST import AST
from src.ast.SymbolTable import SymbolTable
from src.ast.node import Declaration, Value, LiteralType, Comment, CommentType, Print, Pointer, Scope, If, While, Scan, \
    Continue, Break
from src.ast.block import block
from src.ast.Program import program
from src.ast.node_types.node_type import ConditionType


# TODO   break/continue while   v
# TODO   break/continue if      v
# TODO   if                     v
# TODO   expr met pointers
# TODO   scopes
# TODO   counter in return
# TODO   function calls
# TODO   arrays
# TODO   return expression      v
# TODO   print/scan             v
# TODO   include                v (niks toe te voegen)


class ToLLVM():
    def __init__(self):
        print("------------------START LLVM-----------------")
        self.c_function = None
        self.stop_loop = False
        self.g_def = dict()
        self.parameters = None
        self.c_scope = None
        self.scope_counter = None
        self.scope_dic_stack = stack()
        self.global_ = ""
        self.allocate = ""
        self.store = ""
        self.counter = 0
        self.var_dic = dict()
        self.main = True
        self.is_global = False
        self.g_count = 0
        self.f_count = 0
        self.g_assignment = ""
        self.f_declerations = ""
        self.c_block = None
        self.redec = []
        self.output = ""
        self.function_load = ""
        self.function_store = ""
        self.function_alloc = ""
        self.function_end = ""
        self.skip_count = -2
        self.if_prev = None
        # keeps branch label of last if
        self.if_stack = stack()
        self.branch_stack = stack()

    def STable_to_LLVM(self, table: SymbolTable):
        for entry in table:
            line = ""

    def get_variable(self, var: str):
        if isinstance(var, Value):
            var = var.value
        if var in self.var_dic:
            return self.var_dic[var]
        else:
            return self.add_variable(var)

    def add_variable(self, var: str):
        if isinstance(var, Value):
            var = var.value
        self.counter += 1
        if self.counter == self.skip_count:
            self.counter += 1
        if isinstance(var, str) and var[0] == "$":
            self.counter -= 1
        self.var_dic[var] = self.counter
        return self.var_dic[var]

    def increase_counter(self):
        self.counter += 1
        return self.counter

    def decrease_counter(self):
        self.counter -= 1
        return self.counter

    def get_counter(self):
        return self.counter

    def type_store(self, type_):
        if type_ == "int":
            return "i32"
        elif type_ == "float":
            return "float"
        elif type_ == "bool":
            return "i8"

    def float_to_hex(self, f):
        return hex(struct.unpack('<I', struct.pack('<f', f))[0])

    def float_to_64bit_hex(self, x):
        if x is None:
            print("x is none in scope:" + self.c_function.root.f_name)
        if isinstance(x, str):
            x = float(x)
        bytes_of_x = struct.pack('>f', x)
        x_as_int = struct.unpack('>f', bytes_of_x)[0]
        x_as_double = struct.pack('>d', x_as_int).hex()
        x_as_double = '0x' + x_as_double
        return x_as_double

    def get_type(self, v):
        if v.type == LiteralType.INT:
            return "int"
        elif v.type == LiteralType.FLOAT:
            return "float"
        elif v.type == LiteralType.BOOL:
            return "bool"
        elif v.type == LiteralType.CHAR:
            return "char"
        return False

    def start_main(self):
        self.allocate += "define i32 @main() #0 {\n"
        self.allocate += "%{} = alloca i32, align 4\n".format(self.add_variable("main"))
        self.store += "store i32 0, ptr %{}, align 4\n".format(self.get_variable("main"))

    def set_return_type(self, type):
        if type == LiteralType.CHAR:
            self.g_assignment += "define i8 @"
        elif type == LiteralType.INT:
            self.g_assignment += "define i32 @"
        elif type == LiteralType.FLOAT:
            self.g_assignment += "define float @"
        elif type == LiteralType.BOOL:
            self.g_assignment += "define i8 @"
        else:
            self.g_assignment += "define void @"
        return

    def start_function(self, f_name, parameters=None, return_type=None):
        self.g_assignment += "; Function Attrs: noinline nounwind optnone ssp uwtable(sync)\n"
        self.set_return_type(return_type)
        self.g_assignment += f_name
        self.set_function_parameters(parameters)
        self.store_alloc_function_parameters(parameters)

    def set_function_parameters(self, parameters):
        self.g_assignment += "("
        self.counter = -1
        i = 1
        # add return val to parameters if value or expression
        if isinstance(self.c_function.root, Scope) and (isinstance(self.c_function.root.f_return,
                                                                   Value) and not self.c_function.root.f_return.getType() == LiteralType.VAR):
            self.parameters.append(self.c_function.root.f_return.getValue())
        for pi in parameters:
            p = parameters[pi]
            if isinstance(p, Value) and p.getType() == LiteralType.INT:
                self.g_assignment += "i32 noundef %{}".format(self.add_variable(p.getValue()))

            elif isinstance(p, Value) and p.getType() == LiteralType.FLOAT:
                self.g_assignment += "float noundef %{}".format(self.add_variable(p.getValue()))

            elif isinstance(p, Value) and p.getType() == LiteralType.CHAR:
                self.g_assignment += "i8 noundef %{}".format(self.add_variable(p.getValue()))
            elif isinstance(p, Pointer):
                self.g_assignment += "ptr noundef %{}".format(self.add_variable(p.getValue()))
            if i != len(parameters):
                self.g_assignment += ","
            i += 1
        self.g_assignment += ") #0 { \n"

    def store_alloc_function_parameters(self, parameters):
        for pi in parameters:
            p = parameters[pi]
            if isinstance(p, Value) and p.getType() == LiteralType.INT:
                old_var = self.get_variable(p.getValue())
                self.function_alloc += "%{} = alloca i32, align 4\n".format(self.add_variable(p.getValue()))
                self.function_store += "store i32 %{}, ptr %{}, align 4\n".format(old_var,
                                                                                  self.get_variable(p.getValue()))

            elif isinstance(p, Value) and p.getType() == LiteralType.FLOAT:
                old_var = self.get_variable(p.getValue())
                self.function_alloc += "%{} = alloca float, align 4\n".format(self.add_variable(p.getValue()))
                self.function_store += "store float %{}, ptr %{}, align 4\n".format(old_var,
                                                                                    self.get_variable(p.getValue()))

            elif isinstance(p, Value) and p.getType() == LiteralType.CHAR:
                old_var = self.get_variable(p.getValue())
                self.function_alloc += "%{} = alloca i8, align 4\n".format(self.add_variable(p.getValue()))
                self.function_store += "store i8 %{}, ptr %{}, align 4\n".format(old_var,
                                                                                 self.get_variable(p.getValue()))

            elif isinstance(p, Pointer):
                old_var = self.get_variable(p.getValue())
                self.function_alloc += "%{} = alloca ptr, align 4\n".format(self.add_variable(p.getValue()))
                self.function_store += "store ptr %{}, ptr %{}, align 4\n".format(old_var,
                                                                                  self.get_variable(p.getValue()))

    def end_main(self):
        self.g_assignment += "; Function Attrs: noinline nounwind optnone ssp uwtable(sync)\n"
        self.store += "\n"
        self.store += "ret i32 0\n"
        self.store += "}\n"

    def end_function(self):
        print("end function aangeroepen")
        v = self.c_function.root.f_return.root
        if isinstance(v, Value):
            var_name = v.getValue()
            type_ = v.getType()
            if var_name is not None:
                old_variable = self.get_variable(var_name)
                self.g_assignment += " %{} = load ptr, ptr %{}, align 4\n".format(self.add_variable(var_name),
                                                                                  old_variable)
            if type_ == LiteralType.INT:
                self.g_assignment += "ret i32 %{}".format(self.get_variable(var_name))
            elif type_ == LiteralType.FLOAT:
                self.g_assignment += "ret float %{}".format(self.get_variable(var_name))
            elif type_ == LiteralType.CHAR:
                self.g_assignment += "ret i8 %{}".format(self.get_variable(var_name))
            elif type_ == LiteralType.BOOL:
                self.g_assignment += "ret float %{}".format(self.get_variable(var_name))
            else:
                self.g_assignment += "ret void"
            self.g_assignment += "}\n"
            self.counter = 0

    def scope_tree(self, tree: AST):
        if isinstance(tree.root, Scope) and tree.root.f_name == "":
            return self.unnamed_scope(tree)
        elif isinstance(tree.root, Scope) and tree.root.f_name != "":
            return self.function_scope(tree)

    def transverse_program(self, _program: program):
        _block = _program.block
        self.is_global = _program.tree.global_
        # set global functions
        if isinstance(_program.tree, Scope):
            self.c_scope = _program.tree
            # set global functions
            # set global variables
            # enter unnamed scopes
            for tree in self.c_scope.block.trees:
                if isinstance(tree.root, Scope):
                    self.scope_tree(tree)
                elif isinstance(tree.root, If):
                    pass
                elif isinstance(tree, While):
                    pass
                elif isinstance(tree.root, Declaration):
                    self.to_declaration(tree)
                elif isinstance(tree.root, Print):
                    self.to_print(tree)
                elif isinstance(tree.root, Comment):
                    self.to_comment(tree)

        """
        if _block.fname == 'main':
            self.start_main()
            self.transverse_block(_block)
            for _ in _block.blocks:
                print("block in blocks")
            self.end_main()
        """

    def transverse_block(self, cblock: block):
        self.c_block = cblock
        for tree in cblock.trees:
            if isinstance(tree.root, Declaration):
                if tree.root.leftChild.declaration:
                    self.to_declaration(tree)
                else:
                    self.redec.append(tree)
            elif isinstance(tree.root, Value):
                # print("expression no declaration is: "+str(tree.root.value))
                pass
            elif isinstance(tree.root, Comment):
                self.to_comment(tree)
            elif isinstance(tree.root, Print):
                self.to_print(tree)
        cblock.trees = self.redec
        for tree in cblock.trees:
            if isinstance(tree.root, Declaration):
                self.to_declaration(tree)

    def write_to_file(self, filename: str):
        # open text file
        text_file = open(filename, "w")
        text_file.write(self.output)
        # write string to file
        """
        if self.main:
            text_file.write(self.g_assignment)
            text_file.write("\n")
            text_file.write(self.allocate)
            text_file.write("\n")
            text_file.write(self.store)
            text_file.write("\n")
            text_file.write(self.f_declerations)
            text_file.write("\n")

        else:
            text_file.write(self.global_)
"""
        # close file
        text_file.close()

    def allignment(self, type: str):
        if type == 'i32' or 'float':
            return '4'
        elif type == 'i8':
            return '1'

    def switch_Literals(self, v: Value, input: Value, one_side=False):
        # comment above with original code:
        const = ""
        type = ""
        if v.const:
            const = "const"

        if v.type == LiteralType.INT:
            if v.declaration:
                self.allocate += "; {} {} {} = {}\n".format(const, "int", v.value, input.value)
                self.allocate += "%{} = alloca i32, align 4\n".format(self.add_variable(str(v.value)))
            if one_side:
                return
            self.store += "store i32 {}, i32* %{}, align 4\n".format(input.value, self.get_variable(v.value))

        elif v.type == LiteralType.FLOAT:
            val = self.float_to_64bit_hex(input.value)
            if v.declaration:
                self.allocate += "; {} {} {} = {}\n".format(const, "float", v.value, input.value)
                self.allocate += "%{} = alloca float, align 4\n".format(self.add_variable(v.value))
            if one_side:
                return
            self.store += "store float {}, float* %{}, align 4\n".format(val, self.get_variable(v.value))

        elif v.type == LiteralType.CHAR:
            size = len(input.value)
            if v.declaration:
                self.allocate += "; {} {} {} = {}\n".format(const, "char", v.value, input.value)
                self.allocate += "%{} = alloca i8, align 1\n".format(self.add_variable(v.value))
            if one_side:
                return
            num = ord(input.value[1])
            self.store += "store i8 {}, i8* %{}, align 1\n".format(num, self.get_variable(v.value))

        elif v.type == LiteralType.BOOL:
            bval = 0
            if input.value == "True":
                bval = 1
            if v.declaration:
                self.allocate += "; {}{}{}={}\n".format(const, "_Bool", v.value, input.value)
                self.allocate += "%{} = alloca i8, align 1\n".format(self.add_variable(v.value))
            if one_side:
                return
            self.store += "store i8 {}, i8* %{}, align 1\n".format(bval, self.get_variable(v.value))

    def switch_global_Literals(self, v: Value, input: Value, one_side=False):
        # comment above with original code:
        if v.declaration:
            const = ""
            type = ""
            if v.const:
                const = "const"
            if v.type == LiteralType.INT:
                self.allocate += "; {} {} {} = {}\n".format(const, "int", v.value, input.value)
                self.allocate += "@{} = global i32 {}, align 4\n".format(v.value, input.value)

            elif v.type == LiteralType.FLOAT:
                self.allocate += "; {} {} {} = {}\n".format(const, "float", v.value, input.value)
                self.allocate += "@{} = global float {}, align 4\n".format(v.value,
                                                                           self.float_to_64bit_hex(input.value))

            elif v.type == LiteralType.CHAR:
                num = ord(input.value[1])
                self.allocate += "; {} {} {} = {}\n".format(const, "char", v.value, input.value)
                self.allocate += "@{} = global i8 {}, align 1\n".format(v.value, num)

            elif v.type == LiteralType.BOOL:
                bval = 0
                if input.value == "True":
                    bval = 1
                self.allocate += "; {}{}{}={}\n".format(const, "_Bool", v.value, input.value)
                self.allocate += "@{} = global i8 {}, align 1\n".format(v.value, bval)
        else:
            raise "invalid input switch global literals"

    def to_bin_operator(self, operator, leftValue: Value, rightValue: Value, typeOfValue):
        if operator == "/":
            if typeOfValue == LiteralType.INT:
                old_val = self.get_variable(leftValue.value)
                self.g_assignment += "%{} = load i32, ptr %{}, align 4\n".format(old_val,
                                                                                 self.add_variable(leftValue.value))
                old_val = self.get_variable(rightValue.value)
                self.g_assignment += "%{} = load i32, ptr %{}, align 4".format(self.add_variable(rightValue.value),
                                                                               old_val)
                self.g_assignment += "%{} = sdiv i32 %4, %5"
                """
                  %4 = load i32, ptr %2, align 4
                  %5 = load i32, ptr %2, align 4
                  %6 = sdiv i32 %4, %5
                """

    def to_declaration(self, ast: AST, one_side=False):
        if isinstance(ast.root.leftChild, Pointer):

            if ast.root.leftChild.declaration:
                t_type = self.get_type(ast.root.leftChild)
                const = ""
                if ast.root.leftChild.const:
                    const = "const"
                points = ""
                i = 0
                while i < ast.root.leftChild.getPointerLevel():
                    points += "*"
                    i += 1
                self.allocate += "; {} {} {} {} = & {}\n".format(const, t_type, points, ast.root.leftChild.getValue(),
                                                                 ast.root.rightChild.getValue())
                self.allocate += "%{} = alloca ptr, align 8\n".format(self.add_variable(ast.root.leftChild.getValue()))
                self.store += "store ptr %{}, ptr %{}, align 8\n".format(
                    self.get_variable(ast.root.rightChild.getValue()), self.get_variable(ast.root.leftChild.getValue()))
            elif ast.root.leftChild.getValue() in self.var_dic and str(ast.root.rightChild.getValue())[0].isdigit():

                pointer = ast.root.leftChild.getValue()
                level = self.c_block.getSymbolTable().findSymbol(pointer, True)[2]
                o_pointer = self.get_variable(str(pointer))
                for i in range(level):
                    old_pointer = self.get_variable(str(pointer))
                    new_pointer = self.add_variable(str(pointer))
                    self.store += "%{} = load ptr, ptr %{}, align 8\n".format(new_pointer, o_pointer)
                    pointer = self.c_block.getSymbolTable().findSymbol(pointer, True)[0]
                    o_pointer = new_pointer

                p_type = self.type_store(self.get_type(ast.root.leftChild))
                val = ""
                if str(ast.root.rightChild.getValue())[0].isdigit():

                    val = ast.root.rightChild.getValue()
                    self.store += "store {} {}, ptr %{}, align 4\n".format(p_type, val, new_pointer)
                else:

                    val = self.c_block.getSymbolTable().findSymbol(ast.root.rightChild.getValue())[0]
                # elf.store += "store {} {}, ptr %{}, align 4\n".format(p_type,val,new_pointer)
            elif not ast.root.leftChild.declaration:
                reference = self.get_variable(ast.root.rightChild.getValue())
                pointer = self.get_variable(ast.root.leftChild.getValue())
                self.store += "store ptr %{}, ptr %{}, align 8\n".format(reference, pointer)
        elif isinstance(ast.root, Declaration):
            if self.is_global:
                return self.switch_global_Literals(ast.root.leftChild, ast.root.rightChild, one_side)
            else:
                return self.switch_Literals(ast.root.leftChild, ast.root.rightChild, one_side)
        return

    def to_comment(self, ast: AST):

        if isinstance(ast.root, Comment):
            if ast.root.type == CommentType.SL:
                if self.is_global:
                    self.g_assignment += ";"
                    self.g_assignment += ast.root.value
                    self.g_assignment += "\n"
                else:
                    self.store += ";"
                    self.store += ast.root.value
                    self.store += "\n"
            elif ast.root.type == CommentType.ML:
                if self.is_global:
                    # print("ml comment")
                    self.g_assignment += ";"
                    for s in ast.root.value:
                        self.g_assignment += s
                        if s == "\n":
                            self.g_assignment += ";"
                else:
                    # print("ml comment")
                    self.store += ";"
                    for s in ast.root.value:
                        self.store += s
                        if s == "\n":
                            self.store += ";"
        if self.is_global:
            self.g_assignment += "\n"
        else:
            self.store += "\n"

    def to_print(self, tree: AST, f_="printf"):
        """
            printf("hi %d dit\n", z);
            printf("hi %i dit\n", z);
            printf("hi %s dit\n", "z");
            printf("hi %c dit\n", 'c');

            %9 = load float, ptr %3, align 4
            %10 = fpext float %9 to double
            %11 = call i32 (ptr, ...) @printf(ptr noundef @.str.1, double noundef %10)
            %12 = call i32 (ptr, ...) @printf(ptr noundef @.str.2, ptr noundef @.str.3)
            %13 = call i32 (ptr, ...) @printf(ptr noundef @.str.4, i32 noundef 99)
        """

        to_print = tree.root.getValue()
        if isinstance(to_print, Value):
            to_print = to_print.value
            if self.c_scope.block.getSymbolTable().findSymbol(to_print) is not None:
                to_print = self.c_scope.block.getSymbolTable().findSymbol(to_print)[0]
            elif self.c_scope.f_name != "":
                to_print = self.c_scope.parameters[to_print]
        var = self.addGlobalString(tree.root)
        s = self.add_variable(f_ + str(self.g_count))
        self.store += "; {} ({})\n".format(f_, str(to_print))
        if isinstance(tree.root, Print) and tree.root.param.__len__() == 0 or tree.root.paramString.__len__() == 0:
            self.store += "%{} = call i32 (ptr, ...) @{}(ptr noundef @.str{})\n".format(s, f_, var)
        else:
            for p in tree.root.param:
                if p.getType == LiteralType.FLOAT:
                    old = self.get_variable(p.getValue())
                    self.store += "%{} = load float, ptr %{}, align 4\n".format(self.add_variable(p.getValue()), old)
                    old = self.get_variable(p.getValue())
                    self.store += "%{} = fpext float %{} to double\n".format(self.add_variable(p.getValue()), old)

            self.store += "%{} = call i32 (ptr, ...) @{}(ptr noundef @.str{} ".format(s, f_, var)
            i = 0
            for p in tree.root.param:
                self.store += ", "
                type_ = self.getPrintType(tree.root.paramString[i])
                print_ = self.getPrintValue(tree.root.paramString[i], type_, p)
                self.store += "{}noundef {}".format(type_, print_)
                i += 1
            self.store += ")\n"

    def to_scan(self, tree: AST):
        return self.to_print(tree, "scanf")

    def to_expression(self, param):
        pass

    def unnamed_scope(self, tree):
        pass

    def function_scope(self, tree):
        self.c_function = tree
        print("function scope")
        prev_global = self.is_global
        self.is_global = False
        self.counter = 0
        self.redec = []
        self.var_dic = dict()
        # TODO: add parameter list to start function
        self.skip_count = len(tree.root.parameters)
        self.start_function(tree.root.f_name, tree.root.parameters, tree.root.return_type)
        if self.counter == -1:
            self.counter = 0
        self.skip_count = -2
        """
        if declaration encountered in self.function_store
        operations:
        self.function_load
        """
        self.parameters = tree.root.parameters
        self.transverse_tree(tree.root.block)

        self.g_assignment += self.function_alloc
        self.g_assignment += "\n"
        self.g_assignment += self.function_store
        self.g_assignment += "\n"
        self.g_assignment += self.function_load

        if isinstance(tree.root.f_return.root, Value):
            self.end_function()

        self.output += self.g_assignment
        self.output = self.f_declerations + self.output

        self.c_function = None
        self.g_assignment = ""
        self.function_load = ""
        self.function_alloc = ""
        self.function_store = ""
        self.f_declerations = ""
        self.is_global = prev_global
        self.var_dic = dict()

    def transverse_tree(self, cblock: block, branch_count=0, start_loop=0):
        # declarations
        for tree in cblock.trees:
            if isinstance(tree.root, Declaration) and tree.root.leftChild.declaration:
                print("entered for dec" + tree.root.leftChild.getValue())
                self.to_declaration(tree, True)
                self.function_alloc += self.allocate
                self.allocate = ""
        # operations
        for tree in cblock.trees:
            # don't change tree function permanently
            t = tree
            if isinstance(t.root, Comment):
                self.to_comment(t)
                self.function_store += self.store
                self.store = ""
            elif isinstance(t.root, Print):
                self.to_print(t)
                self.function_load += self.store
                self.store = ""
            elif isinstance(t.root, Scan):
                pass
            elif isinstance(t.root, Continue):
                self.to_continue(t, branch_count, start_loop)
            elif isinstance(t.root, Break):
                self.to_break(t, branch_count)
            elif isinstance(t.root, While):
                print("while loop")
                self.set_while_loop(t)
            elif isinstance(t.root, If):
                print("if")
                self.set_if_loop(t)
            elif t is None:
                pass
            else:
                t.root.fold(self)
                # folded declaration, wont load in function_load
                if isinstance(t.root, Declaration) and isinstance(t.root.leftChild, Value):
                    t.root.leftChild.declaration = False
                    self.to_declaration(t)
                    self.function_load += self.store
                    self.store = ""

    def set_while_loop(self, t: AST):
        self.enter_branch()
        self.function_load += "br label %{}\n".format(self.increase_counter())
        counter0 = self.get_counter()
        self.function_load += str(self.get_counter()) + " :\n"
        if isinstance(t.root, While):
            b = block(None)
            b.trees.append(t.root.Condition)
            self.transverse_tree(b, self.branch_stack.peek(), counter0)
        tijdelijk = self.function_load
        self.function_load = ""
        counter1 = self.get_counter()
        counter2 = self.increase_counter()
        self.function_load += str(self.get_counter()) + " :\n"
        self.transverse_tree(t.root.c_block, self.branch_stack.peek(), counter0)
        if self.stop_loop:
            count = self.get_counter()
        else:
            count = self.increase_counter()
        tijdelijk += "br i1 %{}, label %{}, label %{}\n".format(counter1, counter2, count)
        self.function_load = tijdelijk + self.function_load
        if not self.stop_loop:
            self.function_load += "br label %{}, !llvm.loop !5\n".format(counter0)
            self.function_load += str(self.get_counter()) + " :\n"
        self.exit_branch()
        self.stop_loop = False

    def set_if_loop(self, t: AST, keep=False):
        if isinstance(t.root, If):

            if t.root.operator == ConditionType.IF:

                if self.if_stack.__len__() > 0 and not keep:
                    self.if_stack.pop()
                self.enter_branch()
                self.set_condition(t)
                counter0 = self.get_counter()
                self.increase_counter()
                tijdelijk = self.function_load
                self.function_load = "{} :\n".format(self.get_counter())
                ifs = [self.get_counter()]
                self.transverse_tree(t.root.c_block, self.branch_stack.peek())
                branch = ["br i1 %{}, label %{}, label %{}".format(counter0, counter0 + 1, self.increase_counter())]
                tijdelijk += branch[0] + "\n"
                self.function_load = tijdelijk + self.function_load
                branch.append("br label %{}\n".format(self.get_counter()))
                self.function_load += branch[1]
                self.function_load += "{} :\n".format(self.get_counter())
                self.if_stack.push(branch)
            elif t.root.operator == ConditionType.ELSE:
                self.enter_branch()
                self.transverse_tree(t.root.c_block, self.branch_stack.peek())
                self.increase_counter()
                while self.if_stack.__len__() > 0 and len(self.if_stack.peek()) == 2:
                    self.function_load = self.function_load.replace(self.if_stack.pop()[1],
                                                                    "br label %{}\n".format(self.get_counter()))

                self.function_load += "br label %{}\n".format(self.get_counter())
                self.function_load += "{} :\n".format(self.get_counter())

            elif t.root.operator == ConditionType.ELIF:
                t.root.operator = ConditionType.IF
                self.set_if_loop(t, True)
                last_entry = self.if_stack.pop()
                st_entries = self.if_stack
                while st_entries.__len__() > 0 and len(self.if_stack.peek()) == 2:
                    self.function_load = self.function_load.replace(st_entries.pop()[1], last_entry[1])
                self.if_stack.push(last_entry)
            self.exit_branch()

    def add_output_fold(self, out: str):
        self.g_assignment += out
        return

    def set_condition(self, t: AST):
        b = block(None)
        b.trees.append(t.root.Condition)
        self.transverse_tree(b)

    def to_continue(self, t: AST, counter=0, start_loop=0):
        self.function_load += "br label %{}, !llvm.loop !5\n".format(start_loop)
        if self.branch_stack.peek() == counter:
            self.stop_loop = True

    def to_break(self, t: AST, counter=0):
        self.function_load += "br label %{}\n".format(self.increase_counter())
        self.function_load += "{} :\n".format(self.get_counter())
        if self.branch_stack.peek() == counter:
            self.stop_loop = True

    def enter_branch(self):
        self.branch_stack.push(self.get_counter())

    def exit_branch(self):
        self.branch_stack.pop()

    def getPrintType(self, param: str, val: Value):
        if param == "%d" and val.type == LiteralType.FLOAT:
            return " double "
        if param == "%d" and val.type == LiteralType.INT:
            return " i32 "
        if param == "%s":
            return " ptr "
        if param == "%i" and val.type == LiteralType.FLOAT:
            return " double "
        if param == "%i" and val.type == LiteralType.INT:
            return " i32 "
        if param == "%c":
            return " i32"

    def getPrintValue(self, param: str, type_: str, p: Value):
        if param == "%c":
            return str(ord(str(p.getValue())))
        if param == "%d":
            if p.getValue().isdigit():
                if p.getType() == LiteralType.INT:
                    return str(p.getValue())
                if p.getType() == LiteralType.FLOAT:
                    return self.float_to_64bit_hex(p.getValue())
            return self.get_variable(p.getValue())
        if param == "%s":
            return "@.str{}" + self.addGlobalString(p)
        if param == "%i":
            if p.getValue().isdigit():
                if p.getType() == LiteralType.INT:
                    return str(p.getValue())
                if p.getType() == LiteralType.FLOAT:
                    return self.float_to_64bit_hex(p.getValue())
            return self.get_variable(p.getValue())

    def addGlobalString(self, v: Value):
        # adds the string and return string name
        var = ""
        if self.g_count > 0:
            var = "."
            var += str(self.g_count)
        else:
            if "print" not in self.g_def:
                self.f_count += 1
                self.f_declerations += "declare i32 @printf(ptr noundef, ...) #{}\n".format(self.f_count)
                self.g_def["print"] = True
        self.g_count += 1
        self.f_declerations += "@.str{} = private unnamed_addr constant [{}x i8] c\"{}\\0A\\00\", align 1\n".format(
            var, len(str(v.getValue())) + 2, str(v.getValue()))
        return var

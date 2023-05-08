import struct

from src.LLVM.Helper_LLVM import set_llvm_unary_operators, set_llvm_binary_operators
from src.LLVM.helper_functions import stack
from src.ast.AST import AST
from src.ast.SymbolTable import SymbolTable
from src.ast.node import Declaration, Value, LiteralType, Comment, CommentType, Print, Pointer, Scope, If, While, Scan, \
    Continue, Break, Array, Function, BinaryOperator, UnaryOperator, LogicalOperator
from src.ast.block import block
from src.ast.Program import program
from src.ast.node_types.node_type import ConditionType

# TODO: check
""""
normal op           v
while 
if 
function calls
array calls
scopes in scopes
pointers
"""


# TODO vraag said folden return end_function()-> not folding    x
# TODO   break/continue while                                   v
# TODO   break/continue if                                      v
# TODO   if                                                     v
# TODO   expr met pointers                                      v
# TODO   scopes                                                 x
# TODO   counter in return                                      v
# TODO   function calls                                         v
# TODO   arrays                                                 v
# TODO   return expression                                      v
# TODO   print/scan                                             v
# TODO   include                                                v (niks toe te voegen)

class ToLLVM():
    def __init__(self):


        self.program = None
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
        self.old_counter = stack()
        self.save_old_val = None
        self.enter_fold = False
        self.save_old_counter = None
        self.added = []
        self.stack_added = stack()
        self.looping = False
        self.allocated_var = dict()
        self.retransverse = []
        self.comparator_found=False

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
        #print("x is none in scope:" + self.c_function.root.f_name)
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

    def store_alloc_function_parameters(self, parameters=None):
        # add return val to parameters if value or expression
        if parameters is None:
            parameters = dict()
        for pi in parameters:
            p = parameters[pi]
            if isinstance(p, Value) and p.getType() == LiteralType.INT:
                old_var = self.get_variable(p.getValue())
                self.function_alloc += "%{} = alloca i32, align 4\n".format(self.add_variable(p.getValue()))
                self.function_store += "store i32 %{}, ptr %{}, align 4\n".format(old_var,
                                                                                  self.get_variable(p.getValue()))
                self.allocated_var[p.getValue()] = self.get_variable(p.getValue())

            elif isinstance(p, Value) and p.getType() == LiteralType.FLOAT:
                old_var = self.get_variable(p.getValue())
                self.function_alloc += "%{} = alloca float, align 4\n".format(self.add_variable(p.getValue()))
                self.function_store += "store float %{}, ptr %{}, align 4\n".format(old_var,
                                                                                    self.get_variable(p.getValue()))
                self.allocated_var[p.getValue()] = self.get_variable(p.getValue())

            elif isinstance(p, Value) and p.getType() == LiteralType.CHAR:
                old_var = self.get_variable(p.getValue())
                self.function_alloc += "%{} = alloca i8, align 4\n".format(self.add_variable(p.getValue()))
                self.function_store += "store i8 %{}, ptr %{}, align 4\n".format(old_var,
                                                                                 self.get_variable(p.getValue()))
                self.allocated_var[p.getValue()] = self.get_variable(p.getValue())

            elif isinstance(p, Pointer):
                old_var = self.get_variable(p.getValue())
                self.function_alloc += "%{} = alloca ptr, align 4\n".format(self.add_variable(p.getValue()))
                self.function_store += "store ptr %{}, ptr %{}, align 4\n".format(old_var,
                                                                                  self.get_variable(p.getValue()))
                self.allocated_var[p.getValue()] = self.get_variable(p.getValue())

    def end_main(self):
        self.g_assignment += "; Function Attrs: noinline nounwind optnone ssp uwtable(sync)\n"
        self.store += "\n"
        self.store += "ret i32 0\n"
        self.store += "}\n"

    def end_function(self):
        #print("end function aangeroepen")
        if self.c_function.root.f_return is None:
            self.g_assignment += "ret void"
            self.g_assignment += "}\n"
            self.counter = 0
            return
        v = self.c_function.root.f_return.root
        if not isinstance(v, Value) or isinstance(v, Pointer):
            self.c_function.root.f_return.root.printTables("random", self)
        v = self.c_function.root.f_return.root
        if isinstance(v, Value) or isinstance(v, Pointer):
            var_name = v.getValue()
            type_ = v.getType()
            if not v.variable:
                if type_ == LiteralType.CHAR:
                    v.setValue(v.getValue().replace("\'", ""))
                    v.setValue(ord(v.getValue()))
                self.g_assignment += "ret {} {}\n".format(self.get_llvm_type(v), v.getValue())
                self.g_assignment += "}\n"
                self.counter = 0
                return
            if var_name is not None:
                old_variable = self.allocated_var[var_name]
                self.g_assignment += " %{} = load {}, ptr %{}, align 4\n".format(self.add_variable(var_name),self.get_llvm_type(Value(var_name, type_, 0)),
                                                                                  old_variable)
            type_ = None
            if self.c_function.root.block.getSymbolTable().findSymbol(var_name) is not None:
                type_ = self.c_function.root.block.getSymbolTable().findSymbol(var_name)[1]
            elif var_name in self.c_function.root.param.keys:
                type_ = self.c_function.root.param[var_name].getType()
            if isinstance(v, Pointer):
                self.g_assignment += "ret ptr %{}".format(self.get_variable(var_name))
            else:
                self.g_assignment += "ret {} %{}".format(self.get_llvm_type(Value(0, type_, 0)),
                                                         self.get_variable(var_name))
        else:
            self.function_load = ""
            self.c_function.root.f_return.root.printTables("random", self)
            self.g_assignment += self.function_load

            self.g_assignment += "ret ptr %{}".format(self.get_counter())
        self.g_assignment += "}\n"
        self.counter = 0
        self.added = []
        self.allocated_var = dict()

    def scope_tree(self, tree: AST):
        if isinstance(tree.root, Scope) and tree.root.f_name == "":
            return self.unnamed_scope(tree)
        elif isinstance(tree.root, Scope) and tree.root.f_name != "":
            return self.function_scope(tree)

    def transverse_program(self, _program: program):
        self.program = _program
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
        # close file
        text_file.close()

    def allignment(self, type: str):
        if type == 'i32' or 'float':
            return '4'
        elif type == 'i8':
            return '1'
    def LiteralFunction(self,v:Function, var:Value):
        self.store += "%{} = alloca {}, align 4\n".format(self.add_variable(var.getValue()),self.get_llvm_type(var))

        self.allocated_var[var.getValue()]=self.get_counter()
        function=v
        inhoud = self.program.functions.findFunction(function.f_name, function.line)
        return_ = self.program.functions.findFunction(function.f_name, function.line)
        inhoud = function.param
        self.store += "%{} = call {} @{} ".format(self.add_variable(var.getValue()),
                                                         self.get_llvm_type(self.return_type_function(return_["return"])), function.f_name)
        self.store += "( "
        for key in inhoud:
            self.store += self.get_llvm_type(inhoud[key])
            val = key
            is_var = inhoud[key].variable
            if inhoud[key].getType() == LiteralType.FLOAT:
                val = self.float_to_64bit_hex(key)
            if is_var:
                self.store += " noundef %{},".format(self.get_variable(val))
            else:
                self.store += " noundef {},".format(val)
        self.store=self.store[:-1]
        self.store += ")\n"
        self.store += "store {} %{}, ptr %{}, align 4\n".format(self.get_llvm_type(var),self.get_variable(var.getValue()),self.allocated_var[var.getValue()])

        return
    def return_type_function(self, string:str):
        if string=="INT":
            return LiteralType.INT
        if string=="FLOAT":
            return LiteralType.FLOAT
        if string=="CHAR":
            return LiteralType.CHAR
        if string=="BOOL":
            return LiteralType.BOOL


    def LiteralArray(self, v: Array):
        self.allocate += "%{} = alloca [ {} x {}], align 4\n".format(self.add_variable(str(v.value)),
                                                                     v.pos, self.get_llvm_type(v.getType()))
        self.allocated_var[str(v.value)] = self.get_variable(str(v.value))
        if v.pos > 0 and v.arrayContent.__len__()>0:
            if self.global_:
                self.f_declerations += "@{} = global [".format(v.value)
            else:
                self.f_declerations += "@__const.{}.{} = private unnamed_addr constant [{} x {}] [".format(
                    self.c_function.root.f_name, v.value, v.pos, self.get_llvm_type(v.getType()))

            for i in v.arrayContent:
                val = i.value
                if v.type == LiteralType.FLOAT:
                    v = self.float_to_64bit_hex(v.getValue())
                self.f_declerations += "{} {},".format(self.get_llvm_type(v.type), i.value)
            self.f_declerations = self.f_declerations[:-1]
            self.f_declerations += "] , align 4 \n"

    def switch_Literals(self, v, input_, one_side=False):
        # comment above with original code:
        const = ""
        type = ""
        if isinstance(v, Array):
            return self.LiteralArray(v)
        if isinstance(input_, Function):
            return self.LiteralFunction(input_, v)
        if v.const:
            const = "const"

        if v.type == LiteralType.INT:
            if v.declaration:
                self.allocate += "; {} {} {};\n".format(const, "int", v.value)
                self.allocate += "%{} = alloca i32, align 4\n".format(self.add_variable(str(v.value)))
                self.allocated_var[str(v.value)] = self.get_variable(str(v.value))
            if one_side:
                return
            self.store += "store i32 {}, i32* %{}, align 4\n".format(input_.value, self.get_variable(v.value))

        elif v.type == LiteralType.FLOAT:
            val = self.float_to_64bit_hex(input_.value)
            if v.declaration:
                self.allocate += "; {} {} {};\n".format(const, "float", v.value)
                self.allocate += "%{} = alloca float, align 4\n".format(self.add_variable(v.value))
                self.allocated_var[str(v.value)] = self.get_variable(str(v.value))
            if one_side:
                return
            self.store += "store float {}, float* %{}, align 4\n".format(val, self.get_variable(v.value))

        elif v.type == LiteralType.CHAR:
            size = len(input_.value)
            if v.declaration:
                self.allocate += "; {} {} {};\n".format(const, "char", v.value)
                self.allocate += "%{} = alloca i8, align 1\n".format(self.add_variable(v.value))
                self.allocated_var[str(v.value)] = self.get_variable(str(v.value))
            if one_side:
                return
            num = ord(input_.value[1])
            self.store += "store i8 {}, i8* %{}, align 1\n".format(num, self.get_variable(v.value))

        elif v.type == LiteralType.BOOL:
            bval = 0
            if input_.value == "True":
                bval = 1
            if v.declaration:
                self.allocate += "; {}{}{};\n".format(const, "_Bool", v.value)
                self.allocate += "%{} = alloca i8, align 1\n".format(self.add_variable(v.value))
                self.allocated_var[str(v.value)] = self.get_variable(str(v.value))
            if one_side:
                return
            self.store += "store i8 {}, i8* %{}, align 1\n".format(bval, self.get_variable(v.value))

    def switch_global_Literals(self, v, input_, one_side=False):
        # comment above with original code:
        if isinstance(v, Array):
            return self.LiteralArray(v)
        if isinstance(v,Function):
            input_=self.LiteralFunction(v)

        if v.declaration:
            const = ""
            type = ""
            if v.const:
                const = "const"
            if v.type == LiteralType.INT:
                self.allocate += "; {} {} {} = {}\n".format(const, "int", v.value, input_.value)
                self.allocate += "@{} = global i32 {}, align 4\n".format(v.value, input_.value)

            elif v.type == LiteralType.FLOAT:
                self.allocate += "; {} {} {} = {}\n".format(const, "float", v.value, input_.value)
                self.allocate += "@{} = global float {}, align 4\n".format(v.value,
                                                                           self.float_to_64bit_hex(input_.value))

            elif v.type == LiteralType.CHAR:
                num = ord(input_.value[1])
                self.allocate += "; {} {} {} = {}\n".format(const, "char", v.value, input_.value)
                self.allocate += "@{} = global i8 {}, align 1\n".format(v.value, num)

            elif v.type == LiteralType.BOOL:
                bval = 0
                if input_.value == "True":
                    bval = 1
                self.allocate += "; {}{}{}={}\n".format(const, "_Bool", v.value, input_.value)
                self.allocate += "@{} = global i8 {}, align 1\n".format(v.value, bval)
        else:
            raise "invalid input SwitchLiteralType global literals"

    def get_loop_param(self, v):
        if isinstance(v, Value) and not v.variable:
            return
        if v.getValue() in self.allocated_var:

            old_var = self.allocated_var[v.getValue()]
            # self.counter-=1
            self.function_load += " %{} = load {}, ptr %{}, align 4\n".format(self.add_variable(v.getValue()),
                                                                              self.get_llvm_type(v), old_var)
        else:
            # find counter of the param function
            if v.getValue() in self.c_function.root.parameters:
                ci = 0
                for k in self.c_function.root.parameters:
                    if k != v.getValue():
                        ci += 1
                    else:
                        continue
            # save it in the function
            self.function_alloc += " %{} = alloca {}, align 4\n".format(self.add_variable(v.getValue()),
                                                                        self.get_llvm_type(v))
            self.allocated_var[v.getValue()] = self.get_variable(v.getValue())
            self.function_store += "store {} %{}, ptr %{}, align 4\n".format(self.get_llvm_type(v), ci,
                                                                             self.get_variable(v.getValue()))
            self.added.append(v.getValue())

    def get_param_dec(self, v):
        if self.looping:
            return self.get_loop_param(v)
        # find counter of the param function
        if v.getValue() in self.c_function.root.parameters:
            ci = 0
            for k in self.c_function.root.parameters:
                if k != v.getValue():
                    ci += 1
                else:
                    continue
        # save it in the function
        self.function_alloc += " %{} = alloca {}, align 4\n".format(self.add_variable(v.getValue()),
                                                                    self.get_llvm_type(v))
        self.allocated_var[v.getValue()] = self.get_variable(v.getValue())
        self.function_store += "store {} %{}, ptr %{}, align 4\n".format(self.get_llvm_type(v), ci,
                                                                         self.get_variable(v.getValue()))
        self.added.append(v.getValue())

    # save it to be used as input in declaration
    def redec_array(self,dec:AST):
        dec=dec.root
        size=0
        if self.c_function is not None:
            size=self.c_function.root.block.getSymbolTable().findSymbol(dec.leftChild.value)[0]

        old_counter=self.allocated_var[dec.leftChild.value]
        self.store += "%{} = getelementptr inbounds [{} x i32], ptr %{}, i64 0, i64 {}\n".format(self.add_variable(dec.leftChild.value),size, self.allocated_var[dec.leftChild.value],dec.leftChild.getPosition())
        self.store += "store {} {}, ptr %{}, align 4\n".format(self.get_llvm_type(dec.leftChild.type),dec.rightChild.value,self.get_variable(dec.leftChild.value))

        return
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
                self.allocated_var[ast.root.leftChild.getValue()] = self.get_variable(ast.root.leftChild.getValue())
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
        self.store += "; {} ({})\n".format(f_, tree.root.input_string)
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
        p_string=tree.root.input_string
        for t in tree.root.param:
            if isinstance(t,tuple):
                t=t[0]
            if not (isinstance(t.root,Value) or isinstance(t.root,Pointer) or isinstance(t.root,Array) ):
                t.foldTree()
                t.printTables("random",self)
            elif isinstance(t.root, Value):
                to_print = t.root.getValue()
                if t.root.variable:
                    if self.c_scope.block.getSymbolTable().findSymbol(to_print) is not None:
                        to_print = self.c_scope.block.getSymbolTable().findSymbol(to_print)[0]
                    else:
                        if t.root.getValue() in self.c_scope.parameters:
                            to_print = self.c_scope.parameters[t.root.getValue()].getValue()
                        else:
                            to_print = self.c_function.root.block.getSymbolTable().findSymbol(t.root.getValue())[0]
        var = self.addGlobalString(p_string)
        s = self.add_variable(f_ + str(self.g_count))

        if tree.root.param.__len__() == 0:
            self.store += "%{} = call i32 (ptr, ...) @{}(ptr noundef @.str{})\n".format(s, f_, var)
        else:
            for p in tree.root.param:
                if isinstance(p,tuple):
                    p=p[0]
                p=p.root
                if p.getType == LiteralType.FLOAT:
                    old = self.get_variable(p.getValue())
                    self.store += "%{} = load float, ptr %{}, align 4\n".format(self.add_variable(p.getValue()), old)
                    old = self.get_variable(p.getValue())
                    self.store += "%{} = fpext float %{} to double\n".format(self.add_variable(p.getValue()), old)

            self.store += "%{} = call i32 (ptr, ...) @{}(ptr noundef @.str{} ".format(s, f_, var)
            i = 0
            for p in tree.root.param:
                if isinstance(p,tuple):
                    p=p[0]
                p=p.root
                self.store += ", "
                type_ = self.getPrintType(tree.root.paramString[i], p)
                print_ = self.getPrintValue(tree.root.paramString[i], type_, p)
                self.store += "{}noundef {}".format(type_, print_)
                i += 1
            self.store += ")\n"

    def to_scan(self, tree: AST):
        return self.to_print(tree, "scanf")

    def to_expression(self, param):
        pass

    def unnamed_scope(self, tree):
        self.c_function = tree
        prev_global = self.is_global

    def function_scope(self, tree):
        self.c_function = tree

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
            if not isinstance(tree, AST):
                i = AST()
                i.root = tree
                tree = i
            if isinstance(tree.root, Declaration) and tree.root.leftChild.declaration:

                self.to_declaration(tree, True)
                self.function_alloc += self.allocate
                self.allocate = ""
            elif isinstance(tree.root,
                            Declaration) and tree.root.leftChild.getValue() in self.c_function.root.parameters and tree.root.leftChild.getValue() not in self.added:
                self.get_param_dec(tree.root.leftChild)
            elif isinstance(tree.root,
                            Declaration) and tree.root.leftChild.getValue() in self.c_function.root.parameters and self.looping:
                self.get_param_dec(tree.root.leftChild)
        # operations
        for tree in cblock.trees:
            # don't change tree function permanently
            t = tree
            if not isinstance(t, AST):
                i = AST
                i.root = t
                t = i
            if isinstance(t.root, Declaration) and (isinstance(t.root.rightChild, Value) or isinstance(t.root.rightChild, Array) or isinstance(t.root.rightChild, Function)):
                if isinstance(t.root.leftChild, Array):
                    self.redec_array(t)
                t.root.leftChild.declaration = False
                self.to_declaration(t)
                self.function_load += self.store
                self.store = ""
            elif isinstance(t.root,Array) and isinstance(t.root.parent,Declaration):
                a=AST
                a.root=t.root.parent
                t=a
                t.root.leftChild.declaration = False
                self.to_declaration(t)
                self.function_alloc += self.allocate
                self.function_load += self.store
                self.store = ""
                self.allocate =""
            elif isinstance(t.root, Scope):

                self.set_new_scope(t)

            elif isinstance(t.root, Array):
                self.LiteralArray(t.root)

            elif isinstance(t.root, Comment):
                self.to_comment(t)
                self.function_load += self.store
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

                self.set_while_loop(t)
            elif isinstance(t.root, If):

                self.set_if_loop(t)
            elif t is None:
                pass
            else:
                self.save_old_val = None
                if isinstance(t.root, Declaration):
                    self.save_old_val = t.root.leftChild
                    self.save_old_counter = self.get_variable(t.root.leftChild.getValue())
                    if t.root.leftChild.getValue() in self.allocated_var:
                        self.save_old_counter = self.allocated_var[t.root.leftChild.getValue()]
                    old_type = t.root.leftChild.getType()

                    self.enter_fold = True
                t.root.printTables("random", self)  # TODO: t.foldTree() -> check if dit werkt
                self.save_old_val = None
                if isinstance(t.root, Declaration):
                    # self.counter -= 1
                    self.function_load += " store {} %{}, ptr %{}, align 4\n".format(
                        self.get_llvm_type(old_type), self.get_counter(),
                        self.save_old_counter)
                # folded declaration, wont load in function_load
        """while len(self.retransverse)!= 0:
            t=self.retransverse
            self.retransverse=[]
            for ti in t:
                if 2 not in ti:
                    left=ti[0]
                    op=ti[1]
                    set_llvm_unary_operators(left,op,self)
                else:
                    left = ti[0]
                    right = ti[1]
                    op= ti[2]
                    set_llvm_binary_operators(left,right,op,self)"""






    def set_while_loop(self, t: AST):
        self.enter_branch()
        self.function_load += "br label %{}\n".format(self.increase_counter())
        counter0 = self.get_counter()
        self.function_load += str(self.get_counter()) + ":\n"
        # self.stack_added.push(self.added)
        # self.added = []
        self.looping = True
        if isinstance(t.root, While):
            b = block(None)
            b.trees.append(t.root.Condition)
            self.transverse_tree(b, self.branch_stack.peek(), counter0)
            #check what value was saved in dict
            #look up in symboltable or parameters
            val=self.find_val(self.get_counter())
            type=None
            if val is not None:
                if val in self.c_function.root.parameters:
                    type=self.c_function.root.parameters[val].getType()
                elif self.c_function.root.block.getSymbolTable().findSymbol(val) is not None:
                    type=self.c_function.root.block.getSymbolTable().findSymbol(val)[1]
            if type is None:
                type=LiteralType.INT
            if not self.comparator_found:
                self.function_load += "%{} = icmp ne {} %{}, 0\n".format(self.increase_counter(),self.get_llvm_type(type),self.get_variable(val))
            self.comparator_found=False
        tijdelijk = self.function_load
        self.function_load = ""
        counter1 = self.get_counter()
        counter2 = self.increase_counter()
        self.function_load += str(self.get_counter()) + ":\n"
        self.transverse_tree(t.root.c_block, self.branch_stack.peek(), counter0)
        if self.stop_loop:
            count = self.get_counter()
        else:
            count = self.increase_counter()
        tijdelijk += "br i1 %{}, label %{}, label %{}\n".format(counter1, counter2, count)
        self.function_load = tijdelijk + self.function_load
        if not self.stop_loop:
            self.function_load += "br label %{}\n".format(counter0)
            self.function_load += str(self.get_counter()) + ":\n"
        self.exit_branch()
        self.stop_loop = False
        # self.added = self.stack_added.pop()
        self.looping = False

    def set_if_loop(self, t: AST, keep=False):
        if isinstance(t.root, If):

            if t.root.operator == ConditionType.IF:

                if self.if_stack.__len__() > 0 and not keep:
                    self.if_stack.pop()
                self.enter_branch()
                #self.set_condition(t)
                counter0 = self.get_counter()
                self.increase_counter()
                tijdelijk = self.function_load
                self.function_load = "{}:\n".format(self.get_counter())
                ifs = [self.get_counter()]
                self.transverse_tree(t.root.c_block, self.branch_stack.peek())
                branch = ["br i1 %{}, label %{}, label %{}".format(counter0, counter0 + 1, self.increase_counter())]
                tijdelijk += branch[0] + "\n"
                self.function_load = tijdelijk + self.function_load
                branch.append("br label %{}\n".format(self.get_counter()))
                self.function_load += branch[1]
                self.function_load += "{}:\n".format(self.get_counter())
                self.if_stack.push(branch)
            elif t.root.operator == ConditionType.ELSE:
                self.enter_branch()
                self.transverse_tree(t.root.c_block, self.branch_stack.peek())
                self.increase_counter()
                while self.if_stack.__len__() > 0 and len(self.if_stack.peek()) == 2:
                    self.function_load = self.function_load.replace(self.if_stack.pop()[1],
                                                                    "br label %{}\n".format(self.get_counter()))

                self.function_load += "br label %{}\n".format(self.get_counter())
                self.function_load += "{}:\n".format(self.get_counter())

            elif t.root.operator == ConditionType.ELIF:
                t.root.operator = ConditionType.IF
                self.set_if_loop(t, True)
                if self.if_stack.__len__() > 0 :
                    last_entry = self.if_stack
                    st_entries = []
                else:
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
        self.function_load += "br label %{}\n".format(start_loop)
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
        if self.branch_stack.__len__()>0:
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

    def get_llvm_type(self, v=None):
        if isinstance(v, Pointer):
            return "ptr"
        val = v
        if isinstance(v,int):
            v=LiteralType.INT
        if isinstance(v,float):
            v=LiteralType.FLOAT
        if isinstance(v, Value):
            v = v.getType()
        if v == LiteralType.INT:
            return "i32"
        if v == LiteralType.FLOAT:
            return "float"
        if v == LiteralType.CHAR:
            return "i8"
        if v == LiteralType.BOOL:
            return "i1"
        if v == LiteralType.VAR:
            if self.looping:
                if val.getValue() in self.c_function.root.parameters:
                    return self.get_llvm_type(self.c_function.root.parameters[val.getValue()])
                else:
                    return self.get_llvm_type(self.c_function.root.block.getSymbolTable().findSymbol(val.getValue())[0])
            if val.getValue() in self.c_function.root.parameters:
                return self.get_llvm_type(self.c_function.root.parameters[val.getValue()])
            elif self.c_function.root.block.getSymbolTable().findSymbol(val.getValue()) is not None:
                self.get_llvm_type(self.c_function.root.block.getSymbolTable().findSymbol(val.getValue())[0])
            else:
                return None
        return None



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
        if isinstance(v,Value):
            v=v.getValue()
        #self.f_declerations += "@.str{} = private unnamed_addr constant [{}x i8] c\"{}\\0A\\00\", align 1\n".format(var, len(v)+2, v)
        ps=str(v)
        ps= ps.replace("\"", "")
        self.f_declerations += "@.str{} = private unnamed_addr constant [{} x i8] c\"{}\\00\", align 1\n".format(var, len(ps)+1,ps)
        return var

    def make_value(self, lit, valueType, line):
        return Value(lit=lit, valueType=valueType, line=line)

    def is_function(self, f_):
        return isinstance(f_, Function)

    def is_array(self, a_):
        return isinstance(a_, Array)

    def is_pointer(self, p_):
        return isinstance(p_, Pointer)

    def is_value(self, v_):
        return isinstance(v_, Value)

    def is_binary(self, bin):
        return isinstance(bin, BinaryOperator)

    def is_unary(self, un):
        return isinstance(un, UnaryOperator)

    def is_logical(self, logic):
        return isinstance(logic, LogicalOperator)

    def to_retrans(self, left, right, op):
        re = dict()
        re[0] = left
        re[1] = right
        re[2] = op
        self.retransverse.append(re)
        return

    def to_retrans_u(self, left, op):
        re = dict()
        re[0] = left
        re[1] = op
        self.retransverse.append(re)
        return

    def set_new_scope(self, t):
        self.old_counter.push(self.var_dic)
        self.transverse_tree(t.root.block)
        self.var_dic = self.old_counter.pop()

    def find_val(self,ci):
        for i in self.var_dic:
            if self.var_dic[i]==ci:
                return i
        return None
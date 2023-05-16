import struct

from src.ast.Program import *
from src.ast.node import *


# todo: vraag is probleem dat conditions output op de fp opslaag??
# en return_function niet in volgorde?

# TODO: DECLARATIONS        v
# TODO: binary OPERATIONS   v
# todo: unary operations    v --> kan niet helemaal getest worden door folding probleem
# TODO: LOOPS               v
# todo: while               v
# todo: if /else            v
# TODO: POINTERS
# todo :UNNAMED SCOPES      v --> vraag als dit ok is?
# TODO: function return     v
# TODO: PRINT
# TODO: SCAN
# TODO: ARRAYS
# todo : function calls
# TODO: modulo

class Mips:
    def __init__(self, program_: program):
        self.c_function = None
        self.loop = None
        self.declaration = None
        self.program = program_
        self.output = ""
        self.data = ".data\n"
        self.data_count = 0
        self.text = ".text\n"
        self.text += ".globl main\n"
        self.text += "j main\n"
        # counter for temporary registers
        self.temp_count = 0
        # keep used registers
        self.register = dict()
        self.frame_register = dict()
        self.frame_counter = -4
        self.data_dict = dict()
        self.save_old_val = None
        self.loop_counter = 0

    def float_to_64bit_hex(self, x):
        # print("x is none in scope:" + self.c_function.root.f_name)
        if isinstance(x, str):
            x = float(x)
        bytes_of_x = struct.pack('>f', x)
        x_as_int = struct.unpack('>f', bytes_of_x)[0]
        x_as_double = struct.pack('>d', x_as_int).hex()
        x_as_double = '0x' + x_as_double
        return x_as_double

    def new_temp(self):
        self.temp_count += 1
        return "$t" + str(self.temp_count)

    def write_to_file(self, filename: str):
        text_file = open(filename, "w")
        text_file.write(self.output)
        text_file.close()

    def get_mars_type(self, type_: LiteralType):
        if type_ == LiteralType.INT or type_ == LiteralType.BOOL:
            return ".word"
        if type_ == LiteralType.FLOAT:
            return ".float"
        if type_ == LiteralType.CHAR:
            return ".byte"

    def get_value_content(self, value: Value):
        content = value.getValue()
        if value.getType() == LiteralType.BOOL:
            if value.getValue() == "True":
                content = "0"
            else:
                content = "1"
        return content

    def get_sw_type(self, value: Value):
        if isinstance(value, Pointer):
            return "sw"
        if value.getType() == LiteralType.INT:
            return "sw"
        if value.getType() == LiteralType.FLOAT:
            return "s.s"
        if value.getType() == LiteralType.BOOL:
            return "s.b"

    def get_register(self, v: Value):
        return 1

    def get_next_highest_register_type(self, type: str, v: Value):
        # get highest register
        if self.register.__len__() == 0:
            self.register[v.getValue()] = type + "0"
            return type + "0"
        a = {k: v for k, v in self.register.items() if v.startswith(type)}
        if a.__len__() == 0:
            self.register[v.getValue()] = type + "0"
            return type + "0"
        highest = max({k: v for k, v in self.register.items() if v.startswith(type)}.values())
        # $ end of string \d match digits
        digits = int(re.findall(r'\d+$', highest)[0])
        digits += 1
        self.register[v.getValue()] = type + str(digits)

        return type + str(digits)

    def global_declaration(self, declaration: Declaration):
        content = self.get_value_content(declaration.rightChild)
        self.data += "{}: {} {}\n".format(declaration.leftChild.getValue(),
                                          self.get_mars_type(declaration.leftChild.getType()),
                                          content)
        self.data_count += 1
        self.data_dict[declaration.leftChild.getValue()] = self.data_count
        return

    def global_array(self, array: Array):
        type_ = self.get_mars_type(array.getType())
        self.data += "{}:\n".format(array.value)
        self.data_count += 1
        self.data_dict[array.value] = self.data_count
        for i in array.arrayContent:
            self.data += "  {} {}\n".format(type_, self.get_value_content(i))

    def to_comment(self, comment: Comment):
        if comment.getType() == CommentType.SL:
            self.text += "#"
            self.text += comment.getValue()
            self.text += "\n"
        elif comment.getType() == CommentType.ML:
            self.text += "#"
            for s in comment.value:
                self.text += s
                if s == "\n":
                    self.text += "#"
        return

    def transverse_program(self):
        for tree in self.program.tree.block.trees:
            if isinstance(tree.root, Scope):
                self.transverse_function(tree.root)
            elif isinstance(tree.root, Declaration):
                self.global_declaration(tree.root)
            elif isinstance(tree.root, Array):
                self.global_array(tree.root)
            elif isinstance(tree.root, Comment):
                self.to_comment(tree.root)
                pass
        self.output += self.data
        self.output += self.text

    def transverse_trees(self, cblock: block, branch_count=0, start_loop=0):
        for tree in cblock.trees:
            # don't change tree function permanently
            t = tree
            if not isinstance(t, AST):
                i = AST
                i.root = t
                t = i
            if isinstance(t.root, Declaration) and \
                    (isinstance(t.root.rightChild, Value) or isinstance(t.root.rightChild,Array) or isinstance(t.root.rightChild,Pointer) or isinstance(t.root.rightChild,Function)):
                self.to_declaration(t.root)
            if isinstance(t.root, Comment):
                self.to_comment(t.root)
            elif isinstance(t.root, Print):
                self.to_print(t.root)
            elif isinstance(t.root, Scan):
                self.to_scan(t.root)
            elif isinstance(t.root, Continue):
                self.to_continue(t, branch_count, start_loop)
            elif isinstance(t.root, Break):
                self.to_break(t, branch_count)
            elif isinstance(t.root, While):
                self.set_while_loop(t.root)
            elif isinstance(t.root, If):
                self.set_if_loop(t.root)
            elif isinstance(t.root, Scope):
                self.set_new_scope(t.root)
            elif t is None:
                pass
            else:
                if isinstance(t.root, Declaration):
                    self.declaration = t.root.leftChild
                    if self.declaration.value not in self.register.keys():
                        self.add_to_memory(self.declaration)
                t.root.printTables("random", self)
                self.save_old_val = None
                self.declaration = None
                # clear temporary registers
                self.remove_temps()

    def transverse_function(self, scope: Scope):
        self.text += scope.f_name + ": \n"
        self.c_function = scope
        # stack space
        p = self.set_stack_space(scope)
        p += 4
        return_size = 4
        if self.program.getFunctionTable().findFunction(scope.f_name)["return"] == "BOOL":
            return_size = 1
        p += return_size
        self.text += " sw	$fp, 0($sp)	# push old frame pointer (dynamic link)\n"
        self.text += "move	$fp, $sp	# frame	pointer now points to the top of the stack\n"
        self.text += "subu	$sp, $sp,{}	# allocate bytes on the stack\n".format(p)
        self.text += "sw	$ra, -{}($fp)	# store the value of the return address\n".format(return_size)
        # save parameters function
        self.save_function_variables(scope)
        var_reg = self.register

        # transverse trees
        self.transverse_trees(scope.block)
        # return
        self.set_return_function(scope.f_return, scope.f_name == "main")
        self.c_function = None
        self.remove_register_type('s')
        return

    def save_function_variables(self, scope: Scope):
        # Iterate through the DataFrame
        self.frame_counter = -4
        for index, row in scope.block.getSymbolTable().table.iterrows():
            size = 4
            type_ = row['Type']
            if type_ == LiteralType.BOOL:
                size += 1
                self.frame_counter -= 1
            else:
                self.frame_counter -= 4

            name = index
            reg = "s"
            """if type_ == LiteralType.FLOAT:
                reg = "f"""""
            s = self.get_next_highest_register_type(reg, Value(valueType=type_, lit=name, line=0))
            self.frame_register[s] = str(self.frame_counter) + "($fp)"
            self.text += "sw	${}, {}($fp)\n".format(s, self.frame_counter)
        return self.frame_counter

    # determine space arguments and any local variable needed
    def set_stack_space(self, scope):
        p = 0
        # Iterate through the DataFrame
        for index, row in scope.block.getSymbolTable().table.iterrows():
            # Access the data for each column using the column name
            type_ = row['Type']
            if type_ == LiteralType.BOOL:
                p += 1
            else:
                p += 4
        return p

    def set_return_function(self, f_return: AST, is_main=False):
        # transverse return address
        if f_return is not None and (
                isinstance(f_return.root, BinaryOperator) or isinstance(f_return, UnaryOperator) or isinstance(f_return,
                                                                                                               LogicalOperator)):
            self.declaration = Value("$freturn", self.c_function.return_type, 0)
            #self.add_to_memory(self.declaration)
            self.register["v0"]=self.declaration.value
            f_return.printTables("random", self)
            #self.text += "sw ${}, $ra\n".format(self.register[self.declaration.value])
        elif isinstance(f_return.root, Value):
            self.load_retrun_value(f_return.root)
        elif isinstance(f_return, Array):
            pass
        elif isinstance(f_return, Pointer):
            pass
        elif isinstance(f_return, Function):
            pass

        """for key in reversed(reg.keys()):
            self.text += "lw	${}, {}($fp)\n".format(reg[key], min_counter)
            min_counter += 4"""
        for key in reversed(self.frame_register):
            self.text += "lw ${}, {}\n".format(key, self.frame_register[key])
        self.text += "lw	$ra, -4($fp)\n"
        self.text += "move	$sp, $fp\n"
        self.text += "lw	$fp, ($sp)\n"

        if f_return is None or is_main:
            self.text += "li  $v0,10\n"
            self.text += "syscall\n"
        else:
            self.text += "jr	$ra\n"

    def load_retrun_value(self, v):
        if v.getType() == LiteralType.INT and str(v.value).isdigit():
            self.text += "li $v0, {}\n".format(v.value)

        elif v.getType() == LiteralType.FLOAT and is_float(v.value):
            self.text += "ori $v0,$0,{}\n".format(self.float_to_hex(v.value))
        elif v.getType() == LiteralType.CHAR:
            self.data_count += 1
            self.data_dict[v.value] = self.data_count
            self.data += "$${}  : .byte {} \"\n".format(self.data_count, v.value)
            self.text += "lb $t0 , $${}\n".format(self.data_count)
            self.text += "move $v0,$t0\n"
        else:
            self.text += "lw $t0, {}\n".format( self.frame_register[self.register[v.value]])
            self.text += "move $v0,$t0\n"


    def to_print(self, p: Print):
        print("print called")
        # split syscall to %i
        strings = p.input_string.split("%")
        pi = 0
        for i in strings:
            if i[-1] == "\"":
                continue
            if i not in self.data_dict:
                self.data_count += 1
                self.data_dict[i] = self.data_count
                self.data += "$${}  :.asciiz {} \"\n".format(self.data_count, i)
            # load varialbe in $a0
            # self.text += "lw $a0, integer_value"
            self.text += "li $v0, 4\n"
            self.text += "la $a0, $${}\n".format(self.data_count)
            self.text += "syscall\n"
            pi += 1

    def print_load(self, v):
        result = 0
        if isinstance(v, String):
            self.data_count += 1
            self.data_dict[v.value] = self.data_count
            self.data += "$${}  :.asciiz {} \n".format(self.data_count, v.value)
            result = "$${}" + str(self.data_count)
        elif isinstance(v, Value):
            if isinstance(v.getType() == LiteralType.VAR):
                reg = self.register[v.value]
            else:
                self.text += "li $t0, {}\n".format(v.value)

    def to_scan(self, Scan):
        pass

    def to_continue(self, t: Continue, branch_count, start_loop):
        pass

    def to_break(self, t: Break, branch_count):
        pass

    def set_while_loop(self, w: While):
        self.loop_counter += 1
        condition = "loop{}".format(self.loop_counter)
        self.loop_counter += 1
        ctrue = "loop{}".format(self.loop_counter)
        self.loop_counter += 1
        cfalse = "loop{}".format(self.loop_counter)
        self.deel1_condition(w, condition, cfalse, ctrue)
        self.text += "nop \n"
        self.text += "j ${}\n".format(ctrue)
        self.text += "nop\n"
        # if true
        self.text += "${}:\n".format(ctrue)
        self.transverse_trees(w.c_block)
        self.text += "j ${}\n".format(condition)
        self.text += "nop\n"
        self.text += "${}:\n".format(cfalse)

        # remove the temps
        self.register = {key: value for key, value in self.register.items() if not value.isdigit()}
        return

    def set_if_loop(self, f: If):
        if isinstance(f, If) and f.operator == ConditionType.IF:
            self.loop_counter += 1
            condition = "loop{}".format(self.loop_counter)
            self.loop_counter += 1
            ctrue = "loop{}".format(self.loop_counter)
            self.loop_counter += 1
            cfalse = "loop{}".format(self.loop_counter)
            self.deel1_condition(f, condition, cfalse, ctrue)
            # jump to rest of function

            self.text += "nop \n"
            self.text += "j ${}\n".format(ctrue)
            self.text += "nop\n"
            # if true
            self.text += "${}:\n".format(ctrue)
            self.transverse_trees(f.c_block)

            self.text += "j ${}\n".format(cfalse)
            self.text += "${}:\n".format(cfalse)

        elif isinstance(f, If) and f.operator == ConditionType.ELSE:
            # remove last two lines
            lines = self.text.splitlines()  # Split the string into a list of lines
            lines_without_last_two = lines[:-2]  # Remove the last two lines
            self.text = '\n'.join(lines_without_last_two)  # Join the lines back into a string
            lines = self.text.splitlines()  # Split the string into a list of lines
            lines_without_last_two = lines[:-1]  # Remove the last two lines
            self.text = '\n'.join(lines_without_last_two)

            self.text += "\n"
            celse = "loop{}".format(self.loop_counter)
            self.loop_counter += 1
            cfalse = "loop{}".format(self.loop_counter)
            print(cfalse)
            self.text += "j ${}\n".format(cfalse)
            self.text += "${}:\n".format(celse)
            self.transverse_trees(f.c_block)
            self.text += "j ${}\n".format(cfalse)
            self.text += "nop\n"
            self.text += "${}:\n".format(cfalse)




        elif isinstance(f, If) and f.operator == ConditionType.ELIF:
            pass

    def deel1_condition(self, f, condition, cfalse, ctrue):
        self.text += "j ${}\n".format(condition)
        self.text += "nop\n"
        self.text += "${}:\n".format(condition)

        self.declaration = Value(condition, LiteralType.BOOL, 0)
        self.get_next_highest_register_type('', self.declaration)
        key = self.register[self.declaration.value]
        self.add_to_frame_register(key)
        f.Condition.printTables("random", self)
        fr = self.frame_register[self.register[self.declaration.value]]
        sr = self.register[self.declaration.value]
        self.declaration = None
        self.text += "lbu ${}, {}\n".format(sr, fr)
        self.text += "andi  ${}, ${}, 1\n".format(sr, sr)
        self.text += "beqz    ${}, ${}\n".format(sr, cfalse)
        return cfalse

    def set_new_scope(self, t: Scope):
        self.transverse_trees(t.block)

    def add_to_frame_register(self, key):
        self.frame_counter -= 4
        self.frame_register[key] = str(self.frame_counter) + "($fp)"

    def to_declaration(self, declaration: Declaration):
        # find register it is stored
        # store it
        if isinstance(declaration.rightChild,Pointer):
            return self.to_pointer_dec(declaration)
        if isinstance(declaration.rightChild,Array):
            return self.to_array_dec(declaration)
        if isinstance(declaration.rightChild,Function):
            return self.to_function_dec(declaration)
        s = self.register[declaration.leftChild.value]
        f = self.frame_register[self.register[declaration.leftChild.value]]
        self.text += "lw  ${}, {}\n".format(s, f)
        if declaration.rightChild.getType() == LiteralType.INT and str(declaration.rightChild.value).isdigit():
            self.text += "ori ${},$0,{}\n".format(self.register[declaration.leftChild.value],
                                                  declaration.rightChild.value)
            self.text += "sw  ${}, {}\n".format(s, f)
        elif declaration.rightChild.getType() == LiteralType.FLOAT and is_float(str(declaration.rightChild.value)):
            self.text += "ori ${},$0,{}\n".format(self.register[declaration.leftChild.value],
                                                  self.float_to_hex(declaration.rightChild.value))
            self.text += "sw  ${}, {}\n".format(s, f)

        elif declaration.rightChild.getType() == LiteralType.BOOL and (
                declaration.rightChild == 'True' or declaration.rightChild == 'False'):
            if declaration.rightChild == 'True':
                self.text += "ori {},$0,1\n".format(self.register[declaration.leftChild.value])
                self.text += "sw  ${}, {}\n".format(s, f)
            else:
                self.text += "ori {},$0,0\n".format(self.register[declaration.leftChild.value])
                self.text += "sw  ${}, {}\n".format(s, f)
        else:
            s1 = self.register[declaration.rightChild.value]
            f1 = self.frame_register[s1]
            # self.text += "lw ${} ,{} \n".format(s, f)
            self.text += "sw ${}, {}\n".format(s, f1)

        return

    def float_to_hex(self, float_num):
        if isinstance(float_num, str):
            float_num = float(float_num)
        # Pack the float as a single-precision (32-bit) binary representation
        binary_data = struct.pack('!f', float_num)

        # Unpack the binary data as a 32-bit unsigned integer
        int_value = struct.unpack('!I', binary_data)[0]

        # Convert the integer to a hexadecimal string
        hex_value = hex(int_value)

        return hex_value

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

    def remove_temps(self):
        self.register = {key: value for key, value in self.register.items() if not value.startswith('t')}
        return

    def remove_register_type(self, type: str):
        self.register = {key: value for key, value in self.register.items() if not value.startswith(type)}
        return

    def add_to_memory(self, declaration):
        self.get_next_highest_register_type("s", declaration)
        self.frame_counter -= 4
        self.frame_register[self.register[declaration.value]] = str(self.frame_counter) + "($fp)"
        self.text += "sw ${}, {}($fp)\n".format(self.register[declaration.value], self.frame_counter)

    def to_pointer_dec(self, declaration):
        return

    def to_array_dec(self, declaration):
        return

    def to_function_dec(self, declaration):
        #pass function paramerters

        #jal function
        #save return value
        return


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

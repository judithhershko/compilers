import struct

from src.HelperFunctions import stack
from src.ast.Program import *
from src.ast.node import *

"""
print implementatie:

https://gist.github.com/KaceCottam/37a065a2c194c0eb50b417cf67455af1

"""


# todo: vraag is probleem dat conditions output op de fp opslaag??
# en return_function niet in volgorde?
# TODO: DECLARATIONS        v
# TODO: binary OPERATIONS   v
# todo: unary operations    v --> kan niet helemaal getest worden door folding probleem
# TODO: LOOPS               v
# todo: while               v
# todo: if /else            v
# todo :UNNAMED SCOPES      v --> vraag als dit ok is?
# TODO: function return     v
# TODO: pointers            x
# TODO: PRINT               x
# TODO: SCAN                x
# TODO: ARRAYS              x
# todo : function calls     v
# TODO: modulo              x
# todo: conversions int    ->float/bool->int in helper  x
# todo function forward declaration skippen v

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
        self.reused_registers = dict()

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
        if digits >= 7:
            """
            need to reuse a register
            set everything of this type in memory
            save the values inn reused registers
            remove them from registers
            call function again
            """
            if type == 's':
                self.text += "push everything in memory to reuse registers \n"
                for k, v in self.register.items():
                    if v.startswith(type):
                        self.reused_registers[v] = self.frame_register[v]
                        self.text += "sw {}, {}\n".format(v, self.frame_register[v])
                self.remove_register_type(type)
                return self.get_next_highest_register_type(type, v)
            elif type == 't':
                self.remove_register_type('t')
                return self.get_next_highest_register_type(type, v)

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
            if isinstance(tree.root, Scope) and not tree.root.forward_declaration:
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
                    (isinstance(t.root.rightChild, Value) or isinstance(t.root.rightChild, Array) or isinstance(
                        t.root.rightChild, Pointer) or isinstance(t.root.rightChild, Function) or isinstance(
                        t.root.rightChild, EmptyNode)):
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
        self.text += " sw	$fp, 0($sp)\n"
        self.text += "move	$fp, $sp\n"
        self.text += "subu	$sp, $sp,{}\n".format(p)
        self.text += "sw	$ra, -{}($fp)\n".format(return_size)
        # save parameters function
        self.save_function_variables(scope)
        var_reg = self.register

        # transverse trees
        self.transverse_trees(scope.block)
        # return
        self.set_return_function(scope.f_return, scope.f_name == "main")
        self.c_function = None
        self.remove_register_type('s')
        self.reused_registers = dict()
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
            if type_ == LiteralType.FLOAT:
                reg = "f"
                self.get_next_highest_register_type(reg, Value(valueType=type_, lit=name, line=0))
            else:
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
        if f_return is None:
            return self.end_function(True)
        if isinstance(f_return.root, BinaryOperator) or isinstance(f_return, UnaryOperator) or isinstance(f_return,
                                                                                                          LogicalOperator):
            self.declaration = Value("$freturn", self.c_function.return_type, 0)
            # self.add_to_memory(self.declaration)
            self.register["v0"] = self.declaration.value
            f_return.printTables("random", self)
            # self.text += "sw ${}, $ra\n".format(self.register[self.declaration.value])
        elif isinstance(f_return.root, Value):
            self.load_retrun_value(f_return.root)
        elif isinstance(f_return, Array):
            pass
        elif isinstance(f_return, Pointer):
            pass
        elif isinstance(f_return, Function):
            pass
        self.end_function(is_main)

    def end_function(self, void: bool):
        for key in reversed(self.frame_register):
            self.text += "lw ${}, {}\n".format(key, self.frame_register[key])
        self.text += "lw	$ra, -4($fp)\n"
        self.text += "move	$sp, $fp\n"
        self.text += "lw	$fp, ($sp)\n"
        if void:
            self.text += "li  $v0,10\n"
            self.text += "syscall\n"
        else:
            self.text += "jr	$ra\n"
    def load_float(self, val):
        self.load_float(val)
        s = self.get_register(val, 'f', LiteralType.FLOAT)
        self.text += "lwc1 ${}, $${}\n".format(s, self.data_count)
        return s
    def load_retrun_value(self, v):
        if v.getType() == LiteralType.INT and str(v.value).isdigit():
            self.text += "li $v0, {}\n".format(v.value)

        elif v.getType() == LiteralType.FLOAT and is_float(v.value):
            #self.text += "ori $v0,$0,{}\n".format(self.float_to_hex(v.value))
            self.load_float(v.value)
            self.text += "mov.s $f0, ${}\n".format(self.get_register(v.value,'f',LiteralType.FLOAT))
        elif v.getType() == LiteralType.CHAR:
            self.data_count += 1
            self.data_dict[v.value] = self.data_count
            self.data += "$${}  : .byte {} \"\n".format(self.data_count, v.value)
            self.text += "lb $t0 , $${}\n".format(self.data_count)
            self.text += "move $v0,$t0\n"
        else:
            self.text += "lw $t0, {}\n".format(self.frame_register[self.register[v.value]])
            self.text += "move $v0,$t0\n"

    def print_nr(self, type):
        if type == LiteralType.INT:
            return 1
        if type == LiteralType.FLOAT:
            return 2
        if type == LiteralType.BOOL:
            return 1
        if type == LiteralType.CHAR:
            return 11

    def load_float(self, fl):
        if isinstance(fl, str):
            fl = float(fl)
        self.data_count += 1
        self.data += "$${}: .float {}\n".format(self.data_count, fl)
        return self.data_count

    def to_print(self, p: Print):
        print("print called")
        # split syscall to %i
        strings = p.input_string.split("%")
        pi = 0
        for i in strings:
            if i[-1] == "\"":
                continue
            i=str(i)
            self.data_count += 1
            self.data_dict[i] = self.data_count
            front=""
            back=""
            if i != strings[0]:
                i = i[1:]
            if i[0]!="\"" or i[0]!='\"':
                front="\""
            if i[-1] != "\"" or i[-1] != '\"':
                back = "\""

            self.data += "$${}  :.asciiz {} {} {} \n".format(self.data_count,front, i,back)
            self.text += "li $v0, 4\n"
            self.text += "la $a0, $${}\n".format(self.data_count)
            self.text += "syscall\n"
            # input value to print:
            inp = p.paramString[pi]
            print_ = self.set_print_type(inp)
            print_nr = 4
            if print_ is not None:
                print_nr = self.print_nr(print_.type)
            if print_ is None or print_.type == LiteralType.CHAR:
                # is string
                self.data_count += 1
                self.data_dict[i] = self.data_count
                self.data += "$${}  :.asciiz {} \n".format(self.data_count, p.param[pi].value)
                self.text += "li $v0, 4\n"
                self.text += "la $a0, $${}\n".format(self.data_count)
                self.text += "syscall\n"
                continue
            elif isinstance(p.param[pi], tuple):
                p.param[pi] = p.param[pi][0]
            if isinstance(p.param[pi].root, Value):
                self.text += "li $v0, {}\n".format(print_nr)
                # float
                if p.param[pi].root.type == LiteralType.FLOAT and is_float(str(p.param[pi].root.value)):
                    s = self.get_register(print_.value, 'f', print_.type)
                    self.load_float(p.param[pi].root.value)
                    self.text += "lwc1 ${}, $${}\n".format(s,self.data_count)
                # int
                elif str(p.param[pi].root.value).isdigit():
                    print_.value = p.param[pi].root.value
                    s = self.get_register(print_.value, 't', print_.type)
                    val = p.param[pi].root.value
                    self.text += "ori ${}, {}\n".format(s, val)
                # var
                else:
                    s = self.get_register(p.param[pi].root.value, 's', p.param[pi].root.type)

                if print_.type == LiteralType.FLOAT:
                    self.text += "mov.s $f12, ${}\n".format(s)
                else:
                    self.text += "move $a0, ${}\n".format(s)
                self.text += "syscall\n"

                # Lload value +syscall
            elif isinstance(p.param[pi].root, Array):
                pass
            elif isinstance(p.param[pi].root, Pointer):
                pass
            elif isinstance(p.param[pi].root, UnaryOperator) or isinstance(p.param[pi].root,
                                                                           BinaryOperator) or isinstance(
                    p.param[pi].root, LogicalOperator):
                self.declaration = print_
                self.add_to_memory(self.declaration)
                p.param[pi].printTables("random", self)
                s = self.get_register(self.declaration.value, 's', self.declaration.type)
                self.text += "li $v0, {}\n".format(print_nr)
                if print_.type == LiteralType.FLOAT:
                    self.text += "mov.s $f12, ${}\n".format(s)
                else:
                    self.text += "move $a0, ${}\n".format(s)
                self.text += "syscall\n"
                self.save_old_val = None
                self.declaration = None
                self.remove_temps()
            pi += 1

    def set_print_type(self, type_):
        if type_ == '%c':
            return Value(lit='$print', line=0, valueType=LiteralType.CHAR)
        if type_ == '%d':
            return Value(lit='$print', line=0, valueType=LiteralType.INT)
        if type_ == '%s':
            return None
        if type_ == '%i':
            return Value(lit='$print', line=0, valueType=LiteralType.INT)
        if type_ == '%f':
            return Value(lit='$print', line=0, valueType=LiteralType.FLOAT)

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
    def remove_register(self, key):
        del self.register[key]
        return
    def get_register(self, v, type_='s', value_type=LiteralType.INT):
        if type_ == 's' and value_type == LiteralType.FLOAT:
            type_ = 'f'
        if v in self.register.keys():
            return self.register[v]
        if v in self.reused_registers.keys():
            s = self.get_next_highest_register_type(type_, Value(valueType=value_type, lit=v, line=0))
            self.text += "sw ${}, {}\n".format(s, self.reused_registers[v])
            return s
        # not in keys:
        s = self.get_next_highest_register_type(type_, Value(valueType=value_type, lit=v, line=0))
        if type_ != 't' and type_ != 'f':
            self.frame_register[s] = str(self.frame_counter) + "($fp)"
            self.text += "sw ${}, {}($fp)\n".format(s, self.frame_counter)
        return s

    def get_register_type(self, type_):
        if type_ == LiteralType.INT:
            return 's'
        if type_ == LiteralType.FLOAT:
            return 'f'
        if type_ == LiteralType.BOOL:
            return 's'
        if type_ == LiteralType.CHAR:
            return None

    def to_declaration(self, declaration: Declaration):
        # find register it is stored
        # store it
        if isinstance(declaration.rightChild, Pointer):
            return self.to_pointer_dec(declaration)
        if isinstance(declaration.rightChild, Array):
            return self.to_array_dec(declaration)
        if isinstance(declaration.rightChild, Function):
            return self.to_function_dec(declaration.rightChild, declaration.leftChild, True)
        s = self.get_register(declaration.leftChild.value, self.get_register_type(declaration.leftChild.getType()),
                              declaration.leftChild.getType())
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
            """
            char needs to be saved in .data fragment
            """
            # check if needs data element:
            if declaration.leftChild.getType() == LiteralType.CHAR:
                self.data_count += 1
                self.data_dict[declaration.leftChild.value] = self.data_count
                self.data += "$${}  : .byte '{}' \n".format(self.data_count, declaration.leftChild.value)
                s = self.get_register(declaration.leftChild.value, 's', LiteralType.CHAR)
                self.text += "lb ${} , $${}\n".format(s, self.data_count)
                self.text += "sb ${}, {}\n".format(s, self.frame_register[self.register[declaration.leftChild.value]])

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

    def to_function_dec(self, f, var, save_mem=False):
        # pass function paramerters
        # jal function
        # save return value
        if var.value not in self.register.keys():
            self.get_next_highest_register_type('t', var)
        for i in f.param:
            self.load_type(f.param[i], True)
        self.text += "jal {}\n".format(f.f_name)
        # self.text += "sw $v0, {}\n".format(d.rightChild.f_name)
        if var.type==LiteralType.FLOAT:
            self.text += "mov.s ${}, $f0\n".format(self.register[var.value])
        else:
            self.text += "move ${}, $v0\n".format(self.register[var.value])
        if save_mem and self.register[var.value][0]=='s':
            self.text += "sw ${}, {}\n".format(self.register[var.value], self.frame_register[self.register[var.value]])

        return

    def load_type(self, v, is_param: bool):
        save = "t"
        if isinstance(v, Pointer):
            pass
        if isinstance(v, Array):
            pass
        if is_param:
            save = 'a'
        if isinstance(v, Value) and v.getType() == LiteralType.INT and str(v.value).isdigit():
            self.get_next_highest_register_type(save, v)
            self.text += "ori ${}, $zero, {}\n".format(self.register[v.value], v.value)
        elif isinstance(v, Value) and v.getType() == LiteralType.FLOAT and is_float(v.value):
            if is_param:
                save = 'f'
            s = self.get_next_highest_register_type(save, v)
            self.load_float(v.value)
            self.remove_register(v.value)
            si = self.get_register(v.value, 'a', v.type)
            self.text += "lwc1 ${}, $${}\n".format(s, self.data_count)
            self.text += "mfc1 ${}, ${}\n".format(si,s)
            #self.text += "ori ${}, $zero, {}\n".format(self.register[v.value], self.float_to_hex(v.value))
        elif isinstance(v, Value) and v.getType() == LiteralType.CHAR and v.value[0] == '\'':
            self.data_count += 1
            self.data_dict[v.value] = self.data_count
            self.data += "$${}  : .byte {} \"\n".format(self.data_count, v.value)
            self.text += "lb ${} , $${}\n".format(self.register[v.value], self.data_count)
        elif isinstance(v, Value):
            self.text += "lw ${}, {}\n".format(self.register[v.value], self.frame_register[self.register[v.value]])

    def make_value(self, lit, valueType, line):
        return Value(lit=lit, valueType=valueType, line=line)


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

from src.ast.Program import *
from src.ast.node import *


class Mips:
    def __init__(self, program_: program):
        self.program = program_
        self.output = ""
        self.data = ".data\n"
        self.text = ".text\n"
        self.text += ".globl main\n"
        # counter for temporary registers
        self.temp_count = 0
        # keep used registers
        self.register = dict()

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
        return

    def global_array(self, array: Array):
        type_ = self.get_mars_type(array.getType())
        self.data += "{}:\n".format(array.value)
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

    def transverse_trees(self):
        for tree in self.program.tree.block.trees:
            if isinstance(tree.root, Scope):
                self.transverse_function(tree.root)
            elif isinstance(tree.root, Declaration):
                self.global_declaration(tree.root)
            elif isinstance(tree.root, Array):
                self.global_array(tree.root)
            elif isinstance(tree.root, Comment):
                self.global_comment(tree.root)
                pass

    def transverse_function(self, scope: Scope):
        self.text += scope.f_name + ": \n"
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
        # transverse trees
        # return
        self.set_return_function(scope.f_return, scope.f_name == "main")

    def save_function_variables(self, scope: Scope):
        # Iterate through the DataFrame
        counter = -4
        for index, row in scope.block.getSymbolTable().table.iterrows():
            size = 4
            type_ = row['Type']
            if type_ == LiteralType.BOOL:
                size += 1
                counter -= 1
            else:
                counter -= 4

            name = row['Value']
            s = self.get_next_highest_register_type("s", Value(valueType=type_, lit=name, line=0))
            self.text += "sw	${}, {}($fp)\n".format(s, counter)

    def function_parameters(self, parameters):
        # function start
        p = 0
        self.text += "#fucntion parameters\n"
        # save values
        for par in parameters:
            t = "a"
            if parameters[par] == LiteralType.FLOAT:
                t = "f"
            self.text += "{} ${}, {}($sp)\n".format(self.get_sw_type(parameters[par]),
                                                    self.get_next_highest_register_type(t, parameters[par]), p)
            if parameters[par].getType() == LiteralType.BOOL:
                p += 1
            else:
                p += 4
        return p

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
        print(p)
        return p

    def set_return_function(self, f_return: AST, is_main=False):

        if f_return is None:
            return
        if is_main:
            self.text += "li  $v0,10\n"
            self.text += "syscall\n"

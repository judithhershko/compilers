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
    def get_register(self,v:Value):
        return 1

    def global_declaration(self, declaration: Declaration):
        content = self.get_value_content(declaration.rightChild)
        self.data += "{}: {} {}\n".format(declaration.leftChild.getValue(),
                                          self.get_mars_type(declaration.leftChild.getType()),
                                          content)
        return

    def global_array(self, array: Array):
        type_ = self.get_mars_type(array.getType())
        self.data += "{}:\n".format(array.getValue())
        for i in array.arrayContent:
            self.data += "  {} {}\n".format(type_, self.get_value_content(i))

    def global_comment(self, comment: Comment):
        self.data += "# {}\n".format(comment.getValue())

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
                # self.global_comment(tree.root)
                pass
        self.output += self.data
        self.output += self.text

    def transverse_function(self, scope: Scope):
        self.text += scope.f_name + ": \n"
        self.function_parameters(scope.parameters)

    def function_parameters(self, parameters):
        # function start
        p = -1 * len(parameters) * 4
        self.text += "addi $sp, $sp, {}        # allocate space for arguments on stack\n".format(p)
        p = -1 * p - 4
        self.text += "sw $ra, {}($sp)           # save return address on stack\n".format(p)
        p = p - 5
        self.text += "sw $fp, {}($sp)          # save frame pointer on stack\n".format(p)
        p = len(parameters) * 4
        self.text += "addi $fp, $sp, {}         # set up new frame pointer\n".format(p)
        self.text += "#fucntion parameters\n"
        # save values
        for par in parameters:
            self.text += "{} ${}, {}($fp)\n".format(self.get_sw_type(parameters[par]), self.get_register(parameters[par]), p)
            p += 4
        # save addresses

        # function body

        # function end

        """
        
f:
    addi $sp, $sp, -16        # allocate space for 4 arguments on stack
    sw $ra, 12($sp)           # save return address on stack
    sw $fp, 8($sp)            # save frame pointer on stack
    addi $fp, $sp, 16         # set up new frame pointer
    sw $a0, 16($fp)           # save value of x on stack
    s.s $f12, 20($fp)         # save value of y on stack
    sb $a2, 24($fp)           # save value of z on stack
    sw $a1, 28($fp)           # save address of xp on stack
    sw $a3, 32($fp)           # save address of fp on stack
    sw $a2, 36($fp)           # save address of zp on stack

    # function body
    li $v0, 1                 # return 1
    
    # function epilogue
    lw $ra, 12($sp)           # restore return address from stack
    lw $fp, 8($sp)            # restore frame pointer from stack
    addi $sp, $sp, 16         # deallocate space for 4 arguments on stack
    jr $ra                    # return to caller

        """

from src.ast.Program import *
from src.ast.node import *


class Mips:
    def __init__(self, program_: program):
        self.program = program_
        self.output = ""
        self.data = ".data\n"
        self.text = ".text\n"

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
                #self.global_comment(tree.root)
                pass
        self.output += self.data
        self.output += self.text

    def transverse_function(self, scope: Scope):
        pass

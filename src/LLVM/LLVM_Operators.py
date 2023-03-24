import ast

from src.ast import AST
from src.ast.SymbolTable import SymbolTable
from src.ast.node import Declaration, Value, LiteralType, Comment, CommentType, Print
from src.ast.block import block


class ToLLVM():
    def __init__(self):
        self.allocate = ""

    def STable_to_LLVM(self, table: SymbolTable):
        for entry in table:
            line = ""

    def transverse_block(self, cblock: block):
        for tree in cblock.trees:
            if isinstance(tree.root, Declaration):
                self.to_declaration(tree)
            elif isinstance(tree.root, Comment):
                self.to_comment(tree)
            elif isinstance(tree.root,Print):
                pass


    def write_to_file(self, filename: str):
        # open text file
        filename = "generated/output/" + filename

        text_file = open(filename, "w")
        # write string to file
        text_file.write(self.allocate)

        # close file
        text_file.close()

    def switch_Literals(self, v: Value, input: Value):
        # comment above with original code:
        const = ""
        type = ""
        if v.const:
            const = "const"
        if v.type == LiteralType.NUM or v.type == LiteralType.INT:
            self.allocate += "// {} {} {} = {}\n".format(const, "int", v.value, input.value)
            self.allocate += "@{}= global i32 {}, align 4\n".format(v.value, input.value)
        elif v.type == LiteralType.FLOAT:
            self.allocate += "// {} {} {} = {}\n".format(const, "float", v.value, input.value)
            self.allocate += "@{} = global float {}, align 4\n".format(v.value, input.value)
        elif v.type == LiteralType.STR:
            size = len(input.value)
            self.allocate += "// {} {} {} = {}\n".format(const, "char", v.value, input.value)
            self.allocate += "@{} = global [{}xi8] c{}, align 1\n".format(v.value, size, input.value)
        elif v.type == LiteralType.BOOL:
            bval = 0
            if input.value == "True":
                bval = 1
            self.allocate += "@{} = global i1 {}, align 4\n".format(v.value, bval)

    def to_bin_operator(self, ast: AST):
        pass

    def to_declaration(self, ast: AST):
        if isinstance(ast.root, Declaration):
            return self.switch_Literals(ast.root.leftChild, ast.root.rightChild)
        return

    def to_comment(self, ast: AST):

        if isinstance(ast.root,Comment):
            if ast.root.type==CommentType.SL:
                self.allocate+=ast.root.value
                self.allocate+="\n"
            elif ast.root.type==CommentType.ML:
                self.allocate += "//"
                for s in ast.root.value:
                    self.allocate += s
                    if s == "\n":
                        self.allocate+="//"
        self.allocate+="\n"


    def to_print(self, ast: AST):
        # len=len+1 van de variabele die je wilt meegeven
        # cast momenteel naar een char

        pass

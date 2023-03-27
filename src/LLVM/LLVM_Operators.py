import ast

from src.ast import AST
from src.ast.SymbolTable import SymbolTable
from src.ast.node import Declaration, Value, LiteralType, Comment, CommentType, Print
from src.ast.block import block


class ToLLVM():
    def __init__(self):
        self.global_ = ""
        self.allocate = ""
        self.store = ""

    def STable_to_LLVM(self, table: SymbolTable):
        for entry in table:
            line = ""

    def transverse_block(self, cblock: block, main=True):
        if main:
            for tree in cblock.trees:
                if isinstance(tree.root, Declaration):
                    self.to_declaration(tree)
                elif isinstance(tree.root, Comment):
                    self.to_comment(tree)
                elif isinstance(tree.root, Print):
                    pass

        for tree in cblock.trees:
            if isinstance(tree.root, Declaration):
                self.to_declaration(tree)
            elif isinstance(tree.root, Comment):
                self.to_comment(tree)
            elif isinstance(tree.root, Print):
                pass

    def write_to_file(self, filename: str):
        # open text file
        filename = "generated/output/" + filename

        text_file = open(filename, "w")
        # write string to file
        text_file.write(self.global_)

        # close file
        text_file.close()

    def switch_Literals(self, v: Value, input: Value):
        # comment above with original code:
        const = ""
        type = ""
        if v.const:
            const = "const"
        if v.type == LiteralType.NUM or v.type == LiteralType.INT:
            self.global_ += "// {} {} {} = {}\n".format(const, "int", v.value, input.value)
            self.allocate += "// {} {} {} = {}\n".format(const, "int", v.value, input.value)
            self.global_ += "@{}= global i32 {}, align 4\n".format(v.value, input.value)
            self.allocate += "%{} = alloca i32, align 4\n"
            self.store += "store i32 {}, i32* %{}, align 4\n".format(input.value, v.value)

        elif v.type == LiteralType.FLOAT:
            self.global_ += "// {} {} {} = {}\n".format(const, "float", v.value, input.value)
            self.allocate += "// {} {} {} = {}\n".format(const, "float", v.value, input.value)
            self.allocate+= "%{} = alloca float, align 4\n".format(v.value)

            self.global_ += "@{} = global float {}, align 4\n".format(v.value, input.value)
            self.store+="store float {}, float* %{}, align 4\n".format(input.value,v.value)

        elif v.type == LiteralType.STR:
            size = len(input.value)
            self.global_ += "// {} {} {} = {}\n".format(const, "char", v.value, input.value)
            self.allocate+= "// {} {} {} = {}\n".format(const, "char", v.value, input.value)
            self.allocate+=  "%{} = alloca i8, align 1\n".format(v.value)

            self.global_ += "@{} = global [{}xi8] c{}, align 1\n".format(v.value, size, input.value)
            num = ord(input.value)
            self.store+="store i8 {}, i8* %{}, align 1\n".format(num,v.value)

        elif v.type == LiteralType.BOOL:
            bval = 0
            if input.value == "True":
                bval = 1
            self.allocate+="// {}{}{}={}\n".format(const,"_Bool",v.value,input.value)
            self.allocate+="%{} = alloca i8, align 1\n".format(v.value)

            self.global_ += "@{} = global i1 {}, align 4\n".format(v.value, bval)
            self.store+="store i8 {}, i8* %{}, align 1\n".format(bval,v.value)

    def to_bin_operator(self, ast: AST):
        pass

    def to_declaration(self, ast: AST):
        if isinstance(ast.root, Declaration):
            return self.switch_Literals(ast.root.leftChild, ast.root.rightChild)
        return

    def to_comment(self, ast: AST):

        if isinstance(ast.root, Comment):
            if ast.root.type == CommentType.SL:
                self.global_ += ast.root.value
                self.store+=ast.root.value
                self.global_ += "\n"
                self.store+="\n"
            elif ast.root.type == CommentType.ML:
                self.global_ += "//"
                self.store += "//"
                for s in ast.root.value:
                    self.global_ += s
                    self.store += s
                    if s == "\n":
                        self.global_ += "//"
                        self.store += "//"
        self.global_ += "\n"
        self.store += "\n"

    def to_print(self, ast: AST):
        # len=len+1 van de variabele die je wilt meegeven
        # cast momenteel naar een char
        var="x"
        #check if variable in table:
        #if yes/ add 1 loop
        #if not:
        self.store+="%{} = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %3)"
        pass

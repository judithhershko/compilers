import ast

from src.ast import AST
from src.ast.SymbolTable import SymbolTable
from src.ast.node import Declaration, Value, LiteralType, Comment, CommentType, Print, Pointer
from src.ast.block import block

# TODO:
"""
- pointers
v getallen
- print f
- testen of geen errors komen
v niet global scope nemen
v dictionary gebruiken !
"""


class ToLLVM():
    def __init__(self):
        self.global_ = ""
        self.allocate = ""
        self.store = ""
        self.couter = 0
        self.var_dic = dict()
        self.main=True
        self.g_count=0
        self.g_assignment=""
        self.f_declerations=""

    def STable_to_LLVM(self, table: SymbolTable):
        for entry in table:
            line = ""
    def add_variable(self,var:str):
        if var in self.var_dic:
            variable=self.var_dic[var]
        else:
            self.couter+=1
            self.var_dic[var]=self.couter
        return self.var_dic[var]

    def transverse_block(self, cblock: block, main=True):
        if main:
            self.allocate+="define i32 @main() #0 {\n"
            self.allocate+="%{} = alloca i32, align 4\n".format(self.add_variable("main"))
            self.store+="store i32 0, ptr %{}, align 4\n".format(self.add_variable("main"))
            for tree in cblock.trees:
                if isinstance(tree.root, Declaration):
                    self.to_declaration(tree)
                elif isinstance(tree.root, Comment):
                    self.to_comment(tree)
                elif isinstance(tree.root, Print):
                    var=""
                    if self.g_count>0:
                        var="."
                        var+=str(self.g_count)
                    else:
                        self.f_declerations += "declare i32 @printf(ptr noundef, ...) #1\n"
                    self.g_count+=1
                    self.g_assignment+="@.str{} = private unnamed_addr constant [{}x i8] c\"{}\\00\", align 1\n".format(var,len(tree.root.value)+1,tree.root.value[0])
                    s=self.add_variable("printf"+str(self.g_count))
                    self.allocate+="%{} = call i32 (ptr, ...) @printf(ptr noundef @.str{})\n".format(s,var)
            self.g_assignment+="; Function Attrs: noinline nounwind optnone ssp uwtable(sync)\n"
            self.store+="\n"
            self.store+="ret i32 0\n"
            self.store+="}\n"
        else:
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

        # close file
        text_file.close()

    def switch_Literals(self, v: Value, input: Value):
        # comment above with original code:
        const = ""
        type = ""
        if v.const:
            const = "const"
        variable=0
        if v.value in self.var_dic:
            variable=self.var_dic[v.value]
        else:
            self.couter+=1
            self.var_dic[v.value]=self.couter
            variable=self.var_dic[v.value]

        if v.type == LiteralType.INT:
            self.global_ += "// {} {} {} = {}\n".format(const, "int", v.value, input.value)
            self.allocate += "// {} {} {} = {}\n".format(const, "int", v.value, input.value)
            self.global_ += "@{}= global i32 {}, align 4\n".format(variable, input.value)

            self.allocate += "%{} = alloca i32, align 4\n".format(variable)
            self.store += "store i32 {}, i32* %{}, align 4\n".format(input.value, variable)

        elif v.type == LiteralType.FLOAT:
            self.global_ += "// {} {} {} = {}\n".format(const, "float", v.value, input.value)
            self.allocate += "// {} {} {} = {}\n".format(const, "float", v.value, input.value)
            self.allocate += "%{} = alloca float, align 4\n".format(variable)

            self.global_ += "@{} = global float {}, align 4\n".format(variable, input.value)
            self.store += "store float {}, float* %{}, align 4\n".format(input.value, variable)

        elif v.type == LiteralType.STR:
            size = len(input.value)
            self.global_ += "// {} {} {} = {}\n".format(const, "char", v.value, input.value)
            self.allocate += "// {} {} {} = {}\n".format(const, "char", v.value, input.value)
            self.allocate += "%{} = alloca i8, align 1\n".format(v.value)

            self.global_ += "@{} = global [{}xi8] c{}, align 1\n".format(variable, size, input.value)
            num = ord(input.value)
            self.store += "store i8 {}, i8* %{}, align 1\n".format(num, v.value)

        elif v.type == LiteralType.BOOL:
            bval = 0
            if input.value == "True":
                bval = 1
            self.allocate += "// {}{}{}={}\n".format(const, "_Bool", v.value, input.value)
            self.allocate += "%{} = alloca i8, align 1\n".format(variable)

            self.global_ += "@{} = global i1 {}, align 4\n".format(variable, bval)
            self.store += "store i8 {}, i8* %{}, align 1\n".format(bval, variable)

    def to_bin_operator(self, ast: AST):
        pass

    def to_declaration(self, ast: AST):
        if isinstance(ast.root.leftChild, Pointer):
            print("pointer instance")
        elif isinstance(ast.root, Declaration):
            return self.switch_Literals(ast.root.leftChild, ast.root.rightChild)
        return

    def to_comment(self, ast: AST):

        if isinstance(ast.root, Comment):
            if ast.root.type == CommentType.SL:
                self.global_ += ast.root.value
                self.store += ast.root.value
                self.global_ += "\n"
                self.store += "\n"
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
        var = "x"
        # check if variable in table:
        # if yes/ add 1 loop
        # if not:
        self.store += "%{} = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %3)"
        pass

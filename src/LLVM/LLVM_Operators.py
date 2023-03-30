import ast

from src.ast import AST
from src.ast.SymbolTable import SymbolTable
from src.ast.node import Declaration, Value, LiteralType, Comment, CommentType, Print, Pointer
from src.ast.block import block

# TODO:
"""
comments vervangen met ; 
v pointers
- const 
v getalle-n
v print f
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
    def get_variable(self,var:str):
        return self.var_dic[var]
    def add_variable(self,var:str):
        self.couter += 1
        self.var_dic[var]=self.couter
        return self.var_dic[var]

    def get_type(self,v):
        if v.type==LiteralType.INT:
            return "int"
        elif v.type==LiteralType.FLOAT:
            return "float"
        elif v.type==LiteralType.BOOL:
            return "bool"
        elif v.type==LiteralType.CHAR:
            return "char"
        return False

    def transverse_block(self, cblock: block, main=True):
        if main:
            self.allocate+="define i32 @main() #0 {\n"
            self.allocate+="%{} = alloca i32, align 4\n".format(self.add_variable("main"))
            self.store+="store i32 0, ptr %{}, align 4\n".format(self.get_variable("main"))
            for tree in cblock.trees:
                if isinstance(tree.root, Declaration):

                    self.to_declaration(tree)
                elif isinstance(tree.root, Comment):
                    self.to_comment(tree)
                elif isinstance(tree.root, Print):
                    var=""
                    to_print=""
                    if type(tree.root.value) is tuple:
                        to_print=tree.root.value[0]
                    else:
                        to_print=tree.root.value
                    if self.g_count>0:
                        var="."
                        var+=str(self.g_count)
                    else:
                        self.f_declerations += "declare i32 @printf(ptr noundef, ...) #1\n"
                    self.g_count+=1
                    self.g_assignment+="@.str{} = private unnamed_addr constant [{}x i8] c\"{}\\0A\\00\", align 1\n".format(var,len(to_print)+2,to_print)
                    s=self.add_variable("printf"+str(self.g_count))
                    self.allocate+="; printf ({})\n".format(tree.root.value[0])
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

        if v.type == LiteralType.INT:
            self.allocate += "; {} {} {} = {}\n".format(const, "int", v.value, input.value)
            self.allocate += "%{} = alloca i32, align 4\n".format(self.add_variable(str(v.value)))
            self.store += "store i32 {}, i32* %{}, align 4\n".format(input.value, self.get_variable(v.value))

        elif v.type == LiteralType.FLOAT:
            self.allocate += "; {} {} {} = {}\n".format(const, "float", v.value, input.value)
            self.allocate += "%{} = alloca float, align 4\n".format(self.add_variable(v.value))
            self.store += "store float {}, float* %{}, align 4\n".format(input.value,  self.get_variable(v.value))

        elif v.type == LiteralType.CHAR:
            size = len(input.value)
            self.allocate += "; {} {} {} = {}\n".format(const, "char", v.value, input.value)
            self.allocate += "%{} = alloca i8, align 1\n".format(self.add_variable(v.value))

            num = ord(input.value[1])
            self.store += "store i8 {}, i8* %{}, align 1\n".format(num,self.get_variable(v.value))

        elif v.type == LiteralType.BOOL:
            bval = 0
            if input.value == "True":
                bval = 1
            self.allocate += "; {}{}{}={}\n".format(const, "_Bool", v.value, input.value)
            self.allocate += "%{} = alloca i8, align 1\n".format(self.add_variable(v.value))
            self.store += "store i8 {}, i8* %{}, align 1\n".format(bval, self.get_variable(v.value))

    def to_bin_operator(self, ast: AST):
        pass

    def to_declaration(self, ast: AST):
        if isinstance(ast.root.leftChild, Pointer):
            t_type=self.get_type(ast.root.leftChild)
            const=""
            if ast.root.leftChild.const:
                const="const"
            points=""
            i=0
            while i< ast.root.leftChild.getPointerLevel():
                points+="*"
                i+=1
            self.allocate+="; {} {} {} {} = & {}\n".format(const,t_type,points,ast.root.leftChild.getValue(),ast.root.rightChild.getValue())
            self.allocate+="%{} = alloca ptr, align 8\n".format(self.add_variable(ast.root.leftChild.getValue()))
            self.store+="store ptr %{}, ptr %{}, align 8\n".format(self.get_variable(ast.root.rightChild.getValue()),self.get_variable(ast.root.leftChild.getValue()))
        elif isinstance(ast.root, Declaration):
            return self.switch_Literals(ast.root.leftChild, ast.root.rightChild)
        return

    def to_comment(self, ast: AST):

        if isinstance(ast.root, Comment):
            if ast.root.type == CommentType.SL:
                self.store += ";"
                self.store += ast.root.value
                self.store += "\n"
            elif ast.root.type == CommentType.ML:
                print("ml comment")
                self.store += ";"
                for s in ast.root.value:
                    self.store += s
                    if s == "\n":
                        self.store += ";"
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

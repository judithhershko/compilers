from src.ast import node
from src.ast.AST import AST
from src.ast.node import *
from .ast.Program import *


def create_tree():
    expression_tree = AST()
    expression_tree.setRoot(None)
    return expression_tree


def getVariable(ctx):
    var = ""
    found = False
    for i in ctx:
        if i == '=':
            found = True
        if not found:
            var += i
    return var

def getType(var):
    if var[0] == 'i':
        return LiteralType.INT
    elif var[0] == 'f':
        return LiteralType.FLOAT
    elif var[0] == 'd':
        return LiteralType.DOUBLE
    elif var[0] == 's':
        return LiteralType.STR
    elif var[0] == 'b':
        return LiteralType.BOOL
    elif var[0] == 'c':
        return LiteralType.CHAR
    elif var[0] == 'p':
        return LiteralType.POINTER
    else:
        return False


def separate_type_variable(old, type_):
    return old.replace(type_, '')


def find_type(txt): #TODO: check if this gives no problems
    #type = types.get(txt)
    if txt[0] == 'i':
        return LiteralType.INT
    elif txt[0] == 'f':
        return LiteralType.FLOAT
    elif txt[0] == 'd':
        return LiteralType.DOUBLE
    elif txt[0] == 's':
        return LiteralType.STR
    elif txt[0] == 'b':
        return LiteralType.BOOL
    elif txt[0] == 'c':
        return LiteralType.CHAR
    elif txt[0] == 'p':
        return LiteralType.POINTER
    else:
        return False


def is_variable(v: str):
    for i in v:
        if i is i.isdigit() or i == '.':
            pass
        else:
            return True
    return False


def is_valid_variable(v: str):
    if v[0].isdigit():
        return False
    return True


def find_value_type(v: str):
    if v[0] == '\'' and v[-1] == '\'':
        return node.LiteralType.STR
    elif isFloat(v):
        return node.LiteralType.FLOAT
    elif v[0].isdigit():
        return node.LiteralType.INT
    else:
        return node.LiteralType.VAR


def isFloat(v: str):
    f = False
    for i in v:
        if i == '.':
            f = True
    return f


def commentType(v: str):
    if v[1] == "/":
        return CommentType.SL
    else:
        return CommentType.ML


def order(op: str):
    if op == "/" or op == "*":
        return 0
    else:
        return 1


class stack:
    def __init__(self):
        self.__index = []

    def __len__(self):
        return len(self.__index)

    def push(self, item):
        self.__index.insert(0, item)

    def peek(self):
        if len(self) == 0:
            raise Exception("peek() called on empty stack.")
        return self.__index[0]

    def pop(self):
        if len(self) == 0:
            raise Exception("pop() called on empty stack.")
        return self.__index.pop(0)

    def __str__(self):
        return str(self.__index)
class brackets:
    def __init__(self):
        self.hierarchy=None
        self.tree=None


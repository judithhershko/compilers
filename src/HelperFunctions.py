from .ast import node
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


def getType(txt):
    if len(txt) >= 3 and txt[0:3] == 'int':
        return LiteralType.INT
    elif len(txt) >= 4 and txt[0:5] == 'float':
        return LiteralType.FLOAT
    elif len(txt) >= 6 and txt[0:6] == 'double':
        return LiteralType.DOUBLE
    elif len(txt) >= 6 and txt[0:6] == 'string':
        return LiteralType.STR
    elif len(txt) >= 4 and txt[0:4] == 'bool':
        return LiteralType.BOOL
    elif len(txt) >= 4 and txt[0:4] == 'char':
        return LiteralType.CHAR
    else:
        return False


def remove_type(ptype: LiteralType, v: str):
    if ptype == LiteralType.INT and len(v) >= 3:
        v = v[3:]
    elif ptype == LiteralType.FLOAT and len(v) >= 5:
        v = v[5:]
    elif ptype == LiteralType.BOOL and len(v) >= 4:
        v = v[4:]
    elif ptype == LiteralType.CHAR and len(v) >= 4:
        v = v[4:]
    return v


def getIftype(var: str):
    if var.__len__() >= 6 and var[0:6] == "elseif":
        return ConditionType.ELIF
    elif var.__len__() >= 4 and var[0:4] == "else":
        return ConditionType.ELSE
    else:
        return ConditionType.IF


def getFunction(name: str):
    result_string = name.split('(')[0]
    return result_string


def separate_type_variable(old, type_):
    return old.replace(type_, '')


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
        return node.LiteralType.CHAR
    elif isFloat(v):
        return node.LiteralType.FLOAT
    elif v[0].isdigit() or ((v[0] == '-' or v[0] == '+') and len(v) > 1 and v[1].isdigit()):
        return node.LiteralType.INT
    else:
        return node.LiteralType.VAR


def getArrayName(text: str, type_=LiteralType.INT):
    x = text.split("[")
    x[0] = remove_type(type_, x[0])
    return x[0]


def getArraySize(text: str):
    x = text.split("[")
    x = x[1].split("]")
    # if x[0]=="+" or x[0]=="-" or
    return int(x[0])


def isFloat(v: str):
    f = False
    for i in v:
        if i == '.':
            f = True
    return f


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def commentType(v: str):
    if v[1] == "/":
        return CommentType.SL
    else:
        return CommentType.ML


order_prec = {"++": 0, "--": 1, "!": 2, "*": 3, "/": 3, "%": 3, "+": 4, "-": 4, "": 4, "<": 5, ">": 5, "<=": 5, ">=": 5,
              "==": 6,
              "!=": 6, "&&": 7, "||": 8}


def order(op: str):
    return order_prec[op]


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
        self.hierarchy = None
        self.tree = None

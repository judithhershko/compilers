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


def separate_type_variable(old, type_):
    return old.replace(type_, '')


def find_type(txt):
    return types.get(txt)


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
    if v[0].isdigit() or v[0] == '.':
        return node.LiteralType.NUM
    return node.LiteralType.VAR

def isFloat(v:str):
    f=False
    for i in v:
        if i=='.':
            f=True
    return f
def commentType(v:str):
    if v[1]=="/":
        return CommentType.SL
    else:
        return CommentType.ML

from src.ast.AST import AST
from src.ast.node import *


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

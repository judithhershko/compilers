# from colorama import Fore
#
# def printError(error):
#     print(Fore.RED + error)

from src.ast.node import *


class Undeclared(Exception):
    def __init__(self, unresolved):
        self.unresolved = unresolved

    def __str__(self):
        err = ""
        for elem in self.unresolved:
            err = err + "\n\tError in line " + str(elem[1]) + ": " + str(elem[0]) + " is not declared"
        return err


class WrongType(Exception):
    def __init__(self, type1, type2, line):
        self.type1 = type1
        self.type2 = type2
        self.line = line

    def __str__(self):
        return "\n\tError in line " + str(self.line) + ": " + str(self.type1) + " and " + str(self.type2) + \
               " do not match"


class BinaryOp(Exception):
    def __init__(self, type1, type2, op, line):
        self.type1 = type1
        self.type2 = type2
        self.op = op
        self.line = line

    def __str__(self):
        return "\n\tError in line " + str(self.line) + ": the binary operator " + str(self.op) + \
               " can not be executed on a " + str(self.type1) + " and a " + str(self.type2)


class LogicalOp(Exception):
    def __init__(self, type1, type2, op, line):
        self.type1 = type1
        self.type2 = type2
        self.op = op
        self.line = line

    def __str__(self):
        return "\n\tError in line " + str(self.line) + ": the logical operator " + str(self.op) + \
               " can not be executed on a " + str(self.type1) + " and a " + str(self.type2)


class NotOp(Exception):
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return "\t\nError in line " + str(self.line) + ": the ! operator only supports variables of LiteralType.BOOL"


class WrongDeclaration(Exception):
    def __init__(self, typeDec, typeVar, line):
        self.declaration = typeDec
        self.variable = typeVar
        self.line = line

    def __str__(self):
        return "\n\tError in line " + str(self.line) + ": " + str(self.variable) + \
               " can not be placed in a variable of type " + str(self.declaration)


class WrongPointer(Exception):
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return "\n\tError in line " + str(self.line) + \
               ": only when a pointer references something can the level be different from zero"


class Redeclaration(Exception):
    def __init__(self, var, line):
        self.variable = var
        self.line = line

    def __str__(self):
        return "\n\tError in line " + str(self.line) + ": there is a redeclaration of the variable " + \
               str(self.variable)


class ResetConst(Exception):
    def __init__(self, var, line):
        self.variable = var
        self.line = line

    def __str__(self):
        return "\n\tError in line " + str(self.line) + ": there is an reassignment of the const variable " + \
               str(self.variable)


class TypeDeclaration(Exception):
    def __init__(self, var, varType, valueType, line):
        self.variable = var
        self.type = varType
        self.value = valueType
        self.line = line

    def __str__(self):
        return "\n\tError in line " + str(self.line) + ": " + str(self.variable) + " has type " + str(self.type) + \
               " and does not support variables of type " + str(self.value)


class PointerLevel(Exception):
    def __init__(self, var, varLevel, valueLevel, line):
        self.variable = var
        self.level = varLevel
        self.valueLevel = valueLevel
        self.line = line

    def __str__(self):
        return "\n\tError in line " + str(self.line) + ": " + str(self.variable) + " has level " + str(self.level) + \
               " and not the given " + str(self.valueLevel)


class RefPointerLevel(Exception):
    def __init__(self, var, varLevel, refLevel, line):
        self.variable = var
        self.level = varLevel
        self.refLevel = refLevel
        self.line = line

    def __str__(self):
        return "\n\tError in line " + str(self.line) + ": " + str(self.variable) + \
               " should reference a variable with a reference level of " + str(self.level) + " and not the given " + \
               str(self.refLevel)


class ImpossibleRef(Exception):
    def __init__(self, ref, line):
        self.reference = ref
        self.line = line

    def __str__(self):
        return "\n\tError in line " + str(self.line) + ": the variable " + str(self.reference) + \
               " that is referenced by the pointer is not available"


class PointerType(Exception):
    def __init__(self, name, refType, valueType, line):
        self.reference = name
        self.type = refType
        self.valueType = valueType
        self.line = line

    def __str__(self):
        return "\n\tError in line " + str(self.line) + ": the pointer has type " + str(self.valueType) + \
               ", while the referenced variable " + str(self.reference) + " has type " + str(self.type)


class NotSupported(Exception):
    def __init__(self, typeOp, valueOp, line):
        self.typeOp = typeOp
        self.valueOp = valueOp
        self.line = line

    def __str__(self):
        return "\n\tError in line " + str(self.line) + ": the " + str(self.typeOp) + " does not support the " + \
               str(self.valueOp) + " operator."


class ChildType(Exception):
    def __init__(self, oper, type1, type2, line):
        self.oper = oper
        self.type1 = type1
        self.type2 = type2
        self.line = line

    def __str__(self):
        if self.type2 is None:
            return "\n\tError in line " + str(self.line) + ": the " + str(self.oper) + \
                   " does not support the following child type: " + str(self.type1)
        else:
            return "\n\tError in line " + str(self.line) + ": the " + str(self.oper) + \
                   " does not support one of the following child types: " + str(self.type1) + ", " + str(self.type2)


class NotDeclaration(Exception):
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return "\n\tError in line " + str(self.line) + \
               ": only objects of type Declaration can be added to the symbol table"


class LeftSideDeclaration(Exception):
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return "\n \t Error in line " + str(self.line) + \
               ": the left hand side of the declaration should be a variable or a pointer"

class ReservedWord(Exception):
    def __init__(self,line,variable):
        self.line=line
        self.variable=variable

    def __str__(self):
        return "\n \t Error in line  {} \n: rename {}. It is a reserved word.".format( str(self.line),self.variable)



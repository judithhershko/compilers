# from colorama import Fore
#
# def printError(error):
#     print(Fore.RED + error)


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

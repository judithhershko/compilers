# TODO: check different operators and how to group them
import enum
import sys
from src.ErrorHandeling.GenerateError import *

types = \
    {"double": 4, "int": 5, "char": 6, "bool": 7, "string": 2,"float":8,"pointer":9,"nr":1,"var":3};


class CommentType(enum.Enum):
    ML = 0
    SL = 1


class LiteralType(enum.Enum):
    NUM = 1
    STR = 2
    VAR = 3
    DOUBLE = 4
    INT = 5
    CHAR = 6
    BOOL = 7
    FLOAT = 8
    POINTER = 9


class AST_node:
    number = None
    level = None
    parent = None
    line = None
    variable = False

    def getId(self):
        return str(self.level) + "." + str(self.number)

    def getParent(self):
        return self.parent

    def setNumber(self, number):
        self.number = number

    def setLevel(self, level):
        self.level = level

    def getLine(self):
        return self.line

    def setLine(self, line):
        self.line = line

    def isVariable(self):
        return self.variable

    def setVariable(self, var):
        self.variable = var


class Comment(AST_node):
    def __init__(self, lit, commentType, line=None):
        self.parent = None
        self.type = commentType
        self.value = lit
        self.line = line

    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return self.value == other.value

    def getValue(self):
        return self.value

    def setValue(self, val):
        self.value = val

    def setType(self, type):
        self.type = type

    def getLabel(self):
        return "\"Comment: " + self.value + "\""

    def getType(self):
        return self.type


class Print(AST_node):
    def __init__(self, lit):
        self.parent = None
        self.value = lit

    def __eq__(self, other):
        if not isinstance(other, Print):
            return False
        return self.value == other.value

    def getValue(self):
        return self.value

    def setValue(self, val):
        self.value = val

    def getLabel(self):
        return "\"Print: " + self.value + "\""


class Value(AST_node):
    def __init__(self, lit, valueType, parent=None, line=None, variable=False, const=False):
        self.value = lit
        self.type = valueType
        self.parent = parent
        self.variable = variable
        self.const = const
        self.nr_pointers = 0
        self.line = line

    def __eq__(self, other):
        if not isinstance(other, Value):
            return False
        return self.value == other.value and self.type == other.type and self.parent == other.parent and \
               self.variable == other.variable and self.const == other.const and self.level == other.level and \
               self.number == other.number and self.line == other.line

    def getValue(self):
        return self.value

    def setValue(self, val):
        self.value = val

    def setType(self, type: LiteralType):
        self.type = type

    def getLabel(self):
        if isinstance(self.value, int) or isinstance(self.value, float):
            return "\"Literal: " + str(self.value) + "\""
        elif isinstance(self.value, str):
            return "\"Literal: " + self.value + "\""

    def getType(self):
        return self.type

    def getVariables(self):
        if self.variable:
            return [(self.value, self.line)]
        else:
            return []

    def replaceVariables(self, values):
        if self.variable:
            self.value = values[self.value]
            self.variable = False

    def getHigherType(self, node2):
        type1 = self.type
        type2 = node2.getType()
        try:
            if (type1 == LiteralType.STR and type2 in (LiteralType.STR, LiteralType.CHAR)) or \
                    (type2 == LiteralType.STR and type1 == LiteralType.CHAR):
                return LiteralType.STR
            elif type1 == LiteralType.CHAR and type2 == LiteralType.CHAR:
                return LiteralType.CHAR
            elif (type1 == LiteralType.DOUBLE and type2 in (LiteralType.DOUBLE, LiteralType.FLOAT, LiteralType.INT)) or \
                    (type2 == LiteralType.DOUBLE and type1 in (LiteralType.FLOAT, LiteralType.INT)):
                return LiteralType.DOUBLE
            elif (type1 == LiteralType.FLOAT and type2 in (LiteralType.FLOAT, LiteralType.INT)) or \
                    (type2 == LiteralType.FLOAT and type1 == LiteralType.INT):
                return LiteralType.FLOAT
            elif type1 == LiteralType.INT and type2 == LiteralType.INT:
                return LiteralType.INT
            else:
                raise WrongType(type1, type2, self.line)

        except WrongType:
            raise


class Declaration(AST_node):
    def __init__(self, parent=None, var=Value, line=None):
        self.parent = parent
        self.leftChild = var
        self.rightChild = None
        self.operator = "="
        self.line = line

    def __eq__(self, other):
        if not isinstance(other, Declaration):
            return False
        return self.leftChild == other.leftChild and self.rightChild == other.rightChild

    def getLabel(self):
        return "\" Declaration: " + self.operator + "\""

    def setLeftChild(self, child):
        self.leftChild = child

    def setRightChild(self, child):
        self.rightChild = child

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild


class BinaryOperator(AST_node):
    leftChild = None
    rightChild = None

    def __init__(self, oper, parent=None, line=None):
        self.operator = oper
        self.parent = parent
        self.line = line

    def __eq__(self, other):
        if not isinstance(other, BinaryOperator):
            return False
        return self.operator == other.operator and self.leftChild == other.leftChild and \
               self.rightChild == other.rightChild and self.parent == other.parent and \
               self.variable == other.variable and self.level == other.level and \
               self.number == other.number and self.line == other.line

    def getValue(self):
        return self.operator

    def getLabel(self):
        return "\"Binary operator: " + self.operator + "\""

    def setLeftChild(self, child):
        self.leftChild = child

    def setRightChild(self, child):
        self.rightChild = child

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def fold(self):
        if not isinstance(self.leftChild, Value):
            self.leftChild = self.leftChild.fold()
        if not isinstance(self.rightChild, Value):
            self.rightChild = self.rightChild.fold()

        # TODO: does char + char need to be supported?
        try:
            if not isinstance(self.leftChild, Value) or not isinstance(self.rightChild, Value):
                return self
            elif not self.leftChild.getType() in (LiteralType.DOUBLE, LiteralType.FLOAT, LiteralType.INT) or \
                    not self.rightChild.getType() in (LiteralType.DOUBLE, LiteralType.FLOAT, LiteralType.INT):
                raise BinaryOp(self.leftChild.getType(), self.rightChild.getType(), self.operator, self.line)
            else:
                if self.operator == "*":
                    res = int(self.leftChild.getValue()) * int(self.rightChild.getValue())
                elif self.operator == "/":
                    res = int(self.leftChild.getValue()) / int(self.rightChild.getValue())
                elif self.operator == "+":
                    res = int(self.leftChild.getValue()) + int(self.rightChild.getValue())
                elif self.operator == "-":
                    res = int(self.leftChild.getValue()) - int(self.rightChild.getValue())
                elif self.operator == "%":
                    res = int(self.leftChild.getValue()) % int(self.rightChild.getValue())

                typeOfValue = self.leftChild.getHigherType(self.rightChild)
                # TODO: check if this if is still necessary, is caught in the error of getHigherType
                if not typeOfValue:
                    return "impossible operation"

                newNode = Value(res, typeOfValue, self.parent)
                return newNode

        except BinaryOp:
            raise

    def getVariables(self):
        res = self.leftChild.getVariables()
        right = self.rightChild.getVariables()
        res.extend(right)
        return res

    def replaceVariables(self, values):
        self.leftChild.replaceVariables(values)
        self.rightChild.replaceVariables(values)


class UnaryOperator(AST_node):
    child = None

    def __init__(self, oper, parent=None, line=None):
        self.operator = oper
        self.parent = parent
        self.line = line

    def __eq__(self, other):
        if not isinstance(other, UnaryOperator):
            return False
        return self.operator == other.operator and self.child == other.child and self.parent == other.parent and \
               self.variable == other.variable and self.level == other.level and \
               self.number == other.number and self.line == other.line

    def getValue(self):
        return self.operator

    def getLabel(self):
        return "\"Unary operator: " + self.operator + "\""

    def setChild(self, child):
        self.child = child

    def fold(self):
        if not isinstance(self.child, Value):
            self.child = self.child.fold()

        if not isinstance(self.child, Value):
            return self
        else:
            if self.operator == "-":
                res = - self.child.getValue()
            elif self.operator == "++":
                res = self.child.getValue() + 1
            elif self.operator == "--":
                res = self.child.getValue() - 1
            else:
                res = + self.child.getValue()

        if self.child.getType() not in (LiteralType.FLOAT, LiteralType.DOUBLE, LiteralType.INT):
            return "impossible operation"

        newNode = Value(res, self.child.getType(), self.parent)
        return newNode

    def getVariables(self):
        return self.child.getVariables()

    def replaceVariables(self, values):
        self.child.replaceVariables(values)


class LogicalOperator(AST_node):
    leftChild = None
    rightChild = None

    def __init__(self, oper, parent=None, line=None):
        self.operator = oper
        self.parent = parent
        self.line = line

    def __eq__(self, other):
        if not isinstance(other, LogicalOperator):
            return False
        return self.operator == other.operator and self.leftChild == other.leftChild and \
               self.rightChild == other.rightChild and self.parent == other.parent and \
               self.variable == other.variable and self.level == other.level and \
               self.number == other.number and self.line == other.line

    def getValue(self):
        return self.operator

    def getLabel(self):
        return "\"Logical operator: " + self.operator + "\""

    def setLeftChild(self, child):
        self.leftChild = child

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def setRightChild(self, child):
        if self.operator == "!":
            print("! operator can only have a left child", file=sys.stderr)
        self.rightChild = child

    def fold(self):
        if not isinstance(self.leftChild, Value):
            self.leftChild = self.leftChild.fold()
        if not isinstance(self.rightChild, Value):
            self.rightChild = self.rightChild.fold()

        leftType = self.leftChild.getType()
        if self.operator == "!":
            rightType = leftType
        else:
            rightType = self.rightChild.getType()

        try:
            if not isinstance(self.leftChild, Value) or not isinstance(self.rightChild, Value):
                return self
            elif leftType != rightType:
                raise LogicalOp
            else:
                if self.operator == "&&":
                    res = self.leftChild.getValue() and self.rightChild.getValue()
                elif self.operator == "||":
                    res = self.leftChild.getValue() or self.rightChild.getValue()
                elif self.operator == ">=":
                    res = self.leftChild.getValue() >= self.rightChild.getValue()
                elif self.operator == "<=":
                    res = self.leftChild.getValue() <= self.rightChild.getValue()
                elif self.operator == ">":
                    res = self.leftChild.getValue() > self.rightChild.getValue()
                elif self.operator == "<":
                    res = self.leftChild.getValue() < self.rightChild.getValue()
                elif self.operator == "==":
                    res = self.leftChild.getValue() == self.rightChild.getValue()
                elif self.operator == "!=":
                    res = self.leftChild.getValue() != self.rightChild.getValue()
                else:
                    if self.leftChild.getType() == LiteralType.BOOL:
                        res = not self.leftChild.getValue()
                    else:
                        raise NotOp

                newNode = Value(res, LiteralType.BOOL, self.parent)
                return newNode

        except LogicalOp:
            raise
        except NotOp:
            raise

    def getVariables(self):
        res = self.leftChild.getVariables()
        right = self.rightChild.getVariables()
        res.extend(right)
        return res

    def replaceVariables(self, values):
        self.leftChild.replaceVariables(values)
        self.rightChild.replaceVaribles(values)


class Declaration(AST_node):
    leftChild = None
    rightChild = None

    def __init__(self, parent=None, line=None):
        self.parent = parent
        self.line = line

    def __eq__(self, other):
        if not isinstance(other, LogicalOperator):
            return False
        return self.leftChild == other.leftChild and self.rightChild == other.rightChild and \
               self.parent == other.parent and self.variable == other.variable and self.level == other.level and \
               self.number == other.number and self.line == other.line

    def getLabel(self):
        return "\"Value declaration\""

    def setLeftChild(self, child):
        self.leftChild = child

    def setRightChild(self, child):
        self.rightChild = child

    def fold(self):
        if not isinstance(self.leftChild, Value):
            self.leftChild = self.leftChild.fold()
        if not isinstance(self.rightChild, Value):
            self.rightChild = self.rightChild.fold()

        highestType = self.leftChild.getHigherType(self.rightChild)
        try:
            if self.leftChild.getType() == highestType:
                return self
            else:
                raise WrongDeclaration

        except WrongDeclaration:
            raise

    def getVariables(self):
        return self.rightChild.getVariables()

    def replaceVariables(self, values):
        self.rightChild.replaceVaribles(values)


class Pointer(AST_node):
    def __init__(self, location, parent=None, variable=True, const=False):
        self.value = location
        self.type = LiteralType.POINTER
        self.parent = parent
        self.variable = variable
        self.const = const

    def __eq__(self, other):
        if not isinstance(other, Pointer):
            return False
        return self.value == other.value and self.type == other.type and self.parent == other.parent and \
               self.variable == other.variable and self.level == other.level and self.const == other.const and \
               self.number == other.number and self.line == other.line

    def getValue(self):
        return self.value

    def setValue(self, val):
        self.value = val

    def getLabel(self):
        return "\"Pointer: " + str(self.value) + "\""

    def getType(self):
        return self.type

    def getVariables(self):
        return [(self.value, self.line)]

    def replaceVariables(self, values):
        if self.variable:
            self.value = values[self.value]
            self.variable = False

# TODO: check different operators and how to group them
import enum
import sys

types = \
    {"double": 4, "int": 5, "char": 6, "bool": 7, "string": 8};


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
    def __init__(self, lit, commentType):
        self.parent = None
        self.type = commentType
        self.value = lit

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
    def __init__(self, lit, valueType, parent=None, variable=False, const=False):
        self.value = lit
        self.type = valueType
        self.parent = parent
        self.variable = variable
        self.const = const
        self.nr_pointers = 0

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

    def setType(self, type):
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
            return [self.value]
        else:
            return []

    def replaceVariables(self, values):
        if self.variable:
            self.value = values[self.value]
            self.variable = False

    def getHigherType(self, node2):
        type1 = self.type
        type2 = node2.getType()
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
            return None

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

    def __init__(self, oper, parent=None):
        self.operator = oper
        self.parent = parent

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

        typeOfValue = None

        if not isinstance(self.leftChild, Value) or not isinstance(self.rightChild, Value):
            return self
        elif not self.leftChild.getType() in (LiteralType.DOUBLE, LiteralType.FLOAT, LiteralType.INT) or \
                not self.rightChild.getType() in (LiteralType.DOUBLE, LiteralType.FLOAT, LiteralType.INT):
            return self
        else:
            if self.operator == "*":
                res = self.leftChild.getValue() * self.rightChild.getValue()
            elif self.operator == "/":
                res = self.leftChild.getValue() / self.rightChild.getValue()
            elif self.operator == "+":
                res = self.leftChild.getValue() + self.rightChild.getValue()
            elif self.operator == "-":
                res = self.leftChild.getValue() - self.rightChild.getValue()
            elif self.operator == "%":
                res = self.leftChild.getValue() % self.rightChild.getValue()
            else:
                res = self.leftChild.getValue() == self.rightChild.getValue()
                typeOfValue = LiteralType.BOOL
            if not typeOfValue:
                typeOfValue = self.leftChild.getHigherType(self.rightChild)
            if not typeOfValue:
                return "impossible operation"

            newNode = Value(res, typeOfValue, self.parent)
            return newNode

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

    def __init__(self, oper, parent=None):
        self.operator = oper
        self.parent = parent

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

    def __init__(self, oper, parent=None):
        self.operator = oper
        self.parent = parent

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

    def setRightChild(self, child):
        if self.operator == "!":
            print("! operator can only have a left child", file=sys.stderr)
        self.rightChild = child

    def fold(self):
        if not isinstance(self.leftChild, Value):
            self.leftChild = self.leftChild.fold()
        if not isinstance(self.rightChild, Value):
            self.rightChild = self.rightChild.fold()

        if not isinstance(self.leftChild, Value) or not isinstance(self.rightChild, Value):
            return self
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
                res = not self.leftChild.getValue()

            newNode = Value(res, LiteralType.BOOL, self.parent)
            return newNode

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

    def __init__(self, parent=None):
        self.parent = parent

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
        if self.leftChild.getType() != highestType:
            return "invalid declaration"

        return self

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
        return [self.value]

    def replaceVariables(self, values):
        if self.variable:
            self.value = values[self.value]
            self.variable = False

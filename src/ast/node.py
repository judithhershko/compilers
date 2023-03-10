# TODO: check different operators and how to group them
import enum
import sys

types = \
    {"double": 4, "int": 5, "char": 6, "bool": 7, "string": 8};


class LiteralType(enum.Enum):
    NUM = 1
    STR = 2
    VAR = 3
    DOUBLE = 4
    INT = 5
    CHAR = 6
    BOOL = 7

    def __init__(self, const=False):
        self.const = const


class AST_node():
    number = None
    level = None
    parent = None

    def getId(self):
        return str(self.level) + "." + str(self.number)

    def getParent(self):
        return self.parent

    def setNumber(self, number):
        self.number = number

    def setLevel(self, level):
        self.level = level


class Value(AST_node):
    def __init__(self, lit, valueType, parent=None, const=False):
        self.value = lit
        self.type = valueType
        self.parent = parent
        self.const = const

    def __eq__(self, other):
        if not isinstance(other, Value):
            return False
        return self.value == other.value

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
        if self.type == LiteralType.VAR:
            return [self.value]
        else:
            return []

    def replaceVariables(self, values):
        self.value = values[self.value]
        self.type = LiteralType.NUM


class Declaration(AST_node):
    def __init__(self, parent=None, var=Value):
        self.parent = parent
        self.leftChild = var
        self.rightChild = None
        self.operator = "="

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

    def __init__(self, oper, parent=None):
        self.operator = oper
        self.parent = parent

    def getValue(self):
        return self.rightChild.getValue()

    def __eq__(self, other):
        if not isinstance(other, BinaryOperator):
            return False
        return self.operator == other.operator and self.leftChild == other.leftChild and self.rightChild == other.rightChild

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

        if not isinstance(self.leftChild, Value) or not isinstance(self.rightChild, Value):
            return self
        elif not self.leftChild.getType() == LiteralType.NUM or not self.rightChild.getType() == LiteralType.NUM:
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
            elif self.operator == ">":
                res = self.leftChild.getValue() > self.rightChild.getValue()
            elif self.operator == "<":
                res = self.leftChild.getValue() < self.rightChild.getValue()
            else:
                res = self.leftChild.getValue() == self.rightChild.getValue()
            newNode = Value(res, LiteralType.NUM)

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
        return self.operator == other.operator and self.child == other.child

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
            else:
                res = + self.child.getValue()
        newNode = Value(res, LiteralType.NUM)

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
        return self.operator == other.operator and self.leftChild == other.leftChild and self.rightChild == other.rightChild

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
            else:
                res = not self.leftChild.getValue()
            newNode = Value(res, LiteralType.NUM)

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
        return self.leftChild == other.leftChild and self.rightChild == other.rightChild

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

        return self

    def getVariables(self):
        return self.rightChild.getVariables()

    def replaceVariables(self, values):
        self.rightChild.replaceVaribles(values)

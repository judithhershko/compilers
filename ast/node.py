class AST_node():
    number = None
    level = None

    def getId(self):
        return str(self.level) + "." + str(self.number)

    def setNumber(self, number):
        self.number = number

    def setLevel(self, level):
        self.level = level


class Value(AST_node):
    def __init__(self, lit):
        self.value = lit

    def __eq__(self, other):
        if not isinstance(other, Value):
            return False
        return self.value == other.value

    def getValue(self):
        return self.value

    def getLabel(self):
        if isinstance(self.value, int):
            return "\"Literal: " + str(self.value) + "\""
        elif isinstance(self.value, str):
            return "\"Literal: " + self.value + "\""


class BinaryOperator(AST_node):
    leftChild = None
    rightChild = None

    def __init__(self, oper):
        self.operator = oper

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


class UnaryOperator(AST_node):
    child = None

    def __init__(self, oper):
        self.operator = oper

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


class LogicalOperator(AST_node):
    leftChild = None
    rightChild = None

    def __init__(self, oper):
        self.operator = oper

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
        self.rightChild = child

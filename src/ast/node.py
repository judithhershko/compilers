from enum import Enum
import re

from src.ErrorHandeling.GenerateError import *
from src.LLVM.Helper_LLVM import set_llvm_binary_operators, set_llvm_unary_operators
from src.ast.node_types.node_type import LiteralType, ConditionType
from itertools import islice


def getHighestType(type1, type2, line):
    if isinstance(type1, str):
        type1 = LiteralType.getLiteral(type1)
    if isinstance(type2, str):
        type2 = LiteralType.getLiteral(type2)

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
        elif type1 == LiteralType.BOOL and type2 == LiteralType.BOOL:
            return LiteralType.BOOL
        elif type1 is None:
            return type2
        elif type1 in (LiteralType.INT, LiteralType.FLOAT) and type2 == LiteralType.BOOL:
            return type1
        else:
            raise WrongType(type1, type2, line)

    except WrongType:
        raise


class ToLLVM:
    pass


class block:
    pass


types = \
    {"double": 4, "int": 5, "char": 6, "bool": 7, "string": 2, "float": 8, "pointer": 9, "nr": 1, "var": 3};


class CommentType(Enum):
    ML = 0
    SL = 1


class AST_node:
    number = None
    level = None
    parent = None
    line = None
    variable = False
    name = None

    def __init__(self, llvm=ToLLVM()):
        self.llvm = llvm

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

    def printTables(self, filePath: str, to_llvm=None):
        pass


class Comment(AST_node):
    def __init__(self, lit, commentType, line=None):
        self.parent = None
        self.type = commentType
        self.value = lit
        self.line = line
        self.name = "comment"

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
        a = self.value
        a = a.replace('"', '')
        return "\"Comment: " + a + "\""

    def getType(self):
        return self.type

    def getVariables(self, fill: bool = True, scope=None):
        return [[], True]

    def replaceVariables(self, values, fill: bool = True):
        pass

    def fold(self, to_llvm=None):
        return self, True


class Print(AST_node):
    def __init__(self, line):
        self.parent = None
        self.value = None
        self.name = "print"
        self.input_string = ""
        self.param = []
        self.paramString = []
        self.line = line

    def __eq__(self, other):
        if not isinstance(other, Print):
            return False
        return self.value == other.value

    def setString(self, input: str):
        self.input_string = input
        self.setParamString(input)

    # TODO : let op param kan *z zijn als een string,
    # TODO: check dat dit een digit niet ervoor staat ipv letter
    def addParam(self, param):
        self.param.append(param)
        # self.value = param

    def find_and_select(self, input_string):
        regex = r'%[cdsif]'
        matches = re.findall(regex, input_string)
        return matches

    #
    def setParamString(self, input: str):
        self.paramString = self.find_and_select(input)

    def getValue(self):
        return self.value

    def getVariables(self, fill: bool = True, scope=None):
        ret = []
        true = True
        for tree in self.param:
            temp = tree
            if isinstance(tree, tuple):
                temp = tree[0]
            temp2 = temp.getVariables(fill, scope)
            if not len(temp2[0]) == 0:
                ret.append(temp2[0][0])
            if not temp2[1]:
                true = False
        return ret, true

    def setValue(self, val):
        self.value = val

    def getLabel(self):
        return "\"Print:\""

    def fold(self, to_llvm=None):
        try:
            if len(self.param) != len(self.paramString):
                raise PrintSize(self.line)
            for pos in range(len(self.param)):
                """if self.paramString[pos] == "%f" and self.param[pos].root.getType() != LiteralType.FLOAT:
                    raise PrintType(self.line, "%f", str(LiteralType.FLOAT))
                elif self.paramString[pos] in ("%d", "%i") and self.param[pos].root.getType() != LiteralType.INT :
                    raise PrintType(self.line, self.paramString[pos], str(LiteralType.INT))
                elif self.paramString[pos] == "%c" and self.param[pos].root.getType() != LiteralType.CHAR:
                    raise PrintType(self.line, "%c", str(LiteralType.CHAR))"""

                self.param[pos] = self.param[pos].foldTree()

        except PrintSize:
            raise
        except PrintType:
            raise
        return self, True  # TODO: redo this when the print function is adapted to the final form

    def replaceVariables(self, values, fill: bool = True):
        for tree in self.param:
            tree.replaceVariables(values, fill)


# Used to hald a single value/variable, normally a leaf of the AST

class Scan(AST_node):
    def __init__(self, line):
        self.parent = None
        self.value = None
        self.name = "scan"
        self.input_string = ""
        self.param = []
        self.paramString = []
        self.line = line

    def __eq__(self, other):
        if not isinstance(other, Print):
            return False
        return self.value == other.value

    def setString(self, input: str):
        self.input_string = input
        self.setParamString(input)

    # TODO : let op param kan *z zijn als een string,
    # TODO: check dat dit een digit niet ervoor staat ipv letter
    def addParam(self, param):
        self.param.append(param)
        # self.value = param

    def find_and_select(self, input_string):
        regex = r'%[cdsif]'
        matches = re.findall(regex, input_string)
        return matches

    #
    def setParamString(self, input: str):
        self.paramString = self.find_and_select(input)

    def getValue(self):
        return self.value

    def getVariables(self, fill: bool = True, scope=None):
        ret = []
        true = True
        for tree in self.param:
            temp = tree
            if isinstance(tree, tuple):
                temp = tree[0]
            temp2 = temp.getVariables(fill, scope)
            if not len(temp2[0]) == 0:
                ret.append(temp2[0][0])
            if not temp2[1]:
                true = False
        return ret, true

    def setValue(self, val):
        self.value = val

    def getLabel(self):
        return "\"Scan:\""

    def fold(self, to_llvm=None):
        try:
            if len(self.param) != len(self.paramString):
                raise PrintSize(self.line)
            for pos in range(len(self.param)):
                if self.paramString[pos] == "%f" and self.param[pos].root.getType() != LiteralType.FLOAT:
                    raise PrintType(self.line, "%f", str(LiteralType.FLOAT))
                elif self.paramString[pos] in ("%d", "%i") and self.param[pos].root.getType() != LiteralType.INT:
                    raise PrintType(self.line, self.paramString[pos], str(LiteralType.INT))
                elif self.paramString[pos] == "%c" and self.param[pos].root.getType() != LiteralType.CHAR:
                    raise PrintType(self.line, "%c", str(LiteralType.CHAR))

                self.param[pos] = self.param[pos].foldTree()

        except PrintSize:
            raise
        except PrintType:
            raise
        return self, True  # TODO: redo this when the print function is adapted to the final form

    def replaceVariables(self, values, fill: bool = True):
        for tree in self.param:
            tree.replaceVariables(values, fill)


class Value(AST_node):
    def __init__(self, lit: str, valueType, line: int, parent: AST_node = None, variable: bool = False,
                 const: bool = False, decl: bool = False, deref: bool = False):
        """
        :param lit: string containing the value (int, string, variable, ...) of the node
        :param valueType: LiteralType containing the type of element saved in the node
        :param line: int telling the line where the element from the node is located
        :param parent: AST_node-object containing the parent of the current node in the AST
        :param variable: boolean telling if the saved element is a variable or an actual value
        :param const: boolean telling if the saved element is a const (only used when talking about variables)
        :param decl: boolean telling if the saved element is a declaration of the variable
        :param deref: boolean telling if the variable is proceeded with an &
        """
        self.value = lit
        self.type = valueType
        self.parent = parent
        self.variable = variable
        self.const = const
        self.declaration = decl
        self.line = line
        self.deref = deref
        self.name = "val"

    def __eq__(self, other):
        if not isinstance(other, Value):
            return False
        res = self.value == other.value and self.type == other.type and self.parent == other.parent and \
              self.variable == other.variable and self.const == other.const and self.declaration == other.declaration \
              and self.number == other.number and self.line == other.line
        return res

    def getValue(self):
        return self.value

    def setValue(self, val):
        self.value = val

    def setType(self, type: LiteralType):
        self.type = type

    def getLabel(self):
        # if isinstance(self.value, int) or isinstance(self.value, float):
        return "\"Literal: " + str(self.value) + "\""
        # elif isinstance(self.value, str):
        #     return "\"Literal: " + self.value + "\""

    def getType(self):
        return self.type

    def getVariables(self, fill: bool = True, scope=None):
        """
        returns the variable contained within the node
        :return:
        """
        if self.variable:
            return [[(self.value, self.line)], True]
        else:
            return [[], True]

    def getDeref(self):
        return self.deref

    def replaceVariables(self, values, fill: bool = True):
        """
        replaces the variables in the node with the actual values contained in values
        :param values: dictionary containing the variable names as keys and the corresponding values as values
        """
        try:
            if len(values) == 0:
                pass
            elif self.variable and not self.value in values:
                raise NotDeclared(self.value, self.line)
            elif self.variable and values[self.value][3] and fill:
                self.type = values[self.value][1]
                self.value = values[self.value][0]
                self.variable = False
            elif self.variable:
                self.type = values[self.value][1]

        except NotDeclared:
            raise

    def getHigherType(self, node2: AST_node):
        """
        This function will compare the type of this node with the one of the inputted node
        :param node2: AST_node type containing the other child of the parent node in the AST
        :return: returns the LiteralType with the highest priority (str>char; double>float>int)
        """
        # if not (isinstance(node2, Value) or isinstance(node2, Array) or isinstance(node2, Function)):
        #     return self.type
        type1 = self.type
        if isinstance(node2, Function):
            pass
        type2 = node2.getType()

        if isinstance(type1, str):
            type1 = LiteralType.getLiteral(type1)
        if isinstance(type2, str):
            type2 = LiteralType.getLiteral(type2)

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
            elif type1 == LiteralType.BOOL and type2 == LiteralType.BOOL:
                return LiteralType.BOOL
            elif type1 is None:
                return type2
            elif type1 in (LiteralType.INT, LiteralType.FLOAT) and type2 == LiteralType.BOOL:
                return type1
            else:
                raise WrongType(type1, type2, self.line)

        except WrongType:
            raise

    def setValueToType(self):
        """
        replaces the string representation of the value with the actual value
        :return:
        """
        if self.getType() == LiteralType.STR:
            self.value = str(self.value)
        elif self.getType() == LiteralType.INT:
            self.value = int(self.value)
        elif self.getType() == LiteralType.FLOAT:
            self.value = float(self.value)
        elif self.getType() == LiteralType.BOOL:
            self.value = bool(self.value)
        else:
            raise


# used to hold a binary operator containing the operator and two children with the operand
class BinaryOperator(AST_node):
    leftChild = None
    rightChild = None

    def __init__(self, oper: str, line: int, parent: AST_node = None):
        """
        :param oper:string containing the operator of the binary operation
        :param parent: AST_node type containing the parent of the current node in the AST
        :param line: int telling the line of the binary operator
        """
        self.operator = oper
        self.parent = parent
        self.line = line
        self.name = "binary"

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

    def fold(self, to_llvm=None):
        """
        This function will try to reduce the whole binary operation by first folding both children of the node.
        Thereafter, the binary operation will be calculated and a Value node will replace the current BinaryOperator
        node.
        :return: the replacing Value node
        """
        if not (isinstance(self.leftChild, Value) or isinstance(self.leftChild, Pointer) or
                isinstance(self.leftChild, Array)):
            self.leftChild = self.leftChild.fold(to_llvm)[0]
        if not (isinstance(self.rightChild, Value) or isinstance(self.rightChild, Pointer) or
                isinstance(self.rightChild, Array)):
            self.rightChild = self.rightChild.fold(to_llvm)[0]

        try:
            if not (isinstance(self.leftChild, Value) or isinstance(self.leftChild, Pointer) or
                    isinstance(self.leftChild, Array)) or \
                    not (isinstance(self.rightChild, Value) or isinstance(self.rightChild, Pointer) or
                         isinstance(self.rightChild, Array)):
                if to_llvm is not None:
                    if isinstance(self.leftChild, UnaryOperator) and not isinstance(self.rightChild, UnaryOperator):
                        set_llvm_unary_operators(self.leftChild, self.operator, to_llvm)
                    if not isinstance(self.leftChild, UnaryOperator) and isinstance(self.rightChild, UnaryOperator):
                        set_llvm_unary_operators(self.rightChild, self.operator, to_llvm)
                    else:
                        set_llvm_binary_operators(self.leftChild, self.rightChild, self.operator, to_llvm)
                return self, False
            elif isinstance(self.leftChild, Value) and isinstance(self.rightChild, Value) and \
                    (self.leftChild.variable or self.rightChild.variable):
                if to_llvm is not None:
                    if isinstance(self.leftChild, UnaryOperator) or isinstance(self.rightChild, UnaryOperator):
                        if isinstance(self.leftChild, UnaryOperator):
                            set_llvm_unary_operators(self.leftChild, self.operator, to_llvm)
                        if isinstance(self.rightChild, UnaryOperator):
                            set_llvm_unary_operators(self.rightChild, self.operator, to_llvm)
                        return self, False
                    else:
                        set_llvm_binary_operators(self.leftChild, self.rightChild, self.operator, to_llvm)
                return self, False

            elif not self.leftChild.getType() in (LiteralType.DOUBLE, LiteralType.FLOAT, LiteralType.INT) or \
                    not self.rightChild.getType() in (LiteralType.DOUBLE, LiteralType.FLOAT, LiteralType.INT):
                raise BinaryOp(self.leftChild.getType(), self.rightChild.getType(), self.operator, self.line)



            else:
                leftValue = float(self.leftChild.getValue())
                rightValue = float(self.rightChild.getValue())

                typeOfValue = self.leftChild.getHigherType(self.rightChild)

                if self.operator == "*":
                    res = leftValue * rightValue
                elif self.operator == "/":
                    res = leftValue / rightValue
                elif self.operator == "+":
                    res = leftValue + rightValue
                elif self.operator == "-":
                    res = leftValue - rightValue
                elif self.operator == "%":
                    res = leftValue % rightValue
                else:
                    raise NotSupported("binary operator", self.operator, self.line)

                if typeOfValue == LiteralType.INT:
                    res = int(res)

                newNode = Value(str(res), typeOfValue, self.line, self.parent)
                return newNode, True

        except BinaryOp:
            raise
        except NotSupported:
            raise

    def getVariables(self, fill: bool = True, scope=None):
        """
        returns the variable contained within the node
        :return:
        """
        res = self.leftChild.getVariables(fill, scope)
        right = self.rightChild.getVariables(fill, scope)
        res[0].extend(right[0])
        if not res[1] or not right[1]:
            res[1] = False
        return res

    def replaceVariables(self, values, fill: bool = True):
        """
        replaces the variables in the node with the actual values contained in values
        :param values: dictionary containing the variable names as keys and the corresponding values as values
        """
        self.leftChild.replaceVariables(values, fill)
        self.rightChild.replaceVariables(values, fill)

    def printTables(self, filePath: str, to_llvm=None):
        if to_llvm is not None:
            if ((isinstance(self.rightChild, Value) or isinstance(self.rightChild, Function) or isinstance(
                    self.rightChild, Array) or isinstance(self.rightChild, Pointer)) or
                    (isinstance(self.leftChild, Value) or isinstance(self.leftChild, Function) or isinstance(
                        self.leftChild, Array)) or isinstance(self.leftChild, Pointer)):
                if not (self.rightChild is None or self.leftChild is None):
                    set_llvm_binary_operators(self.leftChild, self.rightChild, self.operator, to_llvm)
        self.leftChild.printTables(filePath, to_llvm)
        self.rightChild.printTables(filePath, to_llvm)

    def getType(self):
        type1 = self.leftChild.getType()
        type2 = self.rightChild.getType()
        return getHighestType(type1, type2, self.line)


# Used to hold a unary operator with its operator and the operand in the right child
class UnaryOperator(AST_node):
    rightChild = None

    def __init__(self, oper: str, parent: AST_node = None, line: int = None):
        """
        :param oper:string containing the operator of the binary operation
        :param parent: AST_node type containing the parent of the current node in the AST
        :param line: int telling the line of the binary operator
        """
        self.operator = oper
        self.parent = parent
        self.line = line
        self.value = self.operator
        self.name = "unary"

    def __eq__(self, other):
        if not isinstance(other, UnaryOperator):
            return False
        return self.operator == other.operator and self.rightChild == other.rightChild and self.parent == other.parent \
            and self.variable == other.variable and self.level == other.level and \
            self.number == other.number and self.line == other.line

    def getValue(self):
        return self.operator

    def getLabel(self):
        return "\"Unary operator: " + self.operator + "\""

    def setRightChild(self, child):
        self.rightChild = child

    def fold(self, to_llvm=None):
        """
        This function will try to reduce the whole unary operation by first folding the child of the node.
        Thereafter, the unary operation will be calculated and a Value node will replace the current UnaryOperator
        node.
        :return: the replacing Value node
        """
        if not (isinstance(self.rightChild, Value) or isinstance(self.rightChild, Pointer)):
            self.rightChild = self.rightChild.fold(to_llvm)[0]
        try:
            if not (isinstance(self.rightChild, Value) or isinstance(self.rightChild, Pointer)):
                return self, False
            elif self.rightChild.getType() not in (
                    LiteralType.BOOL, LiteralType.INT, LiteralType.FLOAT) and self.operator == "!":
                raise ChildType("unary operator", self.rightChild.getType(), None, self.line)
            elif self.rightChild.variable:
                if to_llvm is not None:
                    set_llvm_unary_operators(self.rightChild, self.operator, to_llvm)
                return self, False
            else:
                if self.rightChild.getType() == LiteralType.FLOAT:
                    child = float(self.rightChild.getValue())
                elif self.rightChild.getType() == LiteralType.BOOL:
                    child = bool(self.rightChild.getValue())
                else:
                    child = int(self.rightChild.getValue())
                if self.operator == "-":
                    res = - child
                elif self.operator == "++":
                    res = child + 1
                elif self.operator == "--":
                    res = child - 1
                elif self.operator == "+":
                    res = + child
                elif self.operator == "!":
                    res = not child
                else:
                    raise NotSupported("unary operator", self.operator, self.line)
            if self.operator != "!":
                newNode = Value(str(res), self.rightChild.getType(), self.line, self.parent)
            else:
                newNode = Value(str(res), LiteralType.BOOL, self.line, self.parent)
            return newNode, True

        except ChildType:
            raise
        except NotSupported:
            raise

    def getVariables(self, fill: bool = True, scope=None):
        """
        returns the variable contained within the node
        :return:
        """
        return self.rightChild.getVariables(fill, scope)

    def replaceVariables(self, values, fill: bool = True):
        """
        replaces the variables in the node with the actual values contained in values
        :param values: dictionary containing the variable names as keys and the corresponding values as values
        """
        self.rightChild.replaceVariables(values, fill)

    def printTables(self, filePath: str, to_llvm=None):
        if to_llvm is not None:
            if (isinstance(self.rightChild, Value) or isinstance(self.rightChild, Function) or isinstance(
                    self.rightChild, Array) or isinstance(self.rightChild, Pointer)):
                set_llvm_unary_operators(self.rightChild, self.operator, to_llvm)
        self.rightChild.printTables(filePath, to_llvm)

    def getType(self):
        return self.rightChild.getType()


# Used for logical operators with the corresponding operator and the children holding the operators
class LogicalOperator(AST_node):
    leftChild = None
    rightChild = None

    def __init__(self, oper: str, parent: AST_node = None, line: int = None):
        """
        :param oper:string containing the operator of the binary operation
        :param parent: AST_node type containing the parent of the current node in the AST
        :param line: int telling the line of the binary operator
        """
        self.operator = oper
        self.parent = parent
        self.line = line
        self.name = "logical"

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
        self.rightChild = child

    def fold(self, to_llvm=None):
        """
        This function will try to reduce the whole logical operation by first folding the children of the node.
        Thereafter, the logical operation will be calculated and a Value node will replace the current LogicalOperator
        node.
        :return: the replacing Value node
        """
        if not (isinstance(self.leftChild, Value) or isinstance(self.leftChild, Pointer)):
            self.leftChild = self.leftChild.fold(to_llvm)[0]
        if not (isinstance(self.rightChild, Value) or isinstance(self.rightChild, Pointer)):
            self.rightChild = self.rightChild.fold(to_llvm)[0]

        try:
            if not (isinstance(self.leftChild, Value) or isinstance(self.leftChild, Pointer)) or \
                    not (isinstance(self.rightChild, Value) or isinstance(self.rightChild, Pointer)):
                return self, False
            # TODO: check if this is necessary
            # elif leftType not in (LiteralType.FLOAT, LiteralType.INT, LiteralType.BOOL, LiteralType.DOUBLE) \
            #         or rightType not in (LiteralType.FLOAT, LiteralType.INT, LiteralType.BOOL, LiteralType.DOUBLE):
            #     raise LogicalOp(self.leftChild.getType(), self.rightChild.getType(), self.operator, self.line)
            elif self.leftChild.variable or self.rightChild.variable:
                if to_llvm is not None:
                    set_llvm_binary_operators(self.leftChild, self.rightChild, self.operator, to_llvm)
                return self, False

            leftType = self.leftChild.getType()
            rightType = self.rightChild.getType()

            # if leftType != rightType:
            #     raise LogicalOp(self.leftChild.getType(), self.rightChild.getType(), self.operator, self.line)
            # elif self.operator in ("&&", "||") and self.leftChild.getType() != LiteralType.BOOL and \
            #         self.rightChild.getType() != LiteralType.BOOL:
            #     raise LogicalOp(self.leftChild.getType(), self.rightChild.getType(), self.operator, self.line)
            if self.leftChild.variable or self.rightChild.variable:
                return self, False
            else:
                self.leftChild.setValueToType()
                self.rightChild.setValueToType()

                # if self.operator in ("&&", "||") and self.leftChild.getType() != LiteralType.BOOL and \
                #         self.rightChild.getType() != LiteralType.BOOL:
                #     raise LogicalOp(self.leftChild.getType(), self.rightChild.getType(), self.operator, self.line)

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
                    raise NotSupported("logical operator", self.operator, self.line)

                resBool = bool(res)
                newNode = Value(resBool, LiteralType.BOOL, self.line, self.parent)
                return newNode, True

        except LogicalOp:
            raise
        except NotSupported:
            raise

    def getVariables(self, fill: bool = True, scope=None):
        """
        returns the variable contained within the node
        :return:
        """
        res = self.leftChild.getVariables(fill, scope)
        right = self.rightChild.getVariables(fill, scope)
        res[0].extend(right[0])
        if not res[1] or not right[1]:
            res[1] = False
        return res

    def replaceVariables(self, values, fill: bool = True):
        """
        replaces the variables in the node with the actual values contained in values
        :param values: dictionary containing the variable names as keys and the corresponding values as values
        """
        self.leftChild.replaceVariables(values, fill)
        self.rightChild.replaceVariables(values, fill)

    def printTables(self, filePath: str, to_llvm=None):
        if to_llvm is not None:
            if ((isinstance(self.rightChild, Value) or isinstance(self.rightChild, Function) or isinstance(
                    self.rightChild, Array) or isinstance(self.rightChild, Pointer)) or
                    (isinstance(self.leftChild, Value) or isinstance(self.leftChild, Function) or isinstance(
                        self.leftChild, Array)) or isinstance(self.leftChild, Pointer)):
                set_llvm_binary_operators(self.leftChild, self.rightChild, self.operator, to_llvm)
        self.leftChild.printTables(filePath, to_llvm)
        self.rightChild.printTables(filePath, to_llvm)

    def getType(self):
        type1 = self.leftChild.getType()
        type2 = self.rightChild.getType()
        return getHighestType(type1, type2, self.line)


# Used to hold a (re)declaration of a variable, the left child holds the variable and the left child the value/operation
# that needs to be placed in the variable
class Declaration(AST_node):
    leftChild = None
    rightChild = None

    def __init__(self, var: Value, line: int, parent: AST_node = None):
        """
        :param var: Value type that contains the variable that is being declared
        :param line: int telling the line at which the declaration is taking place
        :param parent: AST_node type containing the parent of this node in the AST
        """
        self.parent = parent
        self.leftChild = var
        self.rightChild = None
        self.operator = "="
        self.line = line
        self.name = "declaration"

    def __eq__(self, other):
        if not isinstance(other, LogicalOperator):
            return False
        return self.leftChild == other.leftChild and self.rightChild == other.rightChild and \
            self.parent == other.parent and self.variable == other.variable and self.level == other.level and \
            self.number == other.number and self.line == other.line

    def getLabel(self):
        return "\"Declaration: " + self.operator + "\""

    def setLeftChild(self, child):
        self.leftChild = child

    def getLeftChild(self):
        return self.leftChild

    def setRightChild(self, child):
        self.rightChild = child

    def getRightChild(self):
        return self.rightChild

    def fold(self, to_llvm=None):
        """
        This function will try to fold the tree by folding both children until they are a single Value-type node
        :return: it returns itself, but now with the folded children (if possible)
        """
        folded = True
        if not (isinstance(self.leftChild, Value) or isinstance(self.leftChild, Pointer) or
                isinstance(self.leftChild, Array)):
            temp = self.leftChild.fold(to_llvm)
            self.leftChild = temp[0]
            if not temp[1]:
                folded = False
        if not (isinstance(self.rightChild, Value) or isinstance(self.rightChild, Pointer) or
                isinstance(self.rightChild, EmptyNode) or isinstance(self.rightChild, Array)):
            temp = self.rightChild.fold(to_llvm)
            self.rightChild = temp[0]
            if not temp[1]:
                folded = False
        if self.rightChild.variable:
            folded = False

        highestType = self.leftChild.getHigherType(self.rightChild)
        try:
            if self.leftChild.getType() == highestType or self.leftChild.getType() is None:
                test = "a"
                if not isinstance(self.rightChild, Function) and self.rightChild.getValue() in ("True", "False") and \
                        self.leftChild.getType() in (LiteralType.INT, LiteralType.FLOAT):
                    if self.rightChild.getValue() == "True":
                        self.rightChild.setValue(1)
                    else:
                        self.rightChild.setValue(0)
                return self, folded
            else:
                raise WrongDeclaration(self.leftChild.getType(), self.rightChild.getType(), self.line)

        except WrongDeclaration:
            raise

    def getVariables(self, fill: bool = True, scope=None):
        """
        returns the variable contained within the node
        :return:
        """
        values = self.rightChild.getVariables(fill, scope)
        if not self.leftChild.declaration:
            temp = self.leftChild.getVariables(fill, scope)
            values[0].append(temp[0][0])
        return values

    def replaceVariables(self, values, fill: bool = True):
        """
        replaces the variables in the node with the actual values contained in values
        :param values: dictionary containing the variable names as keys and the corresponding values as values
        """
        try:
            if not self.leftChild.declaration:
                if self.leftChild.name == "array":
                    name = str(self.leftChild.pos) + str(self.leftChild.value)
                else:
                    name = self.leftChild.value
                if not name in values:
                    raise NotDeclared(name, self.leftChild.line)
                self.leftChild.type = values[name][1]
            if not isinstance(self.leftChild, Pointer):
                if isinstance(self.rightChild, Value) and self.rightChild.deref:
                    self.rightChild.replaceVariables(values, False)
                else:
                    self.rightChild.replaceVariables(values, fill)
            else:
                self.rightChild.replaceVariables(values, False)

        except NotDeclared:
            raise

    def printTables(self, filePath: str, to_llvm=None):
        self.leftChild.printTables(filePath, to_llvm)
        self.rightChild.printTables(filePath, to_llvm)


# Used to hold pointeres
class Pointer(AST_node):
    def __init__(self, value: str, valueType: LiteralType, line: int, level: int, parent: AST_node = None,
                 const: bool = False, decl: bool = False):
        """
        :param value: string referring to the name of the pointer
        :param valueType: LiteralType containing the type of the variable stored in the variable
        :param line: int telling the line where the pointer is positioned
        :param level: int telling the level of the pointer
        :param parent: AST_node type containing the parent of the current node in the AST
        :param const: bool telling if the pointer is a constant pointer
        :param decl: bool telling if this is a declaration of the pointer
        """
        self.value = value
        self.line = line
        self.pointerLevel = level
        self.type = valueType
        self.parent = parent
        self.variable = True
        self.const = const
        self.declaration = decl
        self.name = "pointer"

    def __eq__(self, other):
        if not isinstance(other, Pointer):
            return False
        return self.value == other.value and self.type == other.type and self.parent == other.parent and \
            self.variable == other.variable and self.pointerLevel == other.pointerLevel and \
            self.const == other.const and self.number == other.number and self.line == other.line

    def getValue(self):
        return self.value

    def setValue(self, val):
        self.value = val

    def getLine(self):
        return self.line

    def setLine(self, line):
        self.line = line

    def getLevel(self):
        return self.level

    def setLevel(self, level):
        self.level = level

    def getPointerLevel(self):
        return self.pointerLevel

    def setPointerLevel(self, pLevel):
        self.pointerLevel = pLevel

    def getLabel(self):
        return "\"Pointer: " + str(self.value) + "\""

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent

    def getVariable(self, fill: bool = True):
        return self.variable

    def setVariable(self, var):
        self.variable = var

    def getConst(self):
        return self.const

    def setConst(self, const):
        self.const = const

    def getDeclaration(self):
        return self.declaration

    def setDeclaration(self, decl):
        self.declaration = decl

    def getVariables(self, fill: bool = True, scope=None):
        """
        returns the variable contained within the node
        :return:
        """
        return [[(self.value, self.line)], True]

    def replaceVariables(self, values, fill: bool = True):
        """
        replaces the variables in the node with the actual values contained in values
        :param values: dictionary containing the variable names as keys and the corresponding values as values
        """
        if fill and self.variable and values[self.value][3]:
            self.value = values[self.value]
            #for key in values:
            #    self.type=values[key][1]
            self.type = values[self.value][1]
            self.variable = False
        elif self.variable:
            self.type = values[self.value][1]

    def getHigherType(self, node2: AST_node):
        """
        :param node2: AST_node type containing the other child of the parent node in the AST
        :return: returns the LiteralType with the highest priority (str>char; double>float>int)
        """
        type1 = self.type
        type2 = node2.getType()

        if isinstance(type1, str):
            type1 = LiteralType.getLiteral(type1)
        if isinstance(type2, str):
            type2 = LiteralType.getLiteral(type2)
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
            elif type1 == LiteralType.BOOL and type2 == LiteralType.BOOL:
                return LiteralType.BOOL
            elif type1 is None:
                return type2
            else:
                raise WrongType(type1, type2, self.line)

        except WrongType:
            raise


# Used for empty nodes in the AST if necessary
class EmptyNode(AST_node):
    def __init__(self, line: int, parent: AST_node = None, type_=None):
        """
        :param line: int, the line on which this node was formed
        :param parent: AST_node, the parent node of this node
        :param type_: LiteralType, the type of the values
        """
        self.value = None
        self.type = type_
        self.parent = parent
        self.variable = False
        self.const = False
        self.declaration = False
        self.line = line
        self.name = "empty"
        self.deref = False

    def getLabel(self):
        return "\"Empty Node: " + str(self.value) + "\""

    def getValue(self):
        return None

    def getValue(self):
        return self.value

    def setValue(self, val):
        self.value = val

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def getVariables(self, fill: bool = True, scope=None):
        """
        returns the variable contained within the node
        :return:
        """
        return [[], True]


class ReturnNode(AST_node):
    def __init__(self, value, line: int, parent: AST_node = None, type_=None):
        """
        :param line: int, the line on which this node was formed
        :param parent: AST_node, the parent node of this node
        :param type_: LiteralType, the type of the values
        """
        self.value = value
        self.type = type_
        self.parent = parent
        self.variable = False
        self.const = False
        self.declaration = False
        self.line = line
        self.name = "return"
        self.deref = False

    def getLabel(self):
        return "\"Return Node\""

    def getValue(self):
        return None

    def getValue(self):
        return self.value

    def setValue(self, val):
        self.value = val

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def getVariables(self, fill: bool = True, scope=None):
        """
        returns the variable contained within the node
        :return:
        """
        return [[], True]

    def fold(self, to_llvm):
        # self.value.foldTree(to_llvm)
        return self, True

    def replaceVariables(self, values, fill: bool = True):
        self.value.replaceVariables(values, fill)


class Include(AST_node):
    def __init__(self, value: str, line: int, parent: AST_node = None, type_=None):
        self.value = value
        self.type = type_
        self.parent = parent
        self.variable = False
        self.const = False
        self.declaration = False
        self.line = line
        self.name = "include"

    def getLabel(self):
        self.value = self.value.replace("\"", "'")
        return "\"Include Node: " + str(self.value) + "\""

    def getType(self):
        return self.type

    def getValue(self):
        return self.value

    def setValue(self, val):
        self.value = val

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def getVariables(self, fill: bool = True, scope=None):
        return [[], True]

    def fold(self, to_llvm):
        return self


# unnamed scopes gebruik scope node
# Used to hold unnamed scopes or function definitions
class Scope(AST_node):  # TODO: let it hold a block instead of trees
    block = None

    # TODO: check if block in Scope is cleaned -> same with while3
    def __init__(self, line: int, parent: AST_node = None, forward_declaration=False):
        """
        :param line: the line on which the scope/function was formed
        :param parent: the parent node of this node
        :param f_name: str, the name of the function (left as "" when it is an unnamed scope)
        :param f_return: AST_node, the return node of the function
        :param return_type: LiteralType, the type of the return value
        :param global_: bool, tells if it is a global varialbe or not
        :param parameters: sortedDict, the input parameters of the functions,
                            with the names as keys and Value nodes as values
        """
        self.parent = parent
        self.line = line
        self.f_name = ""
        self.f_return = None
        self.return_type = None
        self.global_ = False
        # hier moeten de parameters als values en pointers binnen
        self.parameters = dict()
        self.name = "scope"
        self.forward_declaration=forward_declaration

    def __eq__(self, other):
        if not isinstance(other, Scope):
            return False
        same = True
        if self.block is not None:
            same = self.block == other.block
        return self.parent == other.parent and self.line == other.line and same and self.f_name == other.f_name and \
            self.f_return == other.f_return and self.return_type == other.return_type and \
            self.parameters == other.parameters

    def setBlock(self, scope: block):
        self.block = scope

    def setReturnType(self, type):
        """
        sets the return type as a LiteralType based on the inputted string
        :param type: str, type of the return of the function
        """
        if type == "int":
            self.return_type = LiteralType.INT
        elif type == "float":
            self.return_type = LiteralType.FLOAT
        elif type == "bool":
            self.return_type = LiteralType.BOOL
        elif type == "char":
            self.return_type = LiteralType.CHAR

    def addParameter(self, val):
        """
        add an input variable to the function
        :param val: Value node, input variable of the function
        """
        if val.getValue() not in self.parameters.keys():
            self.parameters[val.getValue()] = val
        else:
            pass  # TODO: add error with duplicate inputs

    def addTree(self, ast: AST_node):
        self.block.addTree(ast)

    def getLabel(self):
        if self.f_name == "":
            return "\"New scope\""
        else:
            return "\"Function: " + self.f_name + "\""

    def fold(self, to_llvm=None):
        """
        'folds' the node and gives true with a nameless scope and false with a function
        """
        for param in self.parameters:
            if not (isinstance(self.parameters[param], Value) or isinstance(self.parameters[param], Array) or
                    isinstance(self.parameters[param], Pointer)):
                self.parameters[param] = self.parameters[param].fold()[0]
        if self.f_return is not None:
            self.f_return = self.f_return.foldTree()[0]
            self.return_type = self.f_return.root.getType()
        if self.f_name == "":
            return self, True
        else:
            return self, False

    def getVariables(self, fill: bool = True, scope=None):
        """
        returns the variable contained within the node
        :return:
        """
        if self.f_name == "":
            self.block.cleanBlock(fill=fill)
            return [[], True]
        else:
            # res = self.block.cleanBlock(onlyLocal=True)
            self.block.cleanBlock(onlyLocal=True)
            if self.f_return is not None:
                self.block.fillLiterals(self.f_return, True)
            res = []
            # for elem in res:
            for elem in self.block.getVariables(fill=False):
                if len(elem) != 0 and elem[0][0] not in self.parameters and \
                        not self.block.symbols.findSymbol(elem[0][0]):
                    res.append(elem[0])
            if self.f_return is not None:
                for elem in self.f_return.getVariables(fill=False):
                    if isinstance(elem, list):
                        if len(elem) > 0 and elem[0][0] not in self.parameters and \
                                not self.block.symbols.findSymbol(elem[0][0]):
                            res.append(elem[0])
            return [res, True]

    def replaceVariables(self, values, fill: bool = True):
        """
        replaces the variables in the node with the actual values contained in values
        :param values: dictionary containing the variable names as keys and the corresponding values as values
        """
        pass

    def printTables(self, filePath: str, to_llvm=None):
        for param in self.parameters:
            self.parameters[param].printTables(filePath, to_llvm)
        if self.f_return is not None:
            self.f_return.printTables(filePath, to_llvm)
        self.block.printTables(filePath, to_llvm)

    def getType(self):
        return self.f_return.root.getType()


# Used to hold the for loops TODO: is this used?
class For(AST_node):
    f_dec = None
    Condition = None
    f_incr = None
    c_block = None

    def __init__(self, line):
        self.line = line
        self.name = "for"


# Used to hold if/elif/else nodes with the corresponding conditions and bodies
class If(AST_node):
    Condition = None
    c_block = None
    """
    if(){}
    if (){} else{}
    if (){} else if(){}
    if (){} ele if(){} else if(){}...
    if (){} ele if(){} else if(){}... else {}
    """

    def __init__(self, line, operator: ConditionType = ConditionType.IF, parent=None):
        """
        :param line: int, line on which the condition was generated
        :param operator: ConditionType, tells if it is an IF, ELIF or ELSE condition
        :param parent: AST_node, the parent of the current node
        :param Condition: AST_node, the condition to check if the if needs to be performed
        :param c_block: block, contains the body of the if
        """
        self.line = line
        self.operator = operator
        self.parent = parent
        self.name = "if"

    def __eq__(self, other):
        if not isinstance(other, If):
            return False
        return self.operator == other.operator and self.line == other.line and self.Condition == other.Condition and \
            self.c_block == other.c_block

    def setCondition(self, con: AST_node):
        try:
            if self.operator != ConditionType.ELSE:
                self.Condition = con
            else:
                raise ConditionElse(self.line)

        except ConditionElse:
            raise

    def setBlock(self, newBlock: block):
        self.c_block = newBlock

    def getLabel(self):
        return "\"" + self.operator.__str__() + "\""

    def fold(self, to_llvm=None):
        """
        'folds' the if condition as much as possible
        :param to_llvm:
        :return:
        """
        res = None
        if self.operator != ConditionType.ELSE:
            res = self.Condition.fold(to_llvm)
            self.Condition = res[0]
            return self, res[1]
        # self.c_block = self.c_block.fold(to_llvm)
        return self, True

    def getVariables(self, fill: bool = True, scope=None):
        """
        returns the variable contained within the node
        :return:
        """
        res = None
        if self.operator != ConditionType.ELSE:
            res = self.Condition.getVariables(fill, scope)
        self.c_block.cleanBlock(fill=fill)
        if res is None:
            return [[], True]
        else:
            return res

    def replaceVariables(self, values, fill: bool = True):
        """
        replaces the variables in the node with the actual values contained in values
        :param values: dictionary containing the variable names as keys and the corresponding values as values
        """
        if self.operator != ConditionType.ELSE:
            self.Condition.replaceVariables(values, fill)
            # self.c_block.fillBlock()

    def printTables(self, filePath: str, to_llvm=None):
        if self.operator != ConditionType.ELSE:
            self.Condition.printTables(filePath, to_llvm)
        self.c_block.printTables(filePath, to_llvm)


# Used to indicate a break TODO: stop generation of tree in the body
class Break(AST_node):
    def __init__(self, line):
        self.line = line
        self.name = "break"
        self.value = None
        self.type = None
        self.parent = None
        self.variable = False
        self.const = False
        self.declaration = False
        self.deref = False

    def getLabel(self):
        return "\"Break Node: " + str(self.value) + "\""

    def getValue(self):
        return None

    def getValue(self):
        return self.value

    def setValue(self, val):
        self.value = val

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def getVariables(self, fill: bool = True, scope=None):
        """
        returns the variable contained within the node
        :return:
        """
        return [[], True]

    def fold(self, to_llvm):
        return self


# Used to indicate a continue in the code
class Continue(AST_node):
    def __init__(self, line):
        self.line = line
        self.name = "continue"
        self.value = None
        self.type = None
        self.parent = None
        self.variable = False
        self.const = False
        self.declaration = False
        self.deref = False

    def getLabel(self):
        return "\"Continue Node: " + str(self.value) + "\""

    def getValue(self):
        return None

    def getValue(self):
        return self.value

    def setValue(self, val):
        self.value = val

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def getVariables(self, fill: bool = True, scope=None):
        """
        returns the variable contained within the node
        :return:
        """
        return [[], True]

    def fold(self, to_llvm):
        return self

class String(AST_node):
    def __init__(self, line, value):
        self.line = line
        self.name = "string"
        self.value = value
        self.type = None
        self.parent = None
        self.variable = False
        self.const = False
        self.declaration = False
        self.deref = False

    def getLabel(self):
        return "\"String Node: " + self.value + "\""

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value=value
        return self.value

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def getVariables(self, fill: bool = True, scope=None):
        """
        returns the variable contained within the node
        :return:
        """
        return [[], True]
    def replaceVariables(self,values, fill: bool = True ):
        pass

    def fold(self, to_llvm):
        return self

# Used to hold a while loop
class While(AST_node):
    Condition = None
    c_block = None
    """
    child condition
    child block: scope --> special node (multiple children)--> callable seperate from condition
    """

    def __init__(self, line, parent=None):
        """
        :param line: int, line on which the while loop was initiated
        :param parent: AST_node, the parent node of the current node
        :param Condtion: AST_node, the condition based on which the while loop needs to be excecuted
        :param c_block: block, the body of the while loop
        """
        self.line = line
        self.parent = parent
        self.name = "while"
        self.stop_loop = False

        """
        condition--> tree--> fold--> bool
        block (scope) ; store value in block of condition
        translate for loop to while loop
        """
        """"
        global scope--> program
        block: (level+nr) --> unique id
             : if function --> keep name (callable)
        een node scope while lus->trees in block combineren
        in program set id/nodes-> fold/dot aanpassen 
         
         {
            
         }
         
        """

    def __eq__(self, other):
        if not isinstance(other, If):
            return False
        return self.operator == other.operator and self.line == other.line and self.Condition == other.Condition and \
            self.c_block == other.c_block

    def setCondition(self, con: AST_node):
        self.Condition = con

    def setBlock(self, newBlock: block):
        self.c_block = newBlock

    def getLabel(self):
        return "\"while\""

    def fold(self, to_llvm=None):
        return self, False

    def getVariables(self, fill: bool = True, scope=None):
        """
        returns the variable contained within the node
        :return:
        """
        res = self.Condition.getVariables(fill, scope)[0]
        # self.Condition=self.Condition.root
        self.Condition.fold()
        for elem in self.c_block.getVariables(False)[0]:
            res.append(elem)
        # self.c_block.cleanBlock(fill=False) # TODO: check if something needs to be done instead of this one (to fill in variables)
        return [res, False]

    def replaceVariables(self, values, fill: bool = True):
        """
        replaces the variables in the node with the actual values contained in values
        :param values: dictionary containing the variable names as keys and the corresponding values as values
        """
        pass

    def printTables(self, filePath: str, to_llvm=None):
        self.Condition.printTables(filePath, to_llvm)
        self.c_block.printTables(filePath, to_llvm)


"""
deze node is bij aanroepen van functies bv. 
int i= functie(0)
"""


# Used to hold function calls within the AST
class Function(AST_node):

    def __init__(self, f_name, line, parent=None, decl=False):
        """
        :param f_name: str, the name of the function
        :param line: int, the line on which the function was called
        :param parent: AST_node, the parent node of the current node
        :param decl: ???
        :param param: a list of Value nodes containing the input variables
        :param counter: int, keeps track of the number of variables that is inputted
        :param expected: orderedDict, tells which type the input variables should have
        """
        self.line = line
        self.parent = parent
        self.param = dict()
        self.f_name = f_name
        self.decl = decl
        self.name = "function"
        self.counter = 0  # TODO: use this to check which variable is being read
        self.expected = None

    def __eq__(self, other):
        if not isinstance(other, Function):
            return False
        return self.line == other.line and self.param == other.param and self.f_name == other.f_name and \
            self.decl == other.decl

    def addParameter(self, var, scope, line: int):
        # TODO: check type of input parameter and amount of added input parameters

        # TODO: dit moet anders --> als value/pointer/ref wordt doorgegeven
        # TODO: add parameters to the symbol table of the body
        # var= &x, *x, 21,
        # ]\\\\\\\
        # TODO: check --> verwachte parameter ?
        # self.param.append(var) # TODO: variable comes in as string -> look up in Symbtable -> check type -> make Value/Pointer node
        # if self.expected is None:
        #     parent = scope.block
        #     while parent.name != "program":
        #         parent = parent.parent
        #     self.setExpected(parent.functions.findFunction(self.name, self.line))
        # try:
        #     if self.counter >= len(self.expected):
        #         raise FunctionParam(var, self.expected, line)
        #
        # except FunctionParam:
        #     raise
        #
        # exp = self.expected[next(islice(self.expected.items(), self.counter, None))]
        # given = scope.symbols.findSymbol(var)[1]
        # try:
        #     if exp == given:
        pos = len(self.param)
        if isinstance(var, str):
            if var.isdigit():
                val = Value(var, None, line)
            else:
                val = Value(var, None, line, None, True)
            self.param[pos] = val
        else:
            self.param[pos] = var
        # try:
        #     if len(self.param) > len(self.expected):
        #         raise FunctionParam(self.f_name, len(self.expected), self.line)
        #
        # except FunctionParam:
        #     raise
        #     else:
        #         raise TypeDeclaration(var, exp, given, line)
        #
        # except TypeDeclaration:
        #     raise

    def getLabel(self):
        return "\"function call: " + self.f_name + "\""

    def setExpected(self, exp: dict):
        self.expected = exp

    def fold(self, to_llvm=None):
        return self, False

    def getType(self):
        return self.expected["return"]

    def getVariables(self, fill: bool = True,
                     scope=None):  # TODO: for now no filling of variables because this can run multiple times
        """
        returns the variable contained within the node
        :return:
        """
        # try: TODO: get test to work!
        #     if len(self.param) < len(self.expected):
        #         raise FunctionParam(self.f_name, len(self.expected), self.line)
        # except FunctionParam:
        #     raise
        prog = scope
        while prog.name != "program":
            prog = prog.parent
        self.expected = prog.functions.findFunction(self.f_name, self.line)
        try:
            params = []
            if len(self.expected) - 1 != len(self.param):
                raise FunctionParam(self.f_name, len(self.expected) - 1, self.line)
            pos = 0
            for exp in self.expected:
                if exp == "return":
                    continue
                expec = self.expected[exp]
                given = self.param[pos]
                if given.variable:
                    givenType = scope.symbols.findSymbol(given.value)
                else:
                    givenType = [[], given.type]
                if expec != str(givenType[1]):
                    raise FunctionParamType(self.f_name, exp, givenType, expec, self.line)
                else:
                    if self.param[pos].variable:
                        params.append((self.param[pos].value, self.param[pos].line))
                        self.param[pos].type = givenType[1]
                pos += 1;

        except FunctionParam:
            raise
        # for param in self.param:
        #     if self.param[param].variable:
        #         params.append((self.param[param].value, self.param[param].line))
        return [params, True]

    def replaceVariables(self, values, fill: bool = True):  # TODO: possible to get from listener if it is a variable or not???
        """
        replaces the variables in the node with the actual values contained in values
        :param values: dictionary containing the variable names as keys and the corresponding values as values
        """
        for var in self.param:
            if self.param[var].variable:
                if fill:
                    self.param[var].variable = False  # TODO: check if this is right bool
                self.param[var].replaceVariables(values, fill)

            # Used to set initialisation or call of arrays


class Array(AST_node):
    def __init__(self, value: str, pos: int, valueType: LiteralType, line: int, init: bool = False, parent=None,
                 declaration: bool = False):
        """
        :param value: str, the name of the array
        :param pos: int, the length of the array when initialization or the position of the called value
        :param valueType: LiteralType, the type of values in the array
        :param line: int, the line on which the array was initialized
        :param init: bool, tells if it is an initialization of the array
        :param parent: AST_node, the parent node of the current node
        :param isValue: bool, tells if the array contains an actual value or a variable
        """

        self.value = value
        # DEZE WORD IN DE LISTENER GESEt
        self.declaration = declaration
        # todo : needs to be ast
        self.pos = pos
        self.type = valueType
        self.line = line
        self.init = init
        self.parent = parent
        self.isValue = False
        self.name = "array"

        self.arrayContent = []

    def getPosition(self):
        return self.pos

    def __eq__(self, other):
        return self.value == other.value and self.pos == other.pos and self.type == other.type and \
            self.line == other.line and self.init == other.init

    def getType(self):
        return self.type

    # TODO: content kan var, value, pointer, function zijn
    def setArrayContent(self, content):
        self.arrayContent = content

    def setType(self, type_):
        self.type = type_

    def getValue(self):
        return str(self.pos)

    def getLabel(self):
        if self.init:
            return "\"array: " + str(self.value) + "\nsize: " + str(self.pos) + "\""
        elif self.isValue:
            return "\"array value: " + str(self.value) + "\""
        else:
            return "\"array: " + str(self.value) + "\nposition: " + str(self.pos) + "\""

    def getVariables(self, fill: bool = True, scope=None):
        """
        returns the variable contained within the node
        :return:
        """
        if self.declaration:
            return [[], True]
        return [[(str(self.pos) + str(self.value), self.line)], True]

    def replaceVariables(self, values, fill: bool = True):
        """
        replaces the variables in the node with the actual values contained in values
        :param values: dictionary containing the variable names as keys and the corresponding values as values
        """
        name = str(self.pos) + str(self.value)
        if fill and values and values[name][3]:
            self.type = values[name][1]
            self.value = values[name][0]
            self.isValue = True
        elif self.variable:
            self.type = values[name][1]

    def getHigherType(self, node2: AST_node):
        """
        :param node2: AST_node type containing the other child of the parent node in the AST
        :return: returns the LiteralType with the highest priority (str>char; double>float>int)
        """
        # if not (isinstance(node2, Value) or isinstance(node2, Array) or isinstance(node2, Function)):
        #     return self.type
        type1 = self.type
        type2 = node2.getType()

        if isinstance(type1, str):
            type1 = LiteralType.getLiteral(type1)
        if isinstance(type2, str):
            type2 = LiteralType.getLiteral(type2)

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
            elif type1 == LiteralType.BOOL and type2 == LiteralType.BOOL:
                return LiteralType.BOOL
            elif type1 is None:
                return type2
            elif type1 in (LiteralType.INT, LiteralType.FLOAT) and type2 == LiteralType.BOOL:
                return type1
            else:
                raise WrongType(type1, type2, self.line)

        except WrongType:
            raise

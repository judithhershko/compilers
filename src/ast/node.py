from enum import Enum
from src.ErrorHandeling.GenerateError import *
from src.LLVM.Helper_LLVM import set_llvm_binary_operators
from src.ast.node_types.node_type import LiteralType, ConditionType
from itertools import islice


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
        return "\"Comment: " + self.value + "\""

    def getType(self):
        return self.type

    def getVariables(self):
        return [[], True]


class Print(AST_node):
    def __init__(self, lit):
        self.parent = None
        self.value = lit
        self.name = "print"

    def __eq__(self, other):
        if not isinstance(other, Print):
            return False
        return self.value == other.value

    def getValue(self):
        return self.value

    def getVariables(self):
        return self.value.getVariables()

    def setValue(self, val):
        self.value = val

    def getLabel(self):
        return "\"Print: " + self.value + "\""


class Value(AST_node):
    def __init__(self, lit: str, valueType, line: int, parent: AST_node = None, variable: bool = False,
                 const: bool = False, decl: bool = False):
        """
        :param lit: string containing the value (int, string, variable, ...) of the node
        :param valueType: LiteralType containing the type of element saved in the node
        :param line: int telling the line where the element from the node is located
        :param parent: AST_node-object containing the parent of the current node in the AST
        :param variable: boolean telling if the saved element is a variable or an actual value
        :param const: boolean telling if the saved element is a const (only used when talking about variables)
        :param decl: boolean telling if the saved element is a declaration of the variable
        """
        self.value = lit
        self.type = valueType
        self.parent = parent
        self.variable = variable
        self.const = const
        self.declaration = decl
        self.line = line
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
        if isinstance(self.value, int) or isinstance(self.value, float):
            return "\"Literal: " + str(self.value) + "\""
        elif isinstance(self.value, str):
            return "\"Literal: " + self.value + "\""

    def getType(self):
        return self.type

    def getVariables(self):
        if self.variable:
            return [[(self.value, self.line)], True]
        else:
            return [[], True]

    def replaceVariables(self, values):
        if len(values) == 0:
            pass
        elif self.variable and values[self.value][3]:
            self.type = values[self.value][1]
            self.value = values[self.value][0]
            self.variable = False
        elif self.variable:
            self.type = values[self.value][1]

    def getHigherType(self, node2: AST_node):
        """
        :param node2: AST_node type containing the other child of the parent node in the AST
        :return: returns the LiteralType with the highest priority (str>char; double>float>int)
        """
        if not (isinstance(node2, Value) or isinstance(node2, Array)):
            return self.type
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
                return self, False
            elif self.leftChild.variable or self.rightChild.variable:
                if to_llvm is not None:
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

    def getVariables(self):
        res = self.leftChild.getVariables()
        right = self.rightChild.getVariables()
        res[0].extend(right[0])
        if not res[1] or not right[1]:
            res[1] = False
        return res

    def replaceVariables(self, values):
        self.leftChild.replaceVariables(values)
        self.rightChild.replaceVariables(values)


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

    def getVariables(self):
        return self.rightChild.getVariables()

    def replaceVariables(self, values):
        self.rightChild.replaceVariables(values)


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
            elif self.leftChild.variable or self.rightChild.variable:
                if to_llvm is not None:
                    set_llvm_binary_operators(self.leftChild, self.rightChild, self.operator, to_llvm)
                return self, False

            leftType = self.leftChild.getType()
            rightType = self.rightChild.getType()

            if leftType != rightType:
                raise LogicalOp(self.leftChild.getType(), self.rightChild.getType(), self.operator, self.line)
            elif self.operator in ("&&", "||") and self.leftChild.getType() != LiteralType.BOOL and \
                    self.rightChild.getType() != LiteralType.BOOL:
                raise LogicalOp(self.leftChild.getType(), self.rightChild.getType(), self.operator, self.line)
            elif self.leftChild.variable or self.rightChild.variable:
                return self, False

            else:
                self.leftChild.setValueToType()
                self.rightChild.setValueToType()

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

                newNode = Value(res, LiteralType.BOOL, self.line, self.parent)
                return newNode, True

        except LogicalOp:
            raise
        except NotSupported:
            raise

    def getVariables(self):
        res = self.leftChild.getVariables()
        right = self.rightChild.getVariables()
        res[0].extend(right[0])
        if not res[1] or not right[1]:
            res[1] = False
        return res

    def replaceVariables(self, values):
        self.leftChild.replaceVariables(values)
        self.rightChild.replaceVariables(values)


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
                if self.rightChild.getValue() in ("True", "False") and \
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

    def getVariables(self):
        return self.rightChild.getVariables()

    def replaceVariables(self, values):
        self.rightChild.replaceVariables(values)


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

    def getVariable(self):
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

    def getVariables(self):
        return [[(self.value, self.line)], True]

    def replaceVariables(self, values):
        if self.variable and values[self.value][3]:
            self.value = values[self.value]
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


class EmptyNode(AST_node):
    def __init__(self, line: int, parent: AST_node = None, type_=None):
        self.value = None
        self.type = type_
        self.parent = parent
        self.variable = False
        self.const = False
        self.declaration = False
        self.line = line
        self.name = "empty"

    def getLabel(self):
        return "\"Empty Node: " + str(self.value) + "\""

    def getType(self):
        return self.type

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

    def getVariables(self):
        return [[], True]


# unnamed scopes gebruik scope node
class Scope(AST_node):  # TODO: let it hold a block instead of trees
    block = None

    # TODO: check if block in Scope is cleaned -> same with while3
    def __init__(self, line: int, parent: AST_node = None):
        self.parent = parent
        self.line = line
        self.f_name = ""
        self.f_return = None
        self.return_type = None
        self.global_ = False
        # hier moeten de parameters als values en pointers binnen
        self.parameters = dict()
        self.name = "scope"

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
        if type == "int":
            self.return_type = LiteralType.INT
        elif type == "float":
            self.return_type = LiteralType.FLOAT
        elif type == "bool":
            self.return_type = LiteralType.BOOL
        elif type == "char":
            self.return_type = LiteralType.CHAR

    def addParameter(self, val):
        # val is ofwel een pointer, ofwel een value en zit in param[]
        if val.getValue() not in self.parameters.keys():
            self.parameters[val.getValue()] = val

    def addTree(self, ast: AST_node):
        self.block.addTree(ast)

    def getLabel(self):
        if self.f_name == "":
            return "\"New scope\""
        else:
            return "\"Function: " + self.f_name + "\""

    def fold(self, to_llvm=None):
        if self.f_name == "":
            return self, True
        else:
            return self, False

    def getVariables(self):
        if self.f_name == "":
            self.block.cleanBlock()
            return [[], True]
        else:
            res = []
            for elem in self.block.getVariables():
                if len(elem) != 0 and elem[0][0] not in self.parameters:
                    res.append(elem[0])
            self.block.cleanBlock(onlyLocal=True)
            return [res, True]

    def replaceVariables(self, values):
        pass


class For(AST_node):
    f_dec = None
    Condition = None
    f_incr = None
    c_block = None

    def __init__(self, line):
        self.line = line
        self.name = "for"


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
        res = None
        if self.operator != ConditionType.ELSE:
            res = self.Condition.fold(to_llvm)
            self.Condition = res[0]
            return self, res[1]
        # self.c_block = self.c_block.fold(to_llvm)
        return self, True

    def getVariables(self):
        res = None
        if self.operator != ConditionType.ELSE:
            res = self.Condition.getVariables()
        self.c_block.cleanBlock()
        if res is None:
            return [[], True]
        else:
            return res

    def replaceVariables(self, values):
        if self.operator != ConditionType.ELSE:
            self.Condition.replaceVariables(values)
            # self.c_block.fillBlock()


class Break(AST_node):
    def __init__(self, line):
        self.line = line
        self.name = "break"


class Continue(AST_node):
    def __init__(self, line):
        self.line = line
        self.name = "cont"


class While(AST_node):
    Condition = None
    c_block = None
    """
    child condition
    child block: scope --> special node (multiple children)--> callable seperate from condition
    """

    def __init__(self, line, parent=None):
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

    def getVariables(self):
        res = self.Condition.getVariables()[0]
        self.Condition.fold()
        for elem in self.c_block.getVariables()[0]:
            res.append(elem)
        self.c_block.fold()
        return [res, False]

    def replaceVariables(self, values):
        pass


"""
deze node is bij aanroepen van functies bv. 
int i= functie(0)
"""


class Function(AST_node):

    def __init__(self, f_name, line, parent=None, decl=False):
        self.line = line
        self.parent = parent
        self.param = []
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

    def addParameter(self, var, scope, line):
        # TODO: dit moet anders --> als value/pointer/ref wordt doorgegeven
        # var= &x, *x, 21,
        # ]\\\\\\\
        # TODO: check --> verwachte parameter ?
        # self.param.append(var) # TODO: variable comes in as string -> look up in Symbtable -> check type -> make Value/Pointer node
        # if self.expected is None:
        #     self.setExpected(scope.functions.findFunction(self.name))
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
        val = Value(var, None, line)
        self.param.append(val)
        # self.counter += 1
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

    def getVariables(self):  # TODO: for now no filling of variables because this can run multiple times
        params = []
        for param in self.param:
            params.append(param.value)
        return [params, True]

    def replaceVariables(self, values):  # TODO: possible to get from listener if it is a variable or not???
        for var in self.param:
            var.variable = True
            var.replaceVariables(values)


class Array(AST_node):
    def __init__(self, value: str, pos: int, valueType: LiteralType, line: int, init: bool = False, parent=None):
        self.value = value
        self.pos = pos
        self.type = valueType
        self.line = line
        self.init = init
        self.parent = parent
        self.isValue = False
        self.name = "array"

    def __eq__(self, other):
        return self.value == other.value and self.pos == other.pos and self.type == other.type and \
               self.line == other.line and self.init == other.init

    def getType(self):
        return self.type

    def getValue(self):
        if self.init:
            return str(self.value)
        else:
            return str(self.value)

    def getLabel(self):
        if self.init:
            return "\"array: " + str(self.value) + "\nsize: " + str(self.pos) + "\""
        elif self.isValue:
            return "\"array value: " + str(self.value) + "\""
        else:
            return "\"array: " + str(self.value) + "\nposition: " + str(self.pos) + "\""

    def getVariables(self):
        if self.init:
            return [[], True]
        return [[(str(self.pos) + str(self.value), self.line)], True]

    def replaceVariables(self, values):
        name = str(self.pos) + str(self.value)
        if values[name][3]:
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
        if not (isinstance(node2, Value) or isinstance(node2, Array)):
            return self.type
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

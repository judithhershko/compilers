from pandas._libs.lib import Enum
import json


class LiteralType(Enum):
    NUM = 1
    STR = 2
    VAR = 3
    DOUBLE = 4
    INT = 5
    CHAR = 6
    BOOL = 7
    FLOAT = 8
    POINTER = 9

    def __str__(self):
        return self.name

    def getLiteral(name: str):
        if name == "NUM":
            return LiteralType.NUM
        elif name == "STR":
            return LiteralType.STR
        elif name == "VAR":
            return LiteralType.VAR
        elif name == "DOUBLE":
            return LiteralType.DOUBLE
        elif name == "INT":
            return LiteralType.INT
        elif name == "CHAR":
            return LiteralType.CHAR
        elif name == "BOOL":
            return LiteralType.BOOL
        elif name == "FLOAT":
            return LiteralType.FLOAT
        elif name == "POINTER":
            return LiteralType.POINTER


class ConditionType(Enum):
    IF = 0
    ELIF = 1
    ELSE = 2

    def __str__(self):
        if self.value == 0:
            return "if"
        elif self.value == 1:
            return "else if"
        else:
            return "else"


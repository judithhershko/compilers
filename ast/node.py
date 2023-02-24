class ast_node():
    pass

class value(ast_node):
    def __init__(self, input):
        self.value = input

class binaryOperator(ast_node):
    def __int__(self, oper, value1, value2):
        self.operator = oper
        self.leftSide = value1
        self.rightSide = value2

class unaryOperator(ast_node):
    def __int__(self, oper, input):
        self.operator = oper
        self.value = input
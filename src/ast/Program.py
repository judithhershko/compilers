from .SymbolTable import *
from .AST import *
from src.ErrorHandeling.GenerateError import *
import sys
# from colorama import Fore
# from colorama import Style
# from colorama import init as colorama_init
#
# colorama_init()


class program:
    def __init__(self):
        self.symbols = SymbolTable()
        self.ast = AST()
        self.blocks = []

    def getAst(self):
        return self.ast

    def getSymbolTable(self):
        return self.symbols

    def addBlock(self, block):
        self.blocks.append(block)

    def fillLiterals(self):
        variables = self.ast.getVariables()
        notFound = []
        values = dict()
        if not variables:
            return "filled"
        for elem in variables:
            temp = self.symbols.findSymbol(elem[0])
            if temp:
                values[elem[0]] = temp
            else:
                notFound.append(elem)
        try:
            if notFound:
                raise Undeclared(notFound)
            else:
                self.ast.replaceVariables(values)
                return "filled"

        except Undeclared as arg:
            # print(arg)
            raise
            # for elem in notFound:
            #     err = "Error: Line " + str(elem[1]) + " has an undefined " + str(elem[0]) + "\n"
            #     print(err, file=sys.stderr)

from .SymbolTable import *
from .AST import *
from src.ErrorHandeling.GenerateError import *
from .block import *
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

    def addBlock(self, block: block):
        self.blocks.append(block)

    def fillLiterals(self, tree: AST):
        """
         This function will try to replace the variables in the AST with the actual values.
         """
        variables = tree.getVariables()
        notFound = []
        values = dict()
        if not variables:
            return "filled"
        for elem in variables:
            temp = self.symbols.findSymbol(elem[0], elem[1])
            if temp:
                values[elem[0]] = temp
            else:
                notFound.append(elem)
        try:
            if notFound:
                raise Undeclared(notFound)
            else:
                tree.replaceVariables(values)
                return "filled"

        except Undeclared:
            raise

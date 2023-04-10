from .SymbolTable import SymbolTable
from src.ErrorHandeling.GenerateError import *
from .block import block
from .AST import AST


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
            temp = self.symbols.findSymbol(elem[0])
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

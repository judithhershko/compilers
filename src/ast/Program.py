#from .AST import AST
#from .SymbolTable import *
import AST
import SymbolTable
import sys


class Program:
    def __init__(self):
        self.symbols = SymbolTable.SymbolTable()
        self.ast = AST.AST()
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
            temp = self.symbols.findSymbol(elem)
            if temp:
                values[elem] = temp
            else:
                notFound.append(elem)

        if notFound:
            return "missing"

        self.ast.replaceVariables(values)
        return "filled"

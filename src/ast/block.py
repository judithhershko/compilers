import sys
from src.ast import program
from src.ast.AST import AST
from src.ast.symbolTable import *


class block():
    def __init__(self, parent):
        self.symbols = SymbolTable()
        self.ast = AST()
        self.parent = parent
        self.blocks = []

    def getSymbolTable(self):
        return self.symbols

    def getParent(self):
        return self.parent

    def addBlock(self, newBlock):
        self.blocks.append(newBlock)

    def getAst(self):
        return self.ast

    def fillLiterals(self):
        variables = self.ast.getVariables()
        notFound = []
        values = dict()
        for elem in variables:
            temp = self.symbols.findSymbol(elem)
            if temp:
                values[elem] = temp
            else:
                notFound.append(elem)

        current = self
        while not isinstance(current, program.program) and notFound:
            current = self.getParent()
            variables = notFound
            notFound = []
            for elem in variables:
                temp = current.symbols.findSymbol(elem)
                if temp:
                    values[elem] = temp
                else:
                    notFound.append(elem)

        if notFound:
            print("There are undeclared variables", file=sys.stderr)

        self.ast.replaceVariables(values)

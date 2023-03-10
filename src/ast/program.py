import symbolTable
import AST
import sys


class program():
    def __init__(self):
        self.symbols = symbolTable.symbolTable()
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

import symbolTable
import AST
import sys


class program():
    def __init__(self):
        self.symbols = symbolTable.symbolTable()
        self.ast = AST.AST()
        self.blocks = None

    def getAst(self):
        return self.ast

    def getSymbolTable(self):
        return self.symbols

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

        if notFound:
            print("There are undeclared variables", file=sys.stderr)

        self.ast.replaceVariables(values)

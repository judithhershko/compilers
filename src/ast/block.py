import symbolTable
import AST
import sys

class block():
    def __init__(self, parent):
        self.symbols = symbolTable.symbolTable()
        self.ast = AST.AST()
        self.parent = parent
        self.blocks = None

    def getSymbolTable(self):
        return self.symbols

    def getParent(self):
        return self.parent

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
        while current.getParent() and notFound:
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

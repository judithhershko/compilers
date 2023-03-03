import symbolTable
import AST

class block():
    def __init__(self, parent):
        self.symbols = symbolTable.symbolTable()
        self.ast = AST.AST()
        self.parent = parent
        self.blocks = None

    def getSymbolTable(self):
        return self.symbols

    def fillLiterals(self):
        pass
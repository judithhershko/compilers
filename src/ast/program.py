import symbolTable
import AST


class program():
    def __init__(self):
        self.symbols = symbolTable.symbolTable()
        self.ast = AST.AST()
        self.blocks = None

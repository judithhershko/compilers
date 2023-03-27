import sys
from src.ast import Program
from src.ast.AST import AST
from src.ast.SymbolTable import *
from src.ErrorHandeling.GenerateError import *


class block:
    def __init__(self, parent):
        self.symbols = SymbolTable()
        self.ast = AST()
        self.parent = parent
        self.blocks = []
        # moet weg?
        self.trees = []

    def getSymbolTable(self):
        return self.symbols

    def getParent(self):
        return self.parent

    def addBlock(self, newBlock):
        self.blocks.append(newBlock)

    def getAst(self):
        return self.ast

    def fillLiterals(self, tree: AST):
        """
        This function will try to replace the variables in the AST with the actual values. If it can not find the
        variables in its own symbol table, it will look at the symbol tables of its parents
        """
        variables = tree.getVariables()
        notFound = []
        values = dict()
        for elem in variables:
            temp = self.symbols.findSymbol(elem[0])
            if temp:
                values[elem[0]] = temp
            else:
                notFound.append(elem)

        current = self
        while not isinstance(current, Program.program) and notFound:
            current = self.getParent()
            variables = notFound
            notFound = []
            for elem in variables:
                temp = current.symbols.findSymbol(elem[0])
                if temp:
                    values[elem[0]] = temp
                else:
                    notFound.append(elem)
        try:
            if notFound:
                raise Undeclared(notFound)
            elif values:
                tree.replaceVariables(values)

        except Undeclared:
            raise

import json
import os

from .SymbolTable import SymbolTable, FunctionTable
from src.ErrorHandeling.GenerateError import *
from .block import block
from .AST import AST
from src.ast.node import Scope


class program:
    # TODO: add functions for fold and fill literals as in block
    def __init__(self):
        self.symbols = SymbolTable()
        self.functions = FunctionTable()
        self.ast = AST()
        self.blocks = []
        self.include_added = False
        self.block = block(None)
        self.trees = []
        self.tree = Scope(0)
        self.tree.global_ = True
        self.level = None
        self.number = None
        self.name = "program"

    def getAst(self):
        return self.ast

    def getSymbolTable(self):
        return self.symbols

    def getFunctionTable(self):
        return self.functions

    #
    # def addBlock(self, block: block):
    #     self.blocks.append(block)

    def addTree(self, tree: AST):
        self.trees.append(tree)

    def getLabel(self):
        return "\"the program\""

    def getId(self):
        return str(self.level) + "." + str(self.number)

    def setNumber(self, number):
        self.number = number

    def setLevel(self, level):
        self.level = level

    def fillLiterals(self, tree: AST):
        """
         This function will try to replace the variables in the AST with the actual values.
         """
        res = tree.getVariables()
        variables = res[0]
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
                # return "filled"

        except Undeclared:
            raise

        return res

    def fold(self):
        folded = True
        if self.ast.root is not None:
            temp = self.ast.foldTree()
            self.ast = temp[0]
            if not temp[1]:
                folded = False
        foldedBlocks = []
        foldedTrees = []
        for block in self.blocks:
            temp = block.fold()
            foldedBlocks.append(temp[0])
            if not temp[1]:
                folded = False
        for tree in self.trees:
            temp = tree.foldTree()
            foldedTrees.append(temp[0])  # TODO: double check if a tree or a node in put in here
            if not temp[1]:
                folded = False
        self.blocks = foldedBlocks
        self.trees = foldedTrees

        return self, folded

    def fillBlock(self):  # TODO make more efficient
        if self.ast.root is not None:
            self.fillLiterals(self.ast)
        for tree in self.trees:
            self.fillLiterals(tree)
        for localBlock in self.blocks:
            localBlock.fillBlock()

    def generateDot(self, fileName: str):
        nodes = self.getId() + " [label=" + self.getLabel() + "]"
        edges = ""

        tree = self.ast
        edges = edges + "\n" + self.getId() + "--" + tree.root.getId()
        res = tree.toDot(tree.root)
        nodes = nodes + res[0]
        edges = edges + res[1]

        output = "graph ast {\n" + nodes + "\n\n" + edges + "\n}"
        file = open(fileName, "w")
        file.write(output)
        file.close()
        return output

    def toDot(self):  # TODO: check what to do with blocks -> get them in right order with the trees
        nodes = self.getId() + " [label=" + self.getLabel() + "]"
        edges = ""

        for tree in self.trees:
            edges = edges + "\n" + self.getId() + "--" + tree.root.getId()
            res = tree.toDot(tree.root)
            nodes = nodes + res[0]
            edges = edges + res[1]

        return nodes, edges

    def setNodeIds(self, level: int = 0, number: int = 0):
        self.setNumber(number)
        self.setLevel(level)
        if self.ast.root is not None:
            number = self.ast.setNodeIds(self.ast.root, level + 1, number + 1)
        for tree in self.trees:
            number = tree.setNodeIds(tree.root, level + 1, number + 1)
        for localBlock in self.blocks:
            number = localBlock.setNodeIds(level + 1, number + 1)

        return number

    def makeUnfillable(self):
        self.symbols.makeUnfillable()

    def cleanProgram(self):
        if self.ast.root is not None:
            tree = self.ast
            res = self.fillLiterals(tree.root)
            all = res[1]
            if not all:
                self.makeUnfillable()
            fold = tree.foldTree()
            if fold[1] and (tree.root.name == "declaration" or tree.root.name == "array"):
                self.symbols.addSymbol(tree.root, True)
            elif tree.root.name == "declaration" or tree.root.name == "array":
                none = tree.createUnfilledDeclaration(tree.root)
                self.symbols.addSymbol(none, True, False)
            elif tree.root.name == "scope" and tree.root.f_name != "":
                self.parent.functions.addFunction(tree.root)
            tree.setNodeIds(tree.root)
            # self.generateDot("./generated/output/programAST.dot")
            return res[0]

    def printTables(self, filePath):
        symbolPath = filePath + self.name + "_symbols_" + str(self.level) + "_" + str(self.number) + ".csv"
        functionPath = filePath + self.name + "_functions_" + str(self.level) + "_" + str(self.number) + ".csv"
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        self.symbols.table.to_csv(symbolPath)
        with open(functionPath, 'w') as file:
            file.write(json.dumps(self.functions.functions))
        if self.ast.root is not None:
            self.ast.printTables(filePath)

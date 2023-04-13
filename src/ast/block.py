from src.ast.SymbolTable import SymbolTable
from src.ErrorHandeling.GenerateError import *
from .AST import AST


class program:
    pass


class block:
    def __init__(self, parent, name=""):
        self.symbols = SymbolTable()
        self.ast = AST()
        self.parent = parent
        self.blocks = []
        self.trees = []
        self.fname = name
        self.id = ''
        self.level = None
        self.number = None

    def __eq__(self, other):
        if not isinstance(other, block):
            return False
        blocksTrue = True
        treesTrue = True
        for i in range(len(self.blocks)):
            if self.blocks[i] != other.blocks[i]:
                blocksTrue = False
        for j in range(len(self.trees)):
            if self.trees[j] != other.trees[j]:
                treesTrue = False
        return self.symbols == other.symbols and self.ast == other.ast and \
               self.fname == other.fname and self.id == other.id and blocksTrue and treesTrue

    def getId(self):
        return str(self.level) + "." + str(self.number)

    def setNumber(self, number):
        self.number = number

    def setLevel(self, level):
        self.level = level

    def getSymbolTable(self):
        return self.symbols

    def getParent(self):
        return self.parent

    def addBlock(self, newBlock):
        self.blocks.append(newBlock)

    def addTree(self, newTree):
        self.trees.append(newTree)

    def getAst(self):
        return self.ast

    def getLabel(self):
        return "\"new scope: \""

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
        while not isinstance(current, program) and notFound:
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

    def fold(self):
        if self.ast.root is not None:
            self.ast = self.ast.foldTree()
        foldedBlocks = []
        foldedTrees = []
        for block in self.blocks:
            foldedBlocks.append(block.fold())
        for tree in self.trees:
            foldedTrees.append(tree.foldTree())  # TODO: double check if a tree or a node in put in here
        self.blocks = foldedBlocks
        self.trees = foldedTrees

        return self

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

        for tree in self.trees:
            edges = edges + "\n" + self.getId() + "--" + tree.root.getId()
            res = tree.toDot(tree.root)
            nodes = nodes + res[0]
            edges = edges + res[1]

        output = "graph ast {\n" + nodes + "\n\n" + edges + "\n}"
        file = open(fileName, "w")
        file.write(output)
        file.close()
        return output

    def toDot(self): # TODO: check what to do with blocks -> get them in right order with the trees
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

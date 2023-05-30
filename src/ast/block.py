from src.ast.SymbolTable import SymbolTable
from src.ErrorHandeling.GenerateError import *
from .AST import AST


class program:
    pass


class Declaration:
    pass


class block:
    def __init__(self, parent):
        self.symbols = SymbolTable()
        if parent is not None:
            self.symbols.setParent(parent.symbols)
        self.ast = AST()
        self.parent = parent
        self.blocks = []
        self.trees = []
        self.line = None
        self.id = ''
        self.level = None
        self.number = None
        self.name = "block"
        self.cleaned = False

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
               self.id == other.id and blocksTrue and treesTrue

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

    def setParent(self, parent):
        self.parent = parent
        self.symbols.setParent(parent.symbols)

    def addBlock(self, newBlock):
        self.blocks.append(newBlock)

    def addTree(self, newTree):
        self.trees.append(newTree)

    def getAst(self):
        return self.ast

    def getLabel(self):
        return "\"new scope\""

    def getVariables(self, fill: bool = True, f_name: str = None):
        result = []
        for tree in self.trees:
            result.append(tree.getVariables(fill, scope=self, f_name=f_name)[0])
            if tree.root.name == "declaration" and tree.root.leftChild.name == "array":
                name = str(tree.root.leftChild.pos.value) + str(tree.root.leftChild.value)
            elif tree.root.name == "declaration":
                name = tree.root.leftChild.value
            if not fill and tree.root.name == "declaration" and self.symbols.findSymbol(name) is None:
                dec = tree.createUnfilledDeclaration(tree.root)
                self.symbols.addSymbol(dec, False, fill)
        return result

    def fillLiterals(self, tree: AST, onlyLocal: bool = False, fill: bool = True, f_name: str = None):
        """
        This function will try to replace the variables in the AST with the actual values. If it can not find the
        variables in its own symbol table, it will look at the symbol tables of its parents
        """
        res = tree.getVariables(scope=self, f_name=f_name)
        variables = res[0]
        notFound = []
        values = dict()
        for elem in variables:
            if len(elem) == 0:
                continue
            temp = self.symbols.findSymbol(elem[0], line = elem[1])
            if temp:
                values[elem[0]] = temp
            else:
                notFound.append(elem)

        current = self
        if onlyLocal:
            tree.replaceVariables(values, fill)
            return res
        while not current.name == "program" and notFound:
            current = current.getParent()
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
                tree.replaceVariables(values, fill)

        except Undeclared:
            raise

        return res

    def fold(self, llvm=None):
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

    def toDot(self):  # TODO: check what to do with blocks -> get them in right order with the trees
        nodes = "\n" + self.getId() + " [label=" + self.getLabel() + "]"
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
        if self.parent is not None:
            self.parent.symbols.makeUnfillable()

    def cleanBlock(self, glob: bool = False, onlyLocal: bool = False, fill: bool = True, f_name: str = None):
        if self.cleaned:
            return []
        allVar = []
        cleanTrees = []
        for tree in self.trees:
            res = self.fillLiterals(tree.root, onlyLocal, fill, f_name=f_name)
            if fill and tree.root.name == "scope" and tree.root.f_name != "":
                self.parent.functions.addFunction(tree.root)
            all = res[1]
            if not all:
                self.makeUnfillable()
            fold = tree.foldTree()
            if fill and fold[1] and (tree.root.name == "declaration" or tree.root.name == "array"):
                self.symbols.addSymbol(tree.root, glob)
            elif fill and not fold[1] and tree.root.name == "declaration" and tree.root.leftChild.name == "pointer": # TODO: also add to program if works
                self.symbols.addSymbol(tree.root, glob)
            elif fill and tree.root.name == "declaration" or tree.root.name == "array":
                if tree.root.name == "declaration" and tree.root.rightChild.name == "val" and tree.root.rightChild.deref:
                    self.symbols.addSymbol(tree.root, glob)
                else:
                    none = tree.createUnfilledDeclaration(tree.root)
                    self.symbols.addSymbol(none, glob, False)
            for elem in res[0]:
                allVar.append(elem)
            cleanTrees.append(tree)
            if tree.root.name in ("break", "continue", "return"):
                break
        self.trees = cleanTrees
        self.cleaned = True
        return allVar

    def setParent(self, parent):
        self.parent = parent
        self.symbols.setParent(parent.symbols)

    def printTables(self, filePath: str, to_llvm=None):
        symbolPath = filePath + self.name + "_symbols_" + str(self.level) + "_" + str(self.number) + ".csv"
        self.symbols.table.to_csv(symbolPath)
        for tree in self.trees:
            tree.printTables(filePath)

from .AST import *


class Scope(AST_node):
    trees = []

    def __init__(self, line: int, parent: AST_node = None):
        self.parent = parent
        self.line = line

    def addTree(self, ast: AST):
        self.trees.append(ast)

    def getLabel(self):
        return "\"New scope: \""

    def fold(self):
        folded = []
        for tree in self.trees:
            folded.append(tree.foldTree())
        self.trees = folded
        return self

    def getVariables(self):
        res = []
        for tree in self.trees:
            res.extend(tree.getVarialbes())
        return res

    def replaceVariables(self, values):
        for tree in self.trees:
            tree.replaceVariables(values)
from .node import *


class block:
    pass


class AST:
    root = None

    def __eq__(self, other):
        if not isinstance(other, AST):
            return False
        return self.root == other.root

    def setRoot(self, root: AST_node):
        self.root = root

    def setNodeIds(self, nextNode: AST_node, level: int = 0, number: int = 0):
        """
        This function will give all nodes, in the tree given by its root, its own id and the level in the tree it is at
        :param nextNode: AST_node type containing the root of the AST
        :param level: int giving the level in the tree the next node will be at
        :param number: int giving the number/id of the next node
        :return: int the number of the current node so that it can be used to always increase the value in the previous
        node
        """
        nextNode.setNumber(number)
        nextNode.setLevel(level)
        if isinstance(nextNode, BinaryOperator) or isinstance(nextNode, LogicalOperator) or \
                isinstance(nextNode, Declaration):
            number = self.setNodeIds(nextNode.leftChild, level + 1, number + 1)
            number = self.setNodeIds(nextNode.rightChild, level + 1, number + 1)
        elif isinstance(nextNode, UnaryOperator):
            number = self.setNodeIds(nextNode.rightChild, level + 1, number + 1)
        elif isinstance(nextNode, Scope):
            for tree in nextNode.trees:
                number = self.setNodeIds(tree, level + 1, number + 1)
        elif isinstance(nextNode, If):
            number = self.setNodeIds(nextNode.Condition, level + 1, number + 1)
            number = self.setNodeIds(nextNode.c_block, level + 1, number + 1)
        elif isinstance(nextNode, block):
            number = self.setNodeIds(nextNode.getAst().root, level + 1, number + 1)
            for tree in nextNode.trees:
                number = self.setNodeIds(tree.root, level + 1, number + 1)
            for localBlock in nextNode.blocks:
                number = self.setNodeIds(localBlock, level + 1, number + 1)

        return number

    def generateDot(self, fileName: str):
        """
        Generates the dot file of the AST
        :param fileName: str containing the name of the file where the dot representation needs to be stored
        :return: the AST in dot language
        """
        nodes = self.root.getId() + " [label=" + self.root.getLabel() + "]"
        edges = ""

        if isinstance(self.root, BinaryOperator) or isinstance(self.root, LogicalOperator) or \
                isinstance(self.root, Declaration):
            edges = self.root.getId() + "--" + self.root.leftChild.getId() + "\n" + self.root.getId() + "--" + \
                    self.root.rightChild.getId()
            res = self.toDot(self.root.leftChild)
            nodes = nodes + res[0]
            edges = edges + res[1]
            res = self.toDot(self.root.rightChild)
            nodes = nodes + res[0]
            edges = edges + res[1]
        elif isinstance(self.root, UnaryOperator):
            edges = self.root.getId() + "--" + self.root.value.getId()
            res = self.toDot(self.root.value)
            nodes = nodes + res[0]
            edges = edges + res[1]
        elif isinstance(self.root, Scope):
            for tree in self.root.trees:
                edges = edges + "\n" + self.root.getId() + "--" + tree.getId()
                res = self.toDot(tree)
                nodes = nodes + res[0]
                edges = edges + res[1]
        elif isinstance(self.root, If):
            edges = self.root.getId() + "--" + self.root.Condition.getId() + "\n" + self.root.getId() + "--" + \
                    self.root.c_block.getId()
            res = self.toDot(self.root.c_block)
            nodes = nodes + res[0]
            edges = edges + res[1]

        output = "graph ast {\n" + nodes + "\n\n" + edges + "\n}"
        file = open(fileName, "w")
        file.write(output)
        file.close()
        return output

    def toDot(self, root):
        """
        This function transforms the AST, given by its root, to the dot language
        :param root: the root of the AST that needs to be changed to a dot representation
        :return: the nodes and edges as a string
        """
        nodes = "\n" + root.getId() + " [label=" + root.getLabel() + "]"
        edges = ""

        if isinstance(root, block):
            edges = "\n" + root.getId() + "--" + root.getAst().root.getId()
            res = self.toDot(root.getAst().root)
            nodes = nodes + res[0]
            edges = edges + res[1]
            for tree in root.trees:
                edges = "\n" + root.getId() + "--" + tree.root.getId()
                res = self.toDot(tree.root)
                nodes = nodes + res[0]
                edges = edges + res[1]
            for localBlock in root.blocks:
                edges = "\n" + root.getId() + "--" + localBlock.getId()
                res = self.toDot(localBlock)
                nodes = nodes + res[0]
                edges = edges + res[1]
        elif isinstance(root, BinaryOperator) or isinstance(root, LogicalOperator) or \
                isinstance(root, Declaration):
            edges = "\n" + root.getId() + "--" + root.leftChild.getId() + "\n" + root.getId() + "--" + \
                    root.rightChild.getId()
            res = self.toDot(root.leftChild)
            nodes = nodes + res[0]
            edges = edges + res[1]
            res = self.toDot(root.rightChild)
            nodes = nodes + res[0]
            edges = edges + res[1]
        elif isinstance(root, UnaryOperator):
            edges = "\n" + root.getId() + "--" + root.rightChild.getId()
            res = self.toDot(root.rightChild)
            nodes = nodes + res[0]
            edges = edges + res[1]
        elif isinstance(root, Scope):
            for tree in root.trees:
                edges = edges + "\n" + root.getId() + "--" + tree.getId()
                res = self.toDot(tree)
                nodes = nodes + res[0]
                edges = edges + res[1]

        return nodes, edges

    def foldTree(self):
        """
        This function tries to reduce the size of the tree as much as possible
        """
        if not isinstance(self.root, Value):
            self.root = self.root.fold()

    def getVariables(self):
        return self.root.getVariables()

    def replaceVariables(self, values):
        self.root.replaceVariables(values)

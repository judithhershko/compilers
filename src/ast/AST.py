from . import node


class AST:
    root = None

    def __eq__(self, other):
        if not isinstance(other, AST):
            return False
        return self.root == other.root

    def setRoot(self, root: node.AST_node):
        self.root = root

    def setNodeIds(self, nextNode: node.AST_node, level: int = 0, number: int = 0):
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
        if isinstance(nextNode, node.BinaryOperator) or isinstance(nextNode, node.LogicalOperator) or \
                isinstance(nextNode, node.Declaration):
            number = self.setNodeIds(nextNode.leftChild, level + 1, number + 1)
            number = self.setNodeIds(nextNode.rightChild, level + 1, number + 1)
        elif isinstance(nextNode, node.UnaryOperator):
            number = self.setNodeIds(nextNode.rightChild, level + 1, number + 1)

        return number

    def generateDot(self, fileName: str):
        """
        Generates the dot file of the AST
        :param fileName: str containing the name of the file where the dot representation needs to be stored
        :return: the AST in dot language
        """
        nodes = self.root.getId() + " [label=" + self.root.getLabel() + "]"
        edges = ""

        if isinstance(self.root, node.BinaryOperator) or isinstance(self.root, node.LogicalOperator) or \
                isinstance(self.root, node.Declaration):
            edges = self.root.getId() + "--" + self.root.leftChild.getId() + "\n" + self.root.getId() + "--" + \
                    self.root.rightChild.getId()
            res = self.toDot(self.root.leftChild)
            nodes = nodes + res[0]
            edges = edges + res[1]
            res = self.toDot(self.root.rightChild)
            nodes = nodes + res[0]
            edges = edges + res[1]
        elif isinstance(self.root, node.UnaryOperator):
            edges = self.root.getId() + "--" + self.root.value.getId()
            res = self.toDot(self.root.value)
            nodes = nodes + res[0]
            edges = edges + res[1]

        output = "graph ast {\n" + nodes + "\n\n" + edges + "\n}"
        file = open("./src/ast/dotFiles/" + fileName + ".dot", "w")
        file.write(output)
        file.close()
        return output

    def toDot(self, root: node.AST_node):
        """
        This function transforms the AST, given by its root, to the dot language
        :param root: the root of the AST that needs to be changed to a dot representation
        :return: the nodes and edges as a string
        """
        nodes = "\n" + root.getId() + " [label=" + root.getLabel() + "]"
        edges = ""

        if isinstance(root, node.BinaryOperator) or isinstance(root, node.LogicalOperator) or \
                isinstance(root, node.Declaration):
            edges = "\n" + root.getId() + "--" + root.leftChild.getId() + "\n" + root.getId() + "--" + \
                    root.rightChild.getId()
            res = self.toDot(root.leftChild)
            nodes = nodes + res[0]
            edges = edges + res[1]
            res = self.toDot(root.rightChild)
            nodes = nodes + res[0]
            edges = edges + res[1]
        elif isinstance(root, node.UnaryOperator):
            edges = "\n" + root.getId() + "--" + root.rightChild.getId()
            res = self.toDot(root.rightChild)
            nodes = nodes + res[0]
            edges = edges + res[1]

        return nodes, edges

    def foldTree(self):
        """
        This function tries to reduce the size of the tree as much as possible
        """
        if not isinstance(self.root, node.Value):
            self.root = self.root.fold()

    def getVariables(self):
        return self.root.getVariables()

    def replaceVariables(self, values):
        self.root.replaceVariables(values)

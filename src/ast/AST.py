import node


class AST():
    root = None

    def __eq__(self, other):
        if not isinstance(other, AST):
            return False
        return self.root == other.root

    def setRoot(self, root):
        self.root = root

    def setNodeIds(self, nextNode, level=0, number=0):
        nextNode.setNumber(number)
        nextNode.setLevel(level)
        if isinstance(nextNode, node.BinaryOperator) or isinstance(nextNode, node.LogicalOperator):
            number = self.setNodeIds(nextNode.leftChild, level + 1, number + 1)
            number = self.setNodeIds(nextNode.rightChild, level + 1, number + 1)
        elif isinstance(nextNode, node.UnaryOperator):
            number = self.setNodeIds(nextNode.child, level + 1, number + 1)

        return number

    def generateDot(self, fileName):
        nodes = self.root.getId() + " [label=" + self.root.getLabel() + "]"
        edges = ""

        if isinstance(self.root, node.BinaryOperator) or isinstance(self.root, node.LogicalOperator):
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
        file = open("dotFiles/" + fileName + ".dot", "w")
        file.write(output)
        file.close()
        return output

    def toDot(self, root):
        nodes = "\n" + root.getId() + " [label=" + root.getLabel() + "]"
        edges = ""

        if isinstance(root, node.BinaryOperator) or isinstance(root, node.LogicalOperator):
            edges = "\n" + root.getId() + "--" + root.leftChild.getId() + "\n" + root.getId() + "--" + \
                    root.rightChild.getId()
            res = self.toDot(root.leftChild)
            nodes = nodes + res[0]
            edges = edges + res[1]
            res = self.toDot(root.rightChild)
            nodes = nodes + res[0]
            edges = edges + res[1]
        elif isinstance(root, node.UnaryOperator):
            edges = "\n" + root.getId() + "--" + root.child.getId()
            res = self.toDot(root.child)
            nodes = nodes + res[0]
            edges = edges + res[1]

        return nodes, edges

    def foldTree(self):
        if not isinstance(self.root, node.Value):
            self.root = self.root.fold()

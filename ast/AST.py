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
            number = self.setNodeIds(nextNode.leftSide, level + 1, number + 1)
            number = self.setNodeIds(nextNode.rightSide, level + 1, number + 1)
        elif isinstance(nextNode, node.UnaryOperator):
            number = self.setNodeIds(nextNode.value, level + 1, number + 1)

        return number

    def generateDot(self):
        nodes = self.root.getId() + " [label=" + self.root.getLabel() + "]"
        edges = ""

        if isinstance(self.root, node.BinaryOperator) or isinstance(self.root, node.LogicalOperator):
            edges = self.root.getId() + "--" + self.root.leftSide.getId() + "\n" + self.root.getId() + "--" + \
                    self.root.rightSide.getId()
            res = self.toDot(self.root.leftSide)
            nodes = nodes + res[0]
            edges = edges + res[1]
            res = self.toDot(self.root.rightSide)
            nodes = nodes + res[0]
            edges = edges + res[1]
        elif isinstance(self.root, node.UnaryOperator):
            edges = self.root.getId() + "--" + self.root.value.getId()
            res = self.toDot(self.root.value)
            nodes = nodes + res[0]
            edges = edges + res[1]

        output = "graph ast {\n" + nodes + "\n\n" + edges + "\n}"
        file = open("dotFiles/result.dot", "w")
        file.write(output)
        file.close()
        return output

    def toDot(self, root):
        nodes = "\n" + root.getId() + " [label=" + root.getLabel() + "]"
        edges = ""

        if isinstance(root, node.BinaryOperator) or isinstance(root, node.LogicalOperator):
            edges = "\n" + root.getId() + "--" + root.leftSide.getId() + "\n" + root.getId() + "--" + \
                    root.rightSide.getId()
            res = self.toDot(root.leftSide)
            nodes = nodes + res[0]
            edges = edges + res[1]
            res = self.toDot(root.rightSide)
            nodes = nodes + res[0]
            edges = edges + res[1]
        elif isinstance(root, node.UnaryOperator):
            edges = "\n" + root.getId() + "--" + root.value.getId()
            res = self.toDot(root.value)
            nodes = nodes + res[0]
            edges = edges + res[1]

        return nodes, edges

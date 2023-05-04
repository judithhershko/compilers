from src.ast.node import *


# class block:
#     pass
#

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
        if isinstance(nextNode,AST):
            nextNode=nextNode.root
        nextNode.setNumber(number)
        nextNode.setLevel(level)
        if isinstance(nextNode, BinaryOperator) or isinstance(nextNode, LogicalOperator) or \
                isinstance(nextNode, Declaration):
            number = self.setNodeIds(nextNode.leftChild, level + 1, number + 1)
            number = self.setNodeIds(nextNode.rightChild, level + 1, number + 1)
        elif isinstance(nextNode, UnaryOperator):
            number = self.setNodeIds(nextNode.rightChild, level + 1, number + 1)
        elif isinstance(nextNode, Scope):
            if nextNode.f_name != "":
                for tree in nextNode.parameters:
                    number = self.setNodeIds(nextNode.parameters[tree], level + 1, number + 1)
                number = nextNode.block.setNodeIds(level + 1, number + 1)
                if nextNode.f_return is not None:
                    number = self.setNodeIds(nextNode.f_return.root, level + 1, number + 1)
            else:
                number = nextNode.block.setNodeIds(level, number)
        elif isinstance(nextNode, If):
            if nextNode.operator != ConditionType.ELSE:
                number = self.setNodeIds(nextNode.Condition, level + 1, number + 1)
            # number = self.setNodeIds(nextNode.c_block, level + 1, number + 1)
            number = nextNode.c_block.setNodeIds(level + 1, number + 1)
        elif isinstance(nextNode, While):
            number = self.setNodeIds(nextNode.Condition, level + 1, number + 1)
            number = nextNode.c_block.setNodeIds(level + 1, number + 1)
        elif isinstance(nextNode, Function):
            for value in nextNode.param:
                number = self.setNodeIds(nextNode.param[value], level + 1, number + 1)
        elif isinstance(nextNode, Array):
            for node in nextNode.arrayContent:
                number = self.setNodeIds(node, level + 1, number + 1)
        # elif isinstance(nextNode, block):
        # number = self.setNodeIds(nextNode.getAst().root, level + 1, number + 1)
        # for tree in nextNode.trees:
        #     number = self.setNodeIds(tree.root, level + 1, number + 1)
        # for localBlock in nextNode.blocks:
        #     number = self.setNodeIds(localBlock, level + 1, number + 1)

        return number

    def generateDot(self, fileName: str):
        """
        Generates the dot file of the AST
        :param fileName: str containing the name of the file where the dot representation needs to be stored
        :return: the AST in dot language
        """
        nodes = self.root.getId() + " [label=" + self.root.getLabel() + "]"
        edges = ""

        # if isinstance(self.root, block):
        #     edges = "\n" + self.root.getId() + "--" + self.root.getAst().root.getId()
        #     res = self.toDot(self.root.getAst().root)
        #     nodes = nodes + res[0]
        #     edges = edges + res[1]
        #     for tree in self.root.trees:
        #         edges = "\n" + self.root.getId() + "--" + tree.root.getId()
        #         res = self.toDot(tree.root)
        #         nodes = nodes + res[0]
        #         edges = edges + res[1]
        #     for localBlock in self.root.blocks:
        #         edges = "\n" + self.root.getId() + "--" + localBlock.getId()
        #         res = self.toDot(localBlock)
        #         nodes = nodes + res[0]
        #         edges = edges + res[1]
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
            edges = self.root.getId() + "--" + self.root.rightChild.getId()
            res = self.toDot(self.root.rightChild)
            nodes = nodes + res[0]
            edges = edges + res[1]
        elif isinstance(self.root, Function):
            for param in self.root.param:
                edges = edges + "\n" + self.root.getId() + "--" + self.root.param[param].getId()
                res = self.toDot(self.root.param[param])
                nodes = nodes + res[0]
                edges = edges + res[1]
        elif isinstance(self.root, Scope):
            # if self.root.f_name != "":
            #     params = self.root.parameters
            #     for param in self.root.parameters:
            #         edges = edges + "\n" + self.getId() + "--" + tree.root.getId()
            #         res = tree.toDot(tree.root)
            #         nodes = nodes + res[0]
            #         edges = edges + res[1]
            res = self.root.block.toDot()
            nodes = nodes + res[0]
            edges = "\n" + edges + res[1]
        elif isinstance(self.root, If):
            if self.root.operator != ConditionType.ELSE:
                edges = self.root.getId() + "--" + self.root.Condition.getId() + "\n" + self.root.getId() + "--" + \
                        self.root.c_block.getId()
                temp = self.toDot(self.root.Condition)
                nodes = nodes + temp[0]
                edges = edges + temp[1]
            else:
                edges = self.root.getId() + "--" + self.root.c_block.getId()
            # res = self.toDot(self.root.c_block)
            res = self.root.c_block.toDot()
            nodes = nodes + res[0]
            edges = edges + res[1]
        elif isinstance(self.root, While):
            edges = self.root.getId() + "--" + self.root.Condition.getId() + "\n" + self.root.getId() + "--" + \
                    self.root.c_block.getId()
            temp = self.toDot(self.root.Condition)
            nodes = nodes + temp[0]
            edges = edges + temp[1]
            res = self.root.c_block.toDot()
            nodes = nodes + res[0]
            edges = edges + res[1]
        elif isinstance(self.root, Function):
            for value in self.root.param:
                edges = edges + "\n" + self.root.getId() + "--" + value.getId()
                nodes = nodes + "\n" + value.getId() + " [label=" + value.getLabel() + "]"
        elif isinstance(self.root, Array):
            for node in self.root.arrayContent:
                edges = edges + "\n" + self.root.getId() + "--" + node.getId()
                nodes = nodes + "\n" + node.getId() + " [label=" + node.getLabel() + "]"

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

        # if isinstance(root, block):
        #     edges = "\n" + root.getId() + "--" + root.getAst().root.getId()
        #     res = self.toDot(root.getAst().root)
        #     nodes = nodes + res[0]
        #     edges = edges + res[1]
        #     for tree in root.trees:
        #         edges = "\n" + root.getId() + "--" + tree.root.getId()
        #         res = self.toDot(tree.root)
        #         nodes = nodes + res[0]
        #         edges = edges + res[1]
        #     for localBlock in root.blocks:
        #         edges = "\n" + root.getId() + "--" + localBlock.getId()
        #         res = self.toDot(localBlock)
        #         nodes = nodes + res[0]
        #         edges = edges + res[1]
        if isinstance(root, BinaryOperator) or isinstance(root, LogicalOperator) or \
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
        elif isinstance(root, Function):
            for param in root.param:
                edges = edges + "\n" + root.getId() + "--" + root.param[param].getId()
                res = self.toDot(root.param[param])
                nodes = nodes + res[0]
                edges = edges + res[1]
        elif isinstance(root, Scope):
            if root.f_name != "":
                for param in root.parameters:
                    edges = edges + "\n" + root.getId() + "--" + root.parameters[param].getId()
                    res = self.toDot(root.parameters[param])
                    nodes = nodes + res[0]
                    edges = edges + res[1]
                edges = edges + "\n" + root.getId() + "--" + root.block.getId()
                if root.f_return is not None:
                    edges = edges + "\n" + root.getId() + "--" + root.f_return.root.getId()
                    res = self.toDot(root.f_return.root)
                    nodes = nodes + res[0]
                    edges = edges + res[1]
            else:
                nodes = "\n"
            res = root.block.toDot()
            nodes = nodes + res[0]
            edges = edges + res[1]
        elif isinstance(root, If):
            if root.operator != ConditionType.ELSE:
                edges = edges + "\n" + root.getId() + "--" + root.Condition.getId() + "\n" + root.getId() + "--" + \
                        root.c_block.getId()
                temp = self.toDot(root.Condition)
                nodes = nodes + temp[0]
                edges = edges + temp[1]
            else:
                edges = edges + "\n" + root.getId() + "--" + root.c_block.getId()
            # res = self.toDot(root.c_block)
            res = root.c_block.toDot()
            nodes = nodes + res[0]
            edges = edges + res[1]
        elif isinstance(root, While):
            if isinstance(root.Condition,AST):
                root.Condition=root.Condition.root
            edges = edges + "\n" + root.getId() + "--" + root.Condition.getId() + "\n" + root.getId() + "--" + \
                    root.c_block.getId()
            temp = self.toDot(root.Condition)
            nodes = nodes + temp[0]
            edges = edges + temp[1]
            res = root.c_block.toDot()
            nodes = nodes + res[0]
            edges = edges + res[1]
        elif isinstance(self.root, Function):
            for value in self.root.param:
                edges = edges + "\n" + self.root.getId() + "--" + value.getId()
                nodes = nodes + "\n" + value.getId() + " [label=" + value.getLabel() + "]"
        elif isinstance(self.root, Array):
            for node in self.root.arrayContent:
                edges = edges + "\n" + self.root.getId() + "--" + node.getId()
                nodes = nodes + "\n" + node.getId() + " [label=" + node.getLabel() + "]"

        return nodes, edges

    def foldTree(self, to_llvm=None):
        """
        This function tries to reduce the size of the tree as much as possible
         tree, self.g_assignment
        """
        temp = None
        if not (isinstance(self.root, Value) or isinstance(self.root, Array) or isinstance(self.root, Include)):
            temp = self.root.fold(to_llvm)
            self.root = temp[0]
            return self, temp[1]
        return self, True

    def getVariables(self, fill: bool = True):
        return self.root.getVariables(fill)

    def replaceVariables(self, values):
        self.root.replaceVariables(values)

    def createUnfilledDeclaration(self, root: AST_node):
        left = root.leftChild
        var = Value(left.value, left.type, left.line, None, left.variable, left.const, left.declaration)
        val = EmptyNode(left.line, None, left.type)
        dec = Declaration(var, root.line, None)
        dec.setRightChild(val)
        return dec

    def printTables(self, filePath):
        self.root.printTables(filePath)
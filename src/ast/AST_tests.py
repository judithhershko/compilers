import unittest
import AST
import node
import program
import block


class nodeTestCase(unittest.TestCase):
    def test_getId(self):
        testNode = node.AST_node()
        testNode.setLevel(12)
        testNode.setNumber(55)
        self.assertEqual(testNode.getId(), "12.55", "should be 12.55")

    def test_setNodeIds(self):
        ast1 = AST.AST()
        ast2 = AST.AST()

        # first ast
        add = node.BinaryOperator("+")

        mult = node.BinaryOperator("*")
        add.setLeftChild(mult)

        leaf1 = node.Value(5, node.LiteralType.NUM)
        mult.setLeftChild(leaf1)
        leaf2 = node.Value(22, node.LiteralType.NUM)
        mult.setRightChild(leaf2)

        neg = node.UnaryOperator("-")
        add.setRightChild(neg)

        leaf3 = node.Value(-79, node.LiteralType.NUM)
        neg.setChild(leaf3)

        ast1.setRoot(add)
        ast1.setNodeIds(ast1.root)

        # second ast
        add2 = node.BinaryOperator("+")
        add2.setLevel(0)
        add2.setNumber(0)

        mult2 = node.BinaryOperator("*")
        mult2.setLevel(1)
        mult2.setNumber(1)
        add2.setLeftChild(mult2)

        leaf4 = node.Value(5, node.LiteralType.NUM)
        leaf4.setLevel(2)
        leaf4.setNumber(2)
        mult2.setLeftChild(leaf4)

        leaf5 = node.Value(22, node.LiteralType.NUM)
        leaf5.setLevel(2)
        leaf5.setNumber(3)
        mult2.setRightChild(leaf5)

        neg2 = node.UnaryOperator("-")
        neg2.setLevel(1)
        neg2.setNumber(4)
        add2.setRightChild(neg2)

        leaf6 = node.Value(-79, node.LiteralType.NUM)
        leaf6.setLevel(2)
        leaf6.setNumber(5)
        neg2.setChild(leaf6)

        ast2.setRoot(add2)

        self.assertEqual(ast1, ast2, "both ASTs should be the same")

    def test_generateDot(self):
        ast = AST.AST()

        add = node.BinaryOperator("+")

        mult = node.BinaryOperator("*")
        add.setLeftChild(mult)

        leaf1 = node.Value(5, node.LiteralType.NUM)
        mult.setLeftChild(leaf1)

        leaf2 = node.Value(22, node.LiteralType.NUM)
        mult.setRightChild(leaf2)

        neg = node.UnaryOperator("-")
        add.setRightChild(neg)

        leaf3 = node.Value(-79, node.LiteralType.NUM)
        neg.setChild(leaf3)

        ast.setRoot(add)
        ast.setNodeIds(ast.root)

        dot = ast.generateDot("test_generateDot")
        expected = "graph ast {\n0.0 [label=\"Binary operator: +\"]\n1.1 [label=\"Binary operator: *\"]\n2.2 " \
                   "[label=\"Literal: 5\"]\n2.3 [label=\"Literal: 22\"]\n1.4 [label=\"Unary operator: -\"]\n2.5 " \
                   "[label=\"Literal: -79\"]\n\n0.0--1.1\n0.0--1.4\n1.1--2.2\n1.1--2.3\n1.4--2.5\n}"
        self.assertEqual(dot, expected)

    def test_fold(self):
        ast = AST.AST()

        div = node.BinaryOperator("/")

        add = node.BinaryOperator("+")
        div.setLeftChild(add)

        mult = node.BinaryOperator("*")
        add.setLeftChild(mult)

        leaf1 = node.Value(5, node.LiteralType.NUM)
        mult.setLeftChild(leaf1)

        leaf2 = node.Value(22, node.LiteralType.NUM)
        mult.setRightChild(leaf2)

        neg = node.UnaryOperator("-")
        add.setRightChild(neg)

        leaf3 = node.Value(-78, node.LiteralType.NUM)
        neg.setChild(leaf3)

        leaf4 = node.Value(2, node.LiteralType.NUM)
        div.setRightChild(leaf4)

        ast.setRoot(div)
        ast.setNodeIds(ast.root)

        ast.foldTree()
        ast.setNodeIds(ast.root)
        ast.generateDot("test_fold")

        res = node.Value(94, node.LiteralType.NUM)
        res.setLevel(0)
        res.setNumber(0)

        self.assertEqual(ast.root, res)

    def test_fillSymbolTable(self):
        prog = program.program()

        val = prog.getSymbolTable()
        a = val.addSymbol("x", 5, "int", False)
        b = val.addSymbol("y", 22, "int", True)
        c = val.addSymbol("z", -78, "int", False)
        d = val.addSymbol("x", 7, "int", False)
        e = val.addSymbol("y", 25, int, True)
        f = val.addSymbol("z", "abc", "str", False)

        self.assertEqual(a, "placed")
        self.assertEqual(b, "placed")
        self.assertEqual(c, "placed")
        self.assertEqual(d, "replaced")
        self.assertEqual(e, "const")
        self.assertEqual(f, "type")

        self.assertEqual(val.findSymbol("x"), 7)
        self.assertEqual(val.findSymbol("y"), 22)
        self.assertEqual(val.findSymbol("z"), -78)

    def test_fillLiterals(self):
        div = node.BinaryOperator("/")

        add = node.BinaryOperator("+")
        div.setLeftChild(add)

        mult = node.BinaryOperator("*")
        add.setLeftChild(mult)

        leaf1 = node.Value("x", node.LiteralType.VAR)
        mult.setLeftChild(leaf1)

        leaf2 = node.Value("y", node.LiteralType.VAR)
        mult.setRightChild(leaf2)

        neg = node.UnaryOperator("-")
        add.setRightChild(neg)

        leaf3 = node.Value("z", node.LiteralType.VAR)
        neg.setChild(leaf3)

        leaf4 = node.Value("w", node.LiteralType.VAR)
        div.setRightChild(leaf4)

        prog = program.program()
        prog.getAst().setRoot(div)
        prog.getAst().setNodeIds(prog.getAst().root)

        val = prog.getSymbolTable()
        val.addSymbol("x", 5, "int", False)
        val.addSymbol("y", 22, "int", False)
        val.addSymbol("z", -78, "int", False)
        val.addSymbol("w", 2, "int", False)

        prog.fillLiterals()
        prog.getAst().foldTree()
        prog.getAst().setNodeIds(prog.getAst().root)

        res = node.Value(94, node.LiteralType.NUM)
        res.setLevel(0)
        res.setNumber(0)

        self.assertEqual(prog.getAst().root, res)

    def test_fillLiteralsBlock(self):
        div = node.BinaryOperator("/")

        add = node.BinaryOperator("+")
        div.setLeftChild(add)

        mult = node.BinaryOperator("*")
        add.setLeftChild(mult)

        leaf1 = node.Value("x", node.LiteralType.VAR)
        mult.setLeftChild(leaf1)

        leaf2 = node.Value("y", node.LiteralType.VAR)
        mult.setRightChild(leaf2)

        neg = node.UnaryOperator("-")
        add.setRightChild(neg)

        leaf3 = node.Value("z", node.LiteralType.VAR)
        neg.setChild(leaf3)

        leaf4 = node.Value("w", node.LiteralType.VAR)
        div.setRightChild(leaf4)

        prog = program.program()
        scope = block.block(prog)
        scope.getAst().setRoot(div)
        scope.getAst().setNodeIds(scope.getAst().root)
        prog.addBlock(scope)

        val = prog.getSymbolTable()
        val.addSymbol("x", 5, "int", False)
        val.addSymbol("y", 22, "int", False)

        valBlock = scope.getSymbolTable()
        valBlock.addSymbol("z", -78, "int", False)
        valBlock.addSymbol("w", 2, "int", False)

        scope.fillLiterals()
        scope.getAst().foldTree()
        scope.getAst().setNodeIds(scope.getAst().root)

        res = node.Value(94, node.LiteralType.NUM)
        res.setLevel(0)
        res.setNumber(0)

        self.assertEqual(scope.getAst().root, res)

if __name__ == '__main__':
    unittest.main()

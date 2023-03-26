import unittest
from .AST import *
from .Program import program
from .block import *
from .node import *


# TODO: force input of functions to be of a certain type
# TODO: write documentation for function
# TODO: add more test for new functionality
# TODO: check based on input files if all exceptions are generated (correctly)
# TODO: check functionality for pointers
# TODO: catch generated errors in tests
# TODO: rewrite all tests

class nodeTestCase(unittest.TestCase):
    def test_getId(self):
        testNode = node.AST_node()
        testNode.setLevel(12)
        testNode.setNumber(55)
        self.assertEqual(testNode.getId(), "12.55", "should be 12.55")

    def test_setNodeIds(self):
        ast1 = AST()
        ast2 = AST()

        # first ast
        add = node.BinaryOperator("+", 1)

        mult = node.BinaryOperator("*", 1)
        add.setLeftChild(mult)

        leaf1 = node.Value(5, node.LiteralType.INT, 1, variable=False)
        mult.setLeftChild(leaf1)
        leaf2 = node.Value(22, node.LiteralType.INT, 1, variable=False)
        mult.setRightChild(leaf2)

        neg = node.UnaryOperator("-", 1)
        add.setRightChild(neg)

        leaf3 = node.Value(-79, node.LiteralType.INT, 1, variable=False)
        neg.setRightChild(leaf3)

        ast1.setRoot(add)
        ast1.setNodeIds(ast1.root)

        # second ast
        add2 = node.BinaryOperator("+", 1)
        add2.setLevel(0)
        add2.setNumber(0)

        mult2 = node.BinaryOperator("*", 1)
        mult2.setLevel(1)
        mult2.setNumber(1)
        add2.setLeftChild(mult2)

        leaf4 = node.Value(5, node.LiteralType.INT, 1, variable=False)
        leaf4.setLevel(2)
        leaf4.setNumber(2)
        mult2.setLeftChild(leaf4)

        leaf5 = node.Value(22, node.LiteralType.INT, 1, variable=False)
        leaf5.setLevel(2)
        leaf5.setNumber(3)
        mult2.setRightChild(leaf5)

        neg2 = node.UnaryOperator("-", 1)
        neg2.setLevel(1)
        neg2.setNumber(4)
        add2.setRightChild(neg2)

        leaf6 = node.Value(-79, node.LiteralType.INT, 1, variable=False)
        leaf6.setLevel(2)
        leaf6.setNumber(5)
        neg2.setRightChild(leaf6)

        ast2.setRoot(add2)

        self.assertEqual(ast1, ast2, "both ASTs should be the same")

    def test_generateDot(self):
        ast = AST()

        add = node.BinaryOperator("+", 1)

        mult = node.BinaryOperator("*", 1)
        add.setLeftChild(mult)

        leaf1 = node.Value(5, node.LiteralType.INT, 1, variable=False)
        mult.setLeftChild(leaf1)

        leaf2 = node.Value(22, node.LiteralType.INT, 1, variable=False)
        mult.setRightChild(leaf2)

        neg = node.UnaryOperator("-", 1)
        add.setRightChild(neg)

        leaf3 = node.Value(-79, node.LiteralType.INT, 1, variable=False)
        neg.setRightChild(leaf3)

        ast.setRoot(add)
        ast.setNodeIds(ast.root)

        dot = ast.generateDot("test_generateDot")
        expected = "graph ast {\n0.0 [label=\"Binary operator: +\"]\n1.1 [label=\"Binary operator: *\"]\n2.2 " \
                   "[label=\"Literal: 5\"]\n2.3 [label=\"Literal: 22\"]\n1.4 [label=\"Unary operator: -\"]\n2.5 " \
                   "[label=\"Literal: -79\"]\n\n0.0--1.1\n0.0--1.4\n1.1--2.2\n1.1--2.3\n1.4--2.5\n}"
        self.assertEqual(dot, expected)

    def test_fold(self):
        ast = AST()

        div = node.BinaryOperator("/", 1)

        add = node.BinaryOperator("+", 1)
        div.setLeftChild(add)

        mult = node.BinaryOperator("*", 1)
        add.setLeftChild(mult)

        leaf1 = node.Value(5, node.LiteralType.INT, 1, variable=False)
        mult.setLeftChild(leaf1)

        leaf2 = node.Value(22, node.LiteralType.INT, 1, variable=False)
        mult.setRightChild(leaf2)

        neg = node.UnaryOperator("-", 1)
        add.setRightChild(neg)

        leaf3 = node.Value(-78, node.LiteralType.INT, 1, variable=False)
        neg.setRightChild(leaf3)

        leaf4 = node.Value(2, node.LiteralType.INT, 1, variable=True)
        div.setRightChild(leaf4)

        ast.setRoot(div)
        ast.setNodeIds(ast.root)

        ast.foldTree()
        ast.setNodeIds(ast.root)
        ast.generateDot("test_fold")

        res = node.Value("94", node.LiteralType.INT, 1, variable=False)
        res.setLevel(0)
        res.setNumber(0)

        self.assertEqual(ast.root, res)

    def test_fillSymbolTable(self):
        prog = Program.program()

        val = prog.getSymbolTable()
        # First element
        var1 = Value("x", LiteralType.INT, 1, None, True, False, True)
        val1 = Value("5", LiteralType.INT, 1, None, False, False, True)
        dec1 = Declaration(var1, 1)
        dec1.setRightChild(val1)
        a = val.addSymbol(dec1, True)
        # Second element
        var2 = Value("y", LiteralType.INT, 1, None, True, True, True)
        val2 = Value("22", LiteralType.INT, 1, None, False, True, True)
        dec2 = Declaration(var2, 1)
        dec2.setRightChild(val2)
        b = val.addSymbol(dec2, False)
        # Third element
        var3 = Value("z", LiteralType.INT, 1, None, True, False, True)
        val3 = Value("-78", LiteralType.INT, 1, None, False, False, True)
        dec3 = Declaration(var3, 1)
        dec3.setRightChild(val3)
        c = val.addSymbol(dec3, False)
        # resubmit first
        var4 = Value("x", LiteralType.INT, 1, None, True, True, False)
        val4 = Value("6", LiteralType.INT, 1, None, False, True, False)
        dec4 = Declaration(var4, 1)
        dec4.setRightChild(val4)
        with self.assertRaises(Exception) as except1:
            val.addSymbol(dec4, True)
        # resubmit second
        var5 = Value("y", LiteralType.INT, 1, None, True, False, False)
        val5 = Value("23", LiteralType.INT, 1, None, False, False, False)
        dec5 = Declaration(var5, 1)
        dec5.setRightChild(val5)
        with self.assertRaises(Exception) as except2:
            val.addSymbol(dec5, False)
        # resubmit third
        var6 = Value("z", LiteralType.INT, 1, None, True, False, True)
        val6 = Value("-79", LiteralType.INT, 1, None, False, False, True)
        dec6 = Declaration(var6, 1)
        dec6.setRightChild(val6)
        with self.assertRaises(Exception) as except3:
            val.addSymbol(dec3, False)
        # resubmit third (no decl)
        var7 = Value("z", LiteralType.INT, 1, None, True, False, False)
        val7 = Value("-79", LiteralType.INT, 1, None, False, False, False)
        dec7 = Declaration(var7, 1)
        dec7.setRightChild(val7)
        d = val.addSymbol(dec7, False)
        # resubmit third (wrong type)
        var8 = Value("z", LiteralType.FLOAT, 1, None, True, False, False)
        val8 = Value("-80", LiteralType.FLOAT, 1, None, False, False, False)
        dec8 = Declaration(var8, 1)
        dec8.setRightChild(val8)
        with self.assertRaises(Exception) as except4:
            val.addSymbol(dec8, False)
        # not defined yet
        var9 = Value("s", LiteralType.FLOAT, 1, None, True, False, False)
        val9 = Value("-80.2", LiteralType.FLOAT, 1, None, False, False, False)
        dec9 = Declaration(var9, 1)
        dec9.setRightChild(val9)
        with self.assertRaises(Exception) as except5:
            val.addSymbol(dec9, False)

        self.assertEqual(a, "placed")
        self.assertEqual(b, "placed")
        self.assertEqual(c, "placed")
        self.assertEqual(d, "replaced")

        self.assertEqual(val.findSymbol("x", 1), ("5", LiteralType.INT))
        self.assertEqual(val.findSymbol("y", 1), ("22", LiteralType.INT))
        self.assertEqual(val.findSymbol("z", 1), ("-79", LiteralType.INT))

        self.assertEqual("\n\tError in line 1: there is a reassignment of the global variable x",
                         str(except1.exception))
        self.assertEqual("\n\tError in line 1: there is a reassignment of the const variable y", str(except2.exception))
        self.assertEqual("\n\tError in line 1: there is a redeclaration of the variable z", str(except3.exception))
        self.assertEqual("\n\tError in line 1: z has type INT and does not support variables of type FLOAT",
                         str(except4.exception))
        self.assertEqual("\n\tError in line 1: s has not been declared yet", str(except5.exception))

    def test_fillLiterals(self):
        div = node.BinaryOperator("/", 1)

        add = node.BinaryOperator("+", 1)
        div.setLeftChild(add)

        mult = node.BinaryOperator("*", 1)
        add.setLeftChild(mult)

        leaf1 = node.Value("x", node.LiteralType.STR, 1, variable=True)
        mult.setLeftChild(leaf1)

        leaf2 = node.Value("y", node.LiteralType.INT, 1, variable=True)
        mult.setRightChild(leaf2)

        neg = node.UnaryOperator("-", 1)
        add.setRightChild(neg)

        leaf3 = node.Value("z", node.LiteralType.FLOAT, 1, variable=True)
        neg.setRightChild(leaf3)

        leaf4 = node.Value("w", node.LiteralType.INT, 1, variable=True)
        div.setRightChild(leaf4)

        prog = Program.program()
        prog.getAst().setRoot(div)
        prog.getAst().setNodeIds(prog.getAst().root)

        val = prog.getSymbolTable()
        # First element
        var1 = Value("x", LiteralType.STR, 1, None, True, False, True)
        val1 = Value("5", LiteralType.STR, 1, None, False, False, True)
        dec1 = Declaration(var1, 1)
        dec1.setRightChild(val1)
        val.addSymbol(dec1, True)
        # Second element
        var2 = Value("y", LiteralType.INT, 1, None, True, False, True)
        val2 = Value("22", LiteralType.INT, 1, None, False, False, True)
        dec2 = Declaration(var2, 1)
        dec2.setRightChild(val2)
        val.addSymbol(dec2, True)
        # Third element
        var3 = Value("z", LiteralType.FLOAT, 1, None, True, False, True)
        val3 = Value("-78.0", LiteralType.FLOAT, 1, None, False, False, True)
        dec3 = Declaration(var3, 1)
        dec3.setRightChild(val3)
        val.addSymbol(dec3, True)
        # resubmit first
        var4 = Value("w", LiteralType.INT, 1, None, True, True, True)
        val4 = Value("2", LiteralType.INT, 1, None, False, True, True)
        dec4 = Declaration(var4, 1)
        dec4.setRightChild(val4)
        val.addSymbol(dec4, True)

        prog.fillLiterals(prog.getAst())
        with self.assertRaises(Exception) as excep:
            prog.getAst().foldTree()
        self.assertEqual("\n\tError in line 1: the binary operator * can not be executed on a STR and a INT",
                         str(excep.exception))
        #prog.getAst().setNodeIds(prog.getAst().root)

        leaf5 = node.Value("y", node.LiteralType.INT, 1, variable=True)
        mult.setLeftChild(leaf5)
        prog.getAst().setNodeIds(prog.getAst().root)
        prog.fillLiterals(prog.getAst())
        prog.getAst().foldTree()

        res = node.Value("281.0", node.LiteralType.FLOAT, 1, variable=False)
        # res.setLevel(0)
        # res.setNumber(0)

        self.assertEqual(prog.getAst().root, res)

    def test_fillLiteralsBlock(self):
        div = node.BinaryOperator("/", 1)

        add = node.BinaryOperator("+", 1)
        div.setLeftChild(add)

        mult = node.BinaryOperator("*", 1)
        add.setLeftChild(mult)

        leaf1 = node.Value("x", node.LiteralType.INT, 1, variable=True)
        mult.setLeftChild(leaf1)

        leaf2 = node.Value("y", node.LiteralType.DOUBLE, 1, variable=True)
        mult.setRightChild(leaf2)

        neg = node.UnaryOperator("-", 1)
        add.setRightChild(neg)

        leaf3 = node.Value("z", node.LiteralType.FLOAT, 1, variable=True)
        neg.setRightChild(leaf3)

        leaf4 = node.Value("w", node.LiteralType.INT, 1, variable=True)
        div.setRightChild(leaf4)

        prog = Program.program()
        scope = block(prog)
        scope.getAst().setRoot(div)
        scope.getAst().setNodeIds(scope.getAst().root)
        prog.addBlock(scope)

        # First element
        var1 = Value("x", LiteralType.INT, 1, None, True, False, True)
        val1 = Value("5", LiteralType.INT, 1, None, False, False, True)
        dec1 = Declaration(var1, 1)
        dec1.setRightChild(val1)
        # Second element
        var2 = Value("y", LiteralType.INT, 1, None, True, False, True)
        val2 = Value("22", LiteralType.INT, 1, None, False, False, True)
        dec2 = Declaration(var2, 1)
        dec2.setRightChild(val2)
        # Third element
        var3 = Value("z", LiteralType.FLOAT, 1, None, True, False, True)
        val3 = Value("-78.0", LiteralType.FLOAT, 1, None, False, False, True)
        dec3 = Declaration(var3, 1)
        dec3.setRightChild(val3)
        # resubmit first
        var4 = Value("w", LiteralType.INT, 1, None, True, True, True)
        val4 = Value("2", LiteralType.INT, 1, None, False, True, True)
        dec4 = Declaration(var4, 1)
        dec4.setRightChild(val4)

        val = prog.getSymbolTable()
        val.addSymbol(dec1, True)
        val.addSymbol(dec2, True)

        valBlock = scope.getSymbolTable()
        valBlock.addSymbol(dec3, False)
        valBlock.addSymbol(dec4, False)

        scope.fillLiterals(scope.getAst())
        scope.getAst().foldTree()
        scope.getAst().setNodeIds(scope.getAst().root)

        res = node.Value("94.0", node.LiteralType.FLOAT, 1, variable=False)
        res.setLevel(0)
        res.setNumber(0)

        self.assertEqual(scope.getAst().root, res)

    def test_toDotDeclaration(self):
        var = node.Value("x", node.LiteralType.DOUBLE, 1, variable=True)
        dec = node.Declaration(var, 1)
        var.parent = dec

        mul = node.BinaryOperator("*", 1, parent=dec)
        dec.setRightChild(mul)

        leaf1 = node.Value(5, node.LiteralType.INT, 1, parent=mul, variable=False)
        mul.setLeftChild(leaf1)

        leaf2 = node.Value(3, node.LiteralType.INT, 1, parent=mul, variable=False)
        mul.setRightChild(leaf2)

        ast = AST()
        ast.setRoot(dec)
        ast.setNodeIds(ast.root)
        dot = ast.generateDot("Declaration")
        exp = "graph ast {\n0.0 [label=\"Declaration: =\"]\n1.1 [label=\"Literal: x\"]\n1.2 [label=" \
              "\"Binary operator: *\"]\n2.3 [label=\"Literal: 5\"]\n2.4 [label=\"Literal: 3\"]\n\n0.0--1.1\n0.0--1.2" \
              "\n1.2--2.3\n1.2--2.4\n}"
        self.assertEqual(dot, exp)
        ast.foldTree()
        ast.setNodeIds(ast.root)
        dot = ast.generateDot("DeclarationFolded")
        exp = "graph ast {\n0.0 [label=\"Declaration: =\"]\n1.1 [label=\"Literal: x\"]\n1.2 [label=" \
              "\"Literal: 15\"]\n\n0.0--1.1\n0.0--1.2\n}"
        self.assertEqual(dot, exp)


if __name__ == '__main__': # TODO: this can't be run?! -> run: class nodeTestCase(unittest.TestCase):
    unittest.main()

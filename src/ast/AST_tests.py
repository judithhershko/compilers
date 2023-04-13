import unittest
from .node import *
from .Program import program
from .block import block
from .AST import AST


# TODO: force input of functions to be of a certain type
# TODO: write documentation for function


def generateDiv():
    div = BinaryOperator("/", 1)

    add = BinaryOperator("+", 1)
    div.setLeftChild(add)

    mult = BinaryOperator("*", 1)
    add.setLeftChild(mult)

    leaf1 = Value("x", LiteralType.STR, 1, variable=True)
    mult.setLeftChild(leaf1)

    leaf2 = Value("y", LiteralType.INT, 1, variable=True)
    mult.setRightChild(leaf2)

    neg = UnaryOperator("-", 1)
    add.setRightChild(neg)

    leaf3 = Value("z", LiteralType.FLOAT, 1, variable=True)
    neg.setRightChild(leaf3)

    leaf4 = Value("w", LiteralType.INT, 1, variable=True)
    div.setRightChild(leaf4)

    return div


def generateCondition():
    And = LogicalOperator("&&", parent=None, line=1)
    gt = LogicalOperator(">", parent=None, line=1)
    leaf1 = Value("y", LiteralType.FLOAT, 1, variable=True)
    leaf2 = Value("x", LiteralType.FLOAT, 1, variable=True)
    gt.setLeftChild(leaf1)
    gt.setRightChild(leaf2)
    And.setLeftChild(gt)
    Or = LogicalOperator("||", parent=None, line=1)
    lt = LogicalOperator("<", parent=None, line=1)
    leaf3 = Value("x", LiteralType.FLOAT, 1, variable=True)
    leaf4 = Value("y", LiteralType.FLOAT, 1, variable=True)
    lt.setLeftChild(leaf3)
    lt.setRightChild(leaf4)
    Or.setLeftChild(lt)
    eq = LogicalOperator("==", parent=None, line=1)
    leaf5 = Value("z", LiteralType.FLOAT, 1, variable=True)
    leaf6 = Value("z", LiteralType.FLOAT, 1, variable=True)

    eq.setLeftChild(leaf5)
    eq.setRightChild(leaf6)
    Or.setRightChild(eq)
    And.setRightChild(Or)

    return And



class nodeTestCase(unittest.TestCase):
    def test_getId(self):
        testNode = AST_node()
        testNode.setLevel(12)
        testNode.setNumber(55)
        self.assertEqual(testNode.getId(), "12.55", "should be 12.55")

    def test_setNodeIds(self):
        ast1 = AST()
        ast2 = AST()

        # first ast
        add = BinaryOperator("+", 1)

        mult = BinaryOperator("*", 1)
        add.setLeftChild(mult)

        leaf1 = Value(5, LiteralType.INT, 1, variable=False)
        mult.setLeftChild(leaf1)
        leaf2 = Value(22, LiteralType.INT, 1, variable=False)
        mult.setRightChild(leaf2)

        neg = UnaryOperator("-", 1)
        add.setRightChild(neg)

        leaf3 = Value(-79, LiteralType.INT, 1, variable=False)
        neg.setRightChild(leaf3)

        ast1.setRoot(add)
        ast1.setNodeIds(ast1.root)

        # second ast
        add2 = BinaryOperator("+", 1)
        add2.setLevel(0)
        add2.setNumber(0)

        mult2 = BinaryOperator("*", 1)
        mult2.setLevel(1)
        mult2.setNumber(1)
        add2.setLeftChild(mult2)

        leaf4 = Value(5, LiteralType.INT, 1, variable=False)
        leaf4.setLevel(2)
        leaf4.setNumber(2)
        mult2.setLeftChild(leaf4)

        leaf5 = Value(22, LiteralType.INT, 1, variable=False)
        leaf5.setLevel(2)
        leaf5.setNumber(3)
        mult2.setRightChild(leaf5)

        neg2 = UnaryOperator("-", 1)
        neg2.setLevel(1)
        neg2.setNumber(4)
        add2.setRightChild(neg2)

        leaf6 = Value(-79, LiteralType.INT, 1, variable=False)
        leaf6.setLevel(2)
        leaf6.setNumber(5)
        neg2.setRightChild(leaf6)

        ast2.setRoot(add2)

        self.assertEqual(ast1, ast2, "both ASTs should be the same")

    def test_generateDot(self):
        ast = AST()

        add = BinaryOperator("+", 1)

        mult = BinaryOperator("*", 1)
        add.setLeftChild(mult)

        leaf1 = Value(5, LiteralType.INT, 1, variable=False)
        mult.setLeftChild(leaf1)

        leaf2 = Value(22, LiteralType.INT, 1, variable=False)
        mult.setRightChild(leaf2)

        neg = UnaryOperator("-", 1)
        add.setRightChild(neg)

        leaf3 = Value(-79, LiteralType.INT, 1, variable=False)
        neg.setRightChild(leaf3)

        ast.setRoot(add)
        ast.setNodeIds(ast.root)

        dot = ast.generateDot("./src/ast/dotFiles/test_generateDot.dot")
        expected = "graph ast {\n0.0 [label=\"Binary operator: +\"]\n1.1 [label=\"Binary operator: *\"]\n2.2 " \
                   "[label=\"Literal: 5\"]\n2.3 [label=\"Literal: 22\"]\n1.4 [label=\"Unary operator: -\"]\n2.5 " \
                   "[label=\"Literal: -79\"]\n\n0.0--1.1\n0.0--1.4\n1.1--2.2\n1.1--2.3\n1.4--2.5\n}"
        self.assertEqual(dot, expected)

    def test_fold(self):
        ast = AST()

        div = BinaryOperator("/", 1)

        add = BinaryOperator("+", 1)
        div.setLeftChild(add)

        mult = BinaryOperator("*", 1)
        add.setLeftChild(mult)

        leaf1 = Value(5, LiteralType.INT, 1, variable=False)
        mult.setLeftChild(leaf1)

        leaf2 = Value(22, LiteralType.INT, 1, variable=False)
        mult.setRightChild(leaf2)

        neg = UnaryOperator("-", 1)
        add.setRightChild(neg)

        leaf3 = Value(-78, LiteralType.INT, 1, variable=False)
        neg.setRightChild(leaf3)

        leaf4 = Value(2, LiteralType.INT, 1, variable=True)
        div.setRightChild(leaf4)

        ast.setRoot(div)
        ast.setNodeIds(ast.root)

        ast.foldTree()
        ast.setNodeIds(ast.root)
        ast.generateDot("./src/ast/dotFiles/test_fold.dot")

        res = Value("94", LiteralType.INT, 1, variable=False)
        res.setLevel(0)
        res.setNumber(0)

        self.assertEqual(ast.root, res)

    def test_fillSymbolTable(self):
        prog = program()

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

        self.assertEqual(val.findSymbol("x"), ("5", LiteralType.INT, 0))
        self.assertEqual(val.findSymbol("y"), ("22", LiteralType.INT, 0))
        self.assertEqual(val.findSymbol("z"), ("-79", LiteralType.INT, 0))

        self.assertEqual("\n\tError in line 1: there is a reassignment of the global variable x",
                         str(except1.exception))
        self.assertEqual("\n\tError in line 1: there is a reassignment of the const variable y", str(except2.exception))
        self.assertEqual("\n\tError in line 1: there is a redeclaration of the variable z", str(except3.exception))
        self.assertEqual("\n\tError in line 1: z has type INT and does not support variables of type FLOAT",
                         str(except4.exception))
        self.assertEqual("\n\tError in line 1: s has not been declared yet", str(except5.exception))

    def test_fillLiterals(self):
        div = BinaryOperator("/", 1)

        add = BinaryOperator("+", 1)
        div.setLeftChild(add)

        mult = BinaryOperator("*", 1)
        add.setLeftChild(mult)

        leaf1 = Value("x", LiteralType.STR, 1, variable=True)
        mult.setLeftChild(leaf1)

        leaf2 = Value("y", LiteralType.INT, 1, variable=True)
        mult.setRightChild(leaf2)

        neg = UnaryOperator("-", 1)
        add.setRightChild(neg)

        leaf3 = Value("z", LiteralType.FLOAT, 1, variable=True)
        neg.setRightChild(leaf3)

        leaf4 = Value("w", LiteralType.INT, 1, variable=True)
        div.setRightChild(leaf4)

        prog = program()
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
        # prog.getAst().setNodeIds(prog.getAst().root)

        leaf5 = Value("y", LiteralType.INT, 1, variable=True)
        mult.setLeftChild(leaf5)
        prog.getAst().setNodeIds(prog.getAst().root)
        prog.fillLiterals(prog.getAst())
        prog.getAst().foldTree()

        res = Value("281.0", LiteralType.FLOAT, 1, variable=False)

        self.assertEqual(prog.getAst().root, res)

    def test_fillLiteralsBlock(self):
        div = BinaryOperator("/", 1)

        add = BinaryOperator("+", 1)
        div.setLeftChild(add)

        mult = BinaryOperator("*", 1)
        add.setLeftChild(mult)

        leaf1 = Value("x", LiteralType.INT, 1, variable=True)
        mult.setLeftChild(leaf1)

        leaf2 = Value("y", LiteralType.DOUBLE, 1, variable=True)
        mult.setRightChild(leaf2)

        neg = UnaryOperator("-", 1)
        add.setRightChild(neg)

        leaf3 = Value("z", LiteralType.FLOAT, 1, variable=True)
        neg.setRightChild(leaf3)

        leaf4 = Value("w", LiteralType.INT, 1, variable=True)
        div.setRightChild(leaf4)

        prog = program()
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

        res = Value("94.0", LiteralType.FLOAT, 1, variable=False)
        res.setLevel(0)
        res.setNumber(0)

        self.assertEqual(scope.getAst().root, res)

    def test_toDotDeclaration(self):
        var = Value("x", LiteralType.DOUBLE, 1, variable=True)
        dec = Declaration(var, 1)
        var.parent = dec

        mul = BinaryOperator("*", 1, parent=dec)
        dec.setRightChild(mul)

        leaf1 = Value(5, LiteralType.INT, 1, parent=mul, variable=False)
        mul.setLeftChild(leaf1)

        leaf2 = Value(3, LiteralType.INT, 1, parent=mul, variable=False)
        mul.setRightChild(leaf2)

        ast = AST()
        ast.setRoot(dec)
        ast.setNodeIds(ast.root)
        dot = ast.generateDot("./src/ast/dotFiles/Declaration.dot")
        exp = "graph ast {\n0.0 [label=\"Declaration: =\"]\n1.1 [label=\"Literal: x\"]\n1.2 [label=" \
              "\"Binary operator: *\"]\n2.3 [label=\"Literal: 5\"]\n2.4 [label=\"Literal: 3\"]\n\n0.0--1.1\n0.0--1.2" \
              "\n1.2--2.3\n1.2--2.4\n}"
        self.assertEqual(dot, exp)
        ast.foldTree()
        ast.setNodeIds(ast.root)
        dot = ast.generateDot("./src/ast/dotFiles/DeclarationFolded.dot")
        exp = "graph ast {\n0.0 [label=\"Declaration: =\"]\n1.1 [label=\"Literal: x\"]\n1.2 [label=" \
              "\"Literal: 15\"]\n\n0.0--1.1\n0.0--1.2\n}"
        self.assertEqual(dot, exp)

    def test_Scope(self):
        div1 = generateDiv()
        div2 = generateDiv()
        div3 = generateDiv()
        div4 = generateDiv()
        div5 = generateDiv()

        scope1 = Scope(1)
        scope2 = Scope(2)

        scope1.addTree(div1)
        scope1.addTree(div2)
        scope2.addTree(div3)
        scope2.addTree(div4)
        scope2.addTree(div5)
        scope1.addTree(scope2)

        prog = program()
        prog.getAst().setRoot(scope1)
        prog.getAst().setNodeIds(prog.getAst().root)
        prog.getAst().generateDot("./src/ast/dotFiles/scope_unfilled.dot")
        val = prog.getSymbolTable()
        # First element
        var1 = Value("x", LiteralType.INT, 1, None, True, False, True)
        val1 = Value("5", LiteralType.INT, 1, None, False, False, True)
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
        prog.getAst().generateDot("./src/ast/dotFiles/scope_unfolded.dot")

        prog.getAst().foldTree()
        prog.getAst().setNodeIds(prog.getAst().root)
        prog.getAst().generateDot("./src/ast/dotFiles/scope_folded.dot")

        expected = Scope(1)
        temp = Scope(2)
        expected.addTree(Value("94.0", LiteralType.FLOAT, 1))
        expected.addTree(Value("94.0", LiteralType.FLOAT, 1))
        temp.addTree(Value("94.0", LiteralType.FLOAT, 1))
        temp.addTree(Value("94.0", LiteralType.FLOAT, 1))
        temp.addTree(Value("94.0", LiteralType.FLOAT, 1))
        expected.addTree(temp)

        tree = AST()
        tree.setRoot(expected)
        tree.setNodeIds(tree.root)

        self.assertEqual(prog.getAst(), tree)

    def test_If(self):
        And = generateCondition()
        And2 = generateCondition()

        firstBlock = block(None)

        ifStat = If(1)
        ifStat.setCondition(And)
        ifTree = AST()
        ifTree.root = ifStat

        elifStat = If(2, ConditionType.ELIF)
        elifStat.setCondition(And2)
        elifTree = AST()
        elifTree.root = elifStat

        elseStat = If(3, ConditionType.ELSE)
        elseTree = AST()
        elseTree.root = elseStat

        div1 = generateDiv()
        tree1 = AST()
        tree1.setRoot(div1)

        div2 = generateDiv()
        tree2 = AST()
        tree2.setRoot(div2)
        ifBlock = block(firstBlock)
        ifBlock.addTree(tree2)
        # First element
        ifvar1 = Value("x", LiteralType.INT, 1, None, True, False, True)
        ifval1 = Value("1", LiteralType.INT, 1, None, False, False, True)
        ifdec1 = Declaration(ifvar1, 1)
        ifdec1.setRightChild(ifval1)
        ifBlock.getSymbolTable().addSymbol(ifdec1, True)
        # Second element
        ifvar2 = Value("y", LiteralType.INT, 1, None, True, False, True)
        ifval2 = Value("2", LiteralType.INT, 1, None, False, False, True)
        ifdec2 = Declaration(ifvar2, 1)
        ifdec2.setRightChild(ifval2)
        ifBlock.getSymbolTable().addSymbol(ifdec2, True)
        # Third element
        ifvar3 = Value("z", LiteralType.FLOAT, 1, None, True, False, True)
        ifval3 = Value("3", LiteralType.FLOAT, 1, None, False, False, True)
        ifdec3 = Declaration(ifvar3, 1)
        ifdec3.setRightChild(ifval3)
        ifBlock.getSymbolTable().addSymbol(ifdec3, True)
        # Fourth first
        ifvar4 = Value("w", LiteralType.INT, 1, None, True, True, True)
        ifval4 = Value("4", LiteralType.INT, 1, None, False, True, True)
        ifdec4 = Declaration(ifvar4, 1)
        ifdec4.setRightChild(ifval4)
        ifBlock.getSymbolTable().addSymbol(ifdec4, True)

        ifStat.setBlock(ifBlock)

        div3 = generateDiv()
        tree3 = AST()
        tree3.setRoot(div3)
        elifBlock = block(firstBlock)
        elifBlock.addTree(tree3)

        # First element
        elifvar1 = Value("x", LiteralType.INT, 1, None, True, False, True)
        elifval1 = Value("8", LiteralType.INT, 1, None, False, False, True)
        elifdec1 = Declaration(elifvar1, 1)
        elifdec1.setRightChild(elifval1)
        elifBlock.getSymbolTable().addSymbol(elifdec1, True)
        # Second element
        elifvar2 = Value("y", LiteralType.INT, 1, None, True, False, True)
        elifval2 = Value("9", LiteralType.INT, 1, None, False, False, True)
        elifdec2 = Declaration(elifvar2, 1)
        elifdec2.setRightChild(elifval2)
        elifBlock.getSymbolTable().addSymbol(elifdec2, True)

        elifStat.setBlock(elifBlock)

        div4 = generateDiv()
        tree4 = AST()
        tree4.setRoot(div4)
        elseBlock = block(firstBlock)
        elseBlock.addTree(tree4)
        elseStat.setBlock(elseBlock)

        prog = program()
        firstBlock.addTree(tree1)
        firstBlock.addTree(ifTree)
        firstBlock.addTree(elifTree)
        firstBlock.addTree(elseTree)

        # First element
        var1 = Value("x", LiteralType.INT, 1, None, True, False, True)
        val1 = Value("5", LiteralType.INT, 1, None, False, False, True)
        dec1 = Declaration(var1, 1)
        dec1.setRightChild(val1)
        firstBlock.getSymbolTable().addSymbol(dec1, True)
        # Second element
        var2 = Value("y", LiteralType.INT, 1, None, True, False, True)
        val2 = Value("22", LiteralType.INT, 1, None, False, False, True)
        dec2 = Declaration(var2, 1)
        dec2.setRightChild(val2)
        firstBlock.getSymbolTable().addSymbol(dec2, True)
        # Third element
        var3 = Value("z", LiteralType.FLOAT, 1, None, True, False, True)
        val3 = Value("-78.0", LiteralType.FLOAT, 1, None, False, False, True)
        dec3 = Declaration(var3, 1)
        dec3.setRightChild(val3)
        firstBlock.getSymbolTable().addSymbol(dec3, True)
        # Fourth element
        var4 = Value("w", LiteralType.INT, 1, None, True, True, True)
        val4 = Value("2", LiteralType.INT, 1, None, False, True, True)
        dec4 = Declaration(var4, 1)
        dec4.setRightChild(val4)
        firstBlock.getSymbolTable().addSymbol(dec4, True)

        prog.addBlock(firstBlock)
        prog.blocks[0].setNodeIds()
        prog.blocks[0].generateDot("./src/ast/dotFiles/if_unfilled.dot")
        prog.blocks[0].fillBlock()
        prog.blocks[0].generateDot("./src/ast/dotFiles/if_unfolded.dot")
        prog.blocks[0].fold()
        prog.blocks[0].setNodeIds()
        prog.blocks[0].generateDot("./src/ast/dotFiles/if_folded.dot")

        expected = block(None)
        expected.getSymbolTable().addSymbol(dec1, True)
        expected.getSymbolTable().addSymbol(dec2, True)
        expected.getSymbolTable().addSymbol(dec3, True)
        expected.getSymbolTable().addSymbol(dec4, True)

        # tree
        ast1 = AST()
        leaf1 = Value("94.0", LiteralType.FLOAT, 1)
        ast1.setRoot(leaf1)
        # if
        ifast = If(1)
        con1 = Value(True, LiteralType.BOOL, 1)
        ast2 = AST()
        leaf2 = Value("-0.25", LiteralType.FLOAT, 1)
        ast2.setRoot(leaf2)
        ifast.setCondition(con1)
        block1 = block(expected)
        block1.addTree(ast2)
        block1.getSymbolTable().addSymbol(ifdec1, True)
        block1.getSymbolTable().addSymbol(ifdec2, True)
        block1.getSymbolTable().addSymbol(ifdec3, True)
        block1.getSymbolTable().addSymbol(ifdec4, True)
        ifast.setBlock(block1)

        IF = AST()
        IF.setRoot(ifast)

        # elif
        elifast = If(2, ConditionType.ELIF)
        con2 = Value(True, LiteralType.BOOL, 1)
        ast3 = AST()
        leaf3 = Value("75.0", LiteralType.FLOAT, 1)
        ast3.setRoot(leaf3)
        elifast.setCondition(con2)
        block2 = block(expected)
        block2.addTree(ast3)
        block2.getSymbolTable().addSymbol(elifdec1, True)
        block2.getSymbolTable().addSymbol(elifdec2, True)
        elifast.setBlock(block2)

        ELIF = AST()
        ELIF.setRoot(elifast)
        # else
        elseast = If(3, ConditionType.ELSE)
        ast4 = AST()
        leaf4 = Value("94.0", LiteralType.FLOAT, 1)
        ast4.setRoot(leaf4)
        block3 = block(expected)
        block3.addTree(ast4)
        elseast.setBlock(block3)

        ELSE = AST()
        ELSE.setRoot(elseast)

        expected.addTree(ast1)
        expected.addTree(IF)
        expected.addTree(ELIF)
        expected.addTree(ELSE)

        expected.setNodeIds()

        self.assertEqual(prog.blocks[0], expected)


if __name__ == '__main__':
    unittest.main()

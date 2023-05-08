import unittest
from src.CustomListener import *
from src.LLVM.LLVM_Operators import ToLLVM
from src.CustomErrorListener import *
from generated.input.ExpressionLexer import ExpressionLexer
from generated.input.ExpressionParser import ExpressionParser
from src.MIPS.Mips import Mips


def testFile(fileName):
    argv = "../test_Mips/input/" + fileName + ".c"
    input_stream = FileStream(argv)
    lexer = ExpressionLexer(input_stream)
    MyError = CustomError()
    lexer.removeErrorListeners()
    lexer.addErrorListener(MyError)
    stream = CommonTokenStream(lexer)
    parser = ExpressionParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(MyError)
    tree = parser.start_rule()

    printer = CustomListener("")
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    printer.get_program("../test_Mips/dot_output/" + fileName + ".dot")
    printer.program.printTables("../test_Mips/symbolTables/" + fileName + "/")

    to_mips = Mips(printer.program)
    to_mips.transverse_program()
    to_mips.write_to_file("../test_Mips/Mips_output/" + fileName + ".asm")


class Mips_TestCases_Working(unittest.TestCase):
    # MANDITORY
    # ASSIGNEMT 1
    def filetest(self, filename):
        try:
            testFile(filename)
        except SystemExit:
            sys.exit()
        file1 = 'Mips_output/' + filename + '.asm'
        file2 = 'Mips_expected/' + filename + '.asm'
        with open(file1, 'r') as file:
            text1 = file.read().replace('\n', '')
        with open(file2, 'r') as file:
            text2 = file.read().replace('\n', '')
        self.assertTrue(text1 == text2)

    def test_binaryArithmeticOperators(self):
        # Binary arithmetic operators: +, -, *, /
        file = "M_P_BinaryArithmeticOperators"
        return self.filetest(file)

    def test_binaryComparatorOperators(self):
        # Binary arithmetic operators: +, -, *, /
        file = "M_P_BinaryComparatorOperators"
        return self.filetest(file)

    def test_unaryOperators(self):
        # Unary operators: +var, -var
        file = "M_P_UnaryOperators"
        return self.filetest(file)

    def test_ParaenthesisOrderOfOperations(self):
        file = "M_P_ParenthesisOrderOfOperations"
        return self.filetest(file)

    def test_LogicalOperators(self):
        # &&, ||, !var
        file = "M_P_LogicalOperators"
        return self.filetest(file)

    def test_IgnoringWhiteSpaces(self):
        file = "M_P_IgnoringWhiteSpaces"
        return self.filetest(file)

    def test_ConstantFolding(self):
        file = "M_P_ConstantFolding"
        return self.filetest(file)

    # SHOW USE OF AST
    # ASSIGNMENT 2
    def test_Types(self):
        # Types (float, char, int)
        file = "M_P_Types"
        return self.filetest(file)

    def test_Variables(self):
        file = "M_P_Variables"
        return self.filetest(file)

    def test_ConstantVariables(self):
        file = "M_P_ConstantVariables"
        return self.filetest(file)

    def test_Pointers(self):
        file = "M_P_Pointers"
        return self.filetest(file)

    def test_PointerOperations(self):
        file = "M_P_PointerOperations"
        return self.filetest(file)

    def test_constantPropagation(self):
        file = "M_P_ConstantPropagation"
        return self.filetest(file)

    # SHOW CONSTRUCTION + USE OF SYMBOLTABLE
    # ASSIGNEMT 3
    def test_SL_ML_Comment(self):
        file = "M_P_SL_ML_Comment"
        return self.filetest(file)

    # ASSIGNEMT 4
    def test_IfElse(self):
        file = "M_P_IfElse"
        return self.filetest(file)

    def test_WhileLoops(self):
        file = "M_P_WhileLoops"
        return self.filetest(file)

    def test_ForLoops(self):
        file = "M_P_ForLoops"
        return self.filetest(file)

    def test_Break(self):
        file = "M_P_Break"
        return self.filetest(file)

    def test_Continue(self):
        file = "M_P_Continue"
        return self.filetest(file)

    def test_AnonScope(self):
        file = "M_P_AnonScope"
        return self.filetest(file)

    # SHOW SYMBOLTABLE ANON SCOPE

    # ASSIGNEMT 5
    def test_functionScope(self):
        file = "M_P_functionScope"
        return self.filetest(file)

    # SHOW SYMBOLTABLE FUNCTION SCOPE
    def test_LocalGlobalVariables(self):
        file = "M_P_LocalGlobal"
        return self.filetest(file)

    def test_Functions(self):
        """
        ∗ Definition and declaration
        ∗ Calling
        ∗ Parameters (primitives and pointers, pass-by-value, pass-by-reference)
        ∗ Return values
        ∗ Functions with void return
        """
        file = "M_P_Functions"
        return self.filetest(file)

    def test_FowardDeclaration(self):
        file = "M_P_ForwardDeclaration"
        return self.filetest(file)

    def test_ReturnTypeChecking(self):
        file = "M_P_returnTypeChecking"
        return self.filetest(file)

    def test_TypeCheckforwardDec(self):
        file = "M_P_TypeCheckForwardDec"
        return self.filetest(file)

    # SHOW NO DEAD CODE AFTER RETURN/BREAK/CONTINUE
    def test_DeadReturn_Break_Continue(self):
        file = "M_P_DeadReturnBreakContinue"
        return self.filetest(file)

    # ASSIGNEMT 6
    def test_OneDimeArray(self):
        file = "M_P_Array"
        return self.filetest(file)

    def test_Printf(self):
        file = "M_P_printf"
        return self.filetest(file)

    def test_Scanf(self):
        file = "M_P_scanf"
        return self.filetest(file)

    def test_include(self):
        file = "M_P_include"
        return self.filetest(file)


# EXTRA
# TODO: CHECK WHAT EXTRA WE ARE IMPLEMENTING


class Mips_TestCasesErrors(unittest.TestCase):
    pass
    # ASSIGNEMT 2
    # Syntax errors + error message
    # Semantic errors + error message:
    """
    * Usage of uninitialised and undeclared variables
    ∗ Redeclarations and redefinitions of existing variables
    ∗ Operations and assignments with incompatible types
    ∗ Assignment to an rvalue expression
    ∗ Re-assignment of const variables
    
    """
# LOCAL/GLOBAL VARIABLES

# type checking

# include

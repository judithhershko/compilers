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

    # MANDITORY
    # ASSIGNEMT 1
    def test_binaryArithmeticOperators(self):
        # Binary arithmetic operators: +, -, *, /
        file = "M_P_BinaryArithmeticOperators"
        return self.filetest(file)

    def test_binaryComparatorOperators(self):
        # Binary arithmetic operators: <, >, ==
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

    # SHOW AST OF CONSTANT FOLDING
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

    # SHOW SYMBOLTABLE ANON SCOPE
    def test_AnonScope(self):
        file = "M_P_AnonScope"
        return self.filetest(file)

    # ASSIGNEMT 5
    def test_functionScope(self):
        file = "M_P_functionScope"
        return self.filetest(file)

    # SHOW SYMBOLTABLE FUNCTION SCOPE
    def test_LocalGlobalVariables(self):
        file = "M_P_LocalGlobal"
        return self.filetest(file)

    def test_Functions1(self):
        """
        ∗ Definition and declaration
        ∗ Calling
        ∗ Parameters (primitives and pointers, pass-by-value, pass-by-reference)
        ∗ Return values
        ∗ Functions with void return
        """
        file = "M_P_Functions1"
        return self.filetest(file)

    def test_Functions2(self):
        file = "M_P_Functions2"
        return self.filetest(file)

    def test_FunctionVoid(self):
        file = "M_P_functionVoid"
        return self.filetest(file)

    def test_FowardDeclaration(self):
        file = "M_P_ForwardDeclaration"
        return self.filetest(file)

    # SHOW NO DEAD CODE AFTER RETURN/BREAK/CONTINUE
    def test_DeadReturn_Break_Continue(self):
        file = "M_P_DeadReturnBreakContinue"
        return self.filetest(file)

    # ASSIGNEMT 6 # TODO: progress from here
    def test_OneDimArray(self):
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
# - else if
# - uitgebreide constant propagation + folding
# – Additional logical operators: >=, <=, !=
# – Modulo operator: %
# – Increment, decrement operators: ++, -- (both prefix and suﬀix variants) ???????
# – Store comments in AST and machine code ??????
# - array: int x[2] = {1,2}


class Mips_TestCasesErrors(unittest.TestCase):
    # ASSIGNMENT 1
    def test_synErr_operators1(self):
        file = "M_synErr_operators1"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 2 has a syntax error. Please check the code.")

    def test_synErr_operators2(self):
        file = "M_synErr_operators2"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 2 has a syntax error. Please check the code.")

    def test_synErr_operators3(self):
        file = "M_synErr_operators3"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 4 has a syntax error. Please check the code.")

    def test_synErr_operators4(self):
        file = "M_synErr_operators4"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "")

    #TODO: add syntax error for logical operators

    # ASSIGNMENT 2
    def test_synErr_variable(self):
        file = "M_synErr_variable"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 3 has a syntax error. Please check the code.")

    def test_synErr_float1(self):
        file = "M_synErr_float1"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 4 has a syntax error. Please check the code.")

    def test_synErr_float2(self):
        file = "M_synErr_float2"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 5 has a syntax error. Please check the code.")

    def test_synErr_charEmpty(self):
        file = "M_synErr_charEmpty"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 3: '' char size should be one.")

    def test_synErr_charMultiple(self):
        file = "M_synErr_charMultiple"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 3: 'abcdef' char size should be one.")

    def test_synErr_constVar1(self):
        file = "M_synErr_constVar1"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 2 has a syntax error. Please check the code.")

    def test_synErr_constVar2(self):
        file = "M_synErr_constVar2"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 2 has a syntax error. Please check the code.")

    def test_synErr_constVar3(self):
        file = "M_synErr_constVar3"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 2 has a syntax error. Please check the code.")

    def test_synErr_constVar4(self):
        file = "M_synErr_constVar4"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 2 has a syntax error. Please check the code.")

    def test_synErr_pointerDec1(self):
        file = "M_synErr_pointerDec1"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 3 has a syntax error. Please check the code.")

    def test_synErr_pointerDec2(self):
        file = "M_synErr_pointerDec2"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 3 has a syntax error. Please check the code.")

    def test_synErr_pointerOpp1(self):
        file = "M_synErr_pointerOpp1"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 9 has a syntax error. Please check the code.")

    def test_synErr_pointerOpp2(self):
        file = "M_synErr_pointerOpp2"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "")

    def test_synErr_pointerOpp3(self):
        file = "M_synErr_pointerOpp3"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 11 has a syntax error. Please check the code.")

    def test_semErr_varUndeclared1(self):
        file = "M_semErr_varUndeclared1"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 6: x is not declared")

    def test_semErr_varUndeclared2(self):
        file = "M_semErr_varUndeclared2"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 3: x is not declared")

    def test_semErr_varRedeclared(self):
        file = "M_semErr_varRedeclared"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 5: there is a redeclaration of the variable x")

    def test_semErr_varRedefinition(self):
        file = "M_semErr_varRedefinition"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 4: there is a redeclaration of the variable f")

    def test_semErr_incompatibleTypes1(self):
        file = "M_semErr_incompatibleTypes1"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception),
                         "\n\tError in line 9: x_ptr should reference a level 2 pointer and not the given 0")

    def test_semErr_incompatibleTypes2(self):
        file = "M_semErr_incompatibleTypes2"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception),
                         "\n\tError in line 6: x_ptr should reference a variable with a reference level of 1 "
                         "and not the given 0")

    def test_semErr_incompatibleTypes3(self):
        file = "M_semErr_incompatibleTypes3"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 5: INT can not be placed in a variable of type CHAR")

    def test_semErr_incompatibleTypes4(self):
        file = "M_semErr_incompatibleTypes4"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception),
                         "\n\tError in line 7: the binary operator + can not be executed on a INT and a CHAR")

    def test_semErr_assignRvalue1(self):
        file = "M_semErr_assignRvalue1"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 4 has a syntax error. Please check the code.")

    def test_semErr_assignRvalue2(self):
        file = "M_semErr_assignRvalue2"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 4 has a syntax error. Please check the code.")

    def test_semErr_assignConstVar(self):
        file = "M_semErr_assignConstVar"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 4: there is a reassignment of the const variable x")

    def test_semErr_assignConstPointer(self):
        file = "M_semErr_assignConstPointer"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 7: there is a reassignment of the const pointer x_ptr")

    # ASSIGNMENT 3
    def test_synErr_singleLineComment1(self):
        file = "M_synErr_singleLineComment1"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 2 has a syntax error. Please check the code.")

    def test_synErr_singleLineComment2(self):
        file = "M_synErr_singleLineComment2"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 4 has a syntax error. Please check the code.")

    def test_synErr_singleLineComment3(self):
        file = "M_synErr_singleLineComment3"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 3 has a syntax error. Please check the code.")

    def test_synErr_multiLineComment1(self):
        file = "M_synErr_multiLineComment1"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 4 has a syntax error. Please check the code.")

    def test_synErr_multiLineComment2(self):
        file = "M_synErr_multiLineComment2"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 10 has a syntax error. Please check the code.")

    # ASSIGNMENT 4
    def test_synErr_ifElse1(self):
        file = "M_synErr_ifElse1"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 5 has a syntax error. Please check the code.")

    def test_synErr_ifElse2(self):
        file = "M_synErr_ifElse2"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 6 has a syntax error. Please check the code.")

    def test_synErr_ifElse3(self):
        file = "M_synErr_ifElse3"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 18 has a syntax error. Please check the code.")

    def test_synErr_while1(self):
        file = "M_synErr_while1"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 5 has a syntax error. Please check the code.")

    def test_synErr_while2(self):
        file = "M_synErr_while2"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 10 has a syntax error. Please check the code.")

    def test_synErr_while3(self):
        file = "M_synErr_while3"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 5 has a syntax error. Please check the code.")

    def test_synErr_for1(self):
        file = "M_synErr_for1"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 4 has a syntax error. Please check the code.")

    def test_synErr_for2(self):
        file = "M_synErr_for2"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 4 has a syntax error. Please check the code.")

    def test_synErr_for3(self):
        file = "M_synErr_for3"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 4 has a syntax error. Please check the code.")

    def test_synErr_break(self):
        file = "M_synErr_break"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 8: brek is not declared")

    def test_synErr_continue(self):
        file = "M_synErr_continue"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 12 has a syntax error. Please check the code.")

    # ASSIGNMENT 5
    def test_synErr_function(self):
        file = "M_synErr_function"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 3 has a syntax error. Please check the code.")

    def test_semErr_returnTypeChecking1(self):
        file = "M_semErr_returnTypeChecking1"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception),
                         "\n\tError in line 3: the function f is initialised with return type INT but returns CHAR")

    def test_semErr_returnTypeChecking2(self):
        file = "M_semErr_returnTypeChecking2"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 10: INT can not be placed in a variable of type CHAR")

    def test_semErr_functionInputChecking1(self):
        file = "M_semErr_functionInputChecking1"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 9: the function f should hold exactly 1 parameters")

    def test_semErr_functionInputChecking2(self):
        file = "M_semErr_functionInputChecking2"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception),
                         "\n\tError in line 9: the function f should have type INT for the parameter x "
                         "instead of the given CHAR")

    def test_semErr_functionInputChecking3(self):
        file = "M_semErr_functionInputChecking3"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 9: the function f should hold exactly 1 parameters")

    def test_semErr_forwardDeclaration1(self):
        file = "M_semErr_forwardDeclaration1"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception),
                         "\n\tError in line 3: the parameters of the function f do not have the same types "
                         "as the forward declaration")

    def test_semErr_forwardDeclaration2(self):
        file = "M_semErr_forwardDeclaration2"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception),
                         "\n\tError in line 3: the parameters of the function f do not have the same types "
                         "as the forward declaration")

    def test_semErr_undeclaredFunction(self):
        file = "M_semErr_undeclaredFunction"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 4: f has not been declared yet")

    def test_semErr_declaredFunctionLocal(self):
        file = "M_semErr_declaredFunctionLocal"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 3 has a syntax error. Please check the code.")

    def test_semErr_returnOutsideFunction(self):
        file = "M_semErr_returnOutsideFunction"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 0: main has not been declared yet")

    # ASSIGNMENT 6
    def test_synErr_array1(self):
        file = "M_synErr_array1"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 2 has a syntax error. Please check the code.")

    def test_synErr_array2(self):
        file = "M_synErr_array2"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 2 has a syntax error. Please check the code.")

    # ASSIGNMENT 6
    def test_semErr_arrayIndex1(self):
        file = "M_semErr_arrayIndex1"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 3: 0.5x is not declared")

    def test_semErr_arrayIndex2(self):
        file = "M_semErr_arrayIndex2"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 3: 2x is not declared")

    def test_semErr_arrayCompare(self):
        file = "M_semErr_arrayCompare"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 4: no operations can be done with the full array a")

    def test_synErr_print(self):
        file = "M_synErr_print"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 5 has a syntax error. Please check the code.")

    def test_semErr_print1(self):
        file = "M_semErr_print1"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception),
                         "\n\tError in line 5: the print expects the same amount of flags and values")

    def test_semErr_print2(self):
        file = "M_semErr_print2"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 5 has a syntax error. Please check the code.")

    def test_synErr_scan(self):
        file = "M_synErr_scan"
        with self.assertRaises(Exception) as ce:
            testFile(file)
        self.assertEqual(str(ce.exception), "\n\tError in line 5: the scan expects the same amount of flags and values")

    def test_semErr_scan1(self):
        file = "M_semErr_scan1"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 4 has a syntax error. Please check the code.")

    def test_semErr_scan2(self):
        file = "M_semErr_scan2"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 4 has a syntax error. Please check the code.")

    def test_synErr_include1(self):
        file = "M_synErr_include1"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 1 has a syntax error. Please check the code.")

    def test_synErr_include2(self):
        file = "M_synErr_include2"
        with self.assertRaises(SystemExit) as ce:
            testFile(file)
        self.assertEqual(ce.exception.code, "Line 1 has a syntax error. Please check the code.")

    

# LOCAL/GLOBAL VARIABLES

# type checking

# include
if __name__ == '__main__':
    unittest.main()

import filecmp
import unittest
from src.CustomListener import *
from src.LLVM.LLVM_Operators import ToLLVM
from src.CustomErrorListener import *
from generated.input.ExpressionLexer import ExpressionLexer
from generated.input.ExpressionParser import ExpressionParser


def testFile(fileName):
    argv = "../input/projecten_123_met_main/" + fileName + ".c"
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
    # printer = Expression()
    printer = CustomListener("")
    # result = EvalVisitor().visit(tree)
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    printer.get_program("../tests_LLVM/dot_output/" + fileName + ".dot")
    printer.program.printTables("../tests_LLVM/symbolTables/" + fileName + "/")

    to_llvm = ToLLVM()
    to_llvm.transverse_program(printer.program)
    to_llvm.write_to_file("../tests_LLVM/LLVM_output/" + fileName + ".ll")


class LLVM_TestCases_Working(unittest.TestCase):
    def test_binaryOperations1(self):
        file = "proj2_man_pass_pointerOperations2"
        try:
            testFile(file)
        except SystemExit:
            sys.exit()

        self.assertTrue(filecmp.cmp("LLVM_output/" + file + ".ll", "LLVM_expected/" + file + ".ll"))


if __name__ == '__main__':
    unittest.main()

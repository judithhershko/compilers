import filecmp
import unittest
from src.CustomListener import *
from src.LLVM.LLVM_Operators import ToLLVM
from src.CustomErrorListener import *
from generated.input.ExpressionLexer import ExpressionLexer
from generated.input.ExpressionParser import ExpressionParser


class LLVM_TestCases_Working(unittest.TestCase):
    def test_binaryOperations1(self):
        fileName = "proj1_man_pass_constantFolding"
        try:
            argv = "../input/projecten_123_met_main/"+fileName+".c"
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
            printer = CustomListener("../tests_LLVM/dot_output/"+fileName+"_extra.dot")
            # result = EvalVisitor().visit(tree)
            walker = ParseTreeWalker()
            walker.walk(printer, tree)
            printer.get_program("../tests_LLVM/dot_output/"+fileName+".dot")

            to_llvm = ToLLVM()
            to_llvm.transverse_program(printer.program)
            to_llvm.write_to_file("../tests_LLVM/LLVM_output/"+fileName+".ll")
        except SystemExit:
            sys.exit()


if __name__ == '__main__':
    unittest.main()

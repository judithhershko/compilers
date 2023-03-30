import filecmp
import unittest
from src.CustomListener import *
from src.LLVM.LLVM_Operators import ToLLVM
from src.CustomErrorListener import *
from generated.input.ExpressionLexer import ExpressionLexer
from generated.input.ExpressionParser import ExpressionParser


class LLVM_TestCases(unittest.TestCase):
    def test_workingFile(self):
        file = "InputFiles/fullExample.c"
        input_stream = FileStream(file)
        lexer = ExpressionLexer(input_stream)
        MyError = CustomError()
        lexer.removeErrorListeners()
        lexer.addErrorListener(MyError)
        stream = CommonTokenStream(lexer)
        parser = ExpressionParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(MyError)
        tree = parser.start_rule()
        printer = CustomListener("DotFiles/fullExample")
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
        to_llvm = ToLLVM()
        to_llvm.transverse_block(printer.c_block)
        to_llvm.write_to_file("Results/llvm_fullExample.ll")

        print(filecmp.cmp("Results/llvm_fullExample.ll", "ExpectedResults/llvm_fullExample.ll"))
        self.assertTrue(filecmp.cmp("Results/llvm_fullExample.ll", "ExpectedResults/llvm_fullExample.ll"))

    def test
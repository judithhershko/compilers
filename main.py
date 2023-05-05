import sys

from generated.input.ExpressionLexer import ExpressionLexer
from generated.input.ExpressionParser import ExpressionParser
from antlr4 import *
from src.CustomListener import *
from src.LLVM.LLVM_Operators import ToLLVM
from src.CustomErrorListener import *
from src.ErrorHandeling.GenerateError import *
from src.CustomErrorListener import *


def main():
    try:
        argv = "input/input.c"
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
        printer = CustomListener("./src/ast/dotFiles/no_fold_expression_dot")
        # result = EvalVisitor().visit(tree)
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
        printer.get_program("./src/ast/dotFiles/no_fold_expression_dot")
        printer.program.printTables("./src/ast/dotFiles/table")

        # to_llvm = ToLLVM()
        # to_llvm.transverse_program(printer.program)
        # to_llvm.write_to_file("./generated/output/llvm_output.ll")
        return
    except SystemExit:
        sys.exit()


if __name__ == '__main__':
    main()

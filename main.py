import sys

from generated.input.ExpressionLexer import ExpressionLexer
from generated.input.ExpressionParser import ExpressionParser
from antlr4 import *
from src import Listener
from src.Listener import *
from src.Visitor import *


def main(argv):
    print('in main')
    input_stream = FileStream(argv[1])
    lexer = ExpressionLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ExpressionParser(stream)
    tree = parser.start_rule()
    printer=Expression()
    result=EvalVisitor().visit(tree)
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    printer.asT.generateDot("dot_output")




if __name__ == '__main__':
    main(sys.argv)
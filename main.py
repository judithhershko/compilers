import sys
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from antlr4 import *


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = ExprLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ExprParser(stream)
    # tree = parser.startRule()


if __name__ == '__main__':
    main(sys.argv);

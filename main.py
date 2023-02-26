import sys
from generated.input.ExpressionLexer import ExpressionLexer
from generated.input.ExpressionParser import ExpressionParser
from antlr4 import *


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = ExpressionLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ExpressionParser(stream)
    # tree = parser.program()


if __name__ == '__main__':
    main(sys.argv)

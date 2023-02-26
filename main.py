import sys
from generated.input.ExpressionLexer import ExpressionLexer
from generated.input.ExpressionParser import ExpressionParser
from antlr4 import *
from src import Listener
from src.Listener import Expression_


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = ExpressionLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ExpressionParser(stream)
    tree = parser.start_rule()
    printer=Expression_()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)



if __name__ == '__main__':
    main(sys.argv)

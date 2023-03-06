import sys

from generated.input.ExpressionLexer import ExpressionLexer
from generated.input.ExpressionParser import ExpressionParser
from antlr4 import *
from src import Listener
from src.Listener import *
from src.Visitor import *


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = ExpressionLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ExpressionParser(stream)
    tree = parser.start_rule()
    printer = Expression()
    #result = EvalVisitor().visit(tree)
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    print("end of walk")
    printer.asT.setRoot(printer.current)
    printer.trees.append(printer.asT)
    i = 0
    for tree in printer.trees:
        if tree is not None:
            tree.setNodeIds(printer.asT.root)
            tree.generateDot("expression_dot" + str(i))
            i += 1
    # printer.asT.setNodeIds(printer.asT.root)
    # printer.asT.generateDot("expression_dot")
    # printer.asT.generateDot("dot_output")


if __name__ == '__main__':
    main(sys.argv)

import sys

from generated.input.ExpressionLexer import ExpressionLexer
from generated.input.ExpressionParser import ExpressionParser
from antlr4 import *
from src import Listener
from src.Listener import *
from src.Visitor import *
from src.CustomListener import *


def main():
    argv="input/input.c"
    input_stream = FileStream(argv)
    lexer = ExpressionLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ExpressionParser(stream)
    tree = parser.start_rule()
    #printer = Expression()
    printer=CustomListener()
    #result = EvalVisitor().visit(tree)
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    print("end of walk")
    """
    if printer.current is not None:
        printer.asT.setRoot(printer.current)
        printer.trees.append(printer.asT)
    """
    """
    i = 0
    for tree in printer.trees:
        if tree is not None:
            tree.setNodeIds(printer.asT.root)
            tree.generateDot("expression_dot" + str(i))
            i += 1
    """
    p=Declaration()
    p.leftChild=Value('x',LiteralType.VAR,p)
    p.rightChild=BinaryOperator("+")
    p.rightChild.leftChild=Value(4.7,LiteralType.FLOAT)
    p.rightChild.rightChild=Value(7.98,LiteralType.FLOAT)
    t=AST()
    t.setRoot(p)
    t.setNodeIds(t.root)
    t.foldTree()
    t.setNodeIds(t.root)
    t.generateDot("test_dot")


if __name__ == '__main__':
    main()

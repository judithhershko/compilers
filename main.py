from generated.input.ExpressionLexer import ExpressionLexer
from generated.input.ExpressionParser import ExpressionParser
from antlr4 import *
from src.CustomListener import *
from src.LLVM.LLVM_Operators import ToLLVM
from src.CustomErrorListener import *

def main():
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
    printer = CustomListener()
    # result = EvalVisitor().visit(tree)
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    print("end of walk")
    to_llvm=ToLLVM()
    #to_llvm.transverse_block(printer.c_block)
    #to_llvm.write_to_file("llvm_output.ll")
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

    # p=Declaration()
    left=Value('x',LiteralType.FLOAT,1)
    p=Declaration(left, 1)
    left.parent = p
    p.rightChild=BinaryOperator("+", 1)
    p.rightChild.leftChild=Value(4.7,LiteralType.FLOAT,1)
    p.rightChild.rightChild=Value(7.98,LiteralType.FLOAT,1)
    t=AST()
    t.setRoot(p)
    t.setNodeIds(t.root)
    t.foldTree()
    t.setNodeIds(t.root)
    t.generateDot("test_dot")


if __name__ == '__main__':
    main()

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

        self.assertTrue(filecmp.cmp("Results/llvm_fullExample.ll", "ExpectedResults/llvm_fullExample.ll"))

    def test_SyntaxError(self):
        file = "InputFiles/MissingClosingBracket.c"
        input_stream = FileStream(file)
        lexer = ExpressionLexer(input_stream)
        MyError = CustomError()
        lexer.removeErrorListeners()
        lexer.addErrorListener(MyError)
        stream = CommonTokenStream(lexer)
        parser = ExpressionParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(MyError)
        try:
            parser.start_rule()
            self.assertTrue(False)
        except SystemExit:
            self.assertTrue(True)

        file = "InputFiles/MissingOpeningBracket.c"
        input_stream = FileStream(file)
        lexer = ExpressionLexer(input_stream)
        MyError = CustomError()
        lexer.removeErrorListeners()
        lexer.addErrorListener(MyError)
        stream = CommonTokenStream(lexer)
        parser = ExpressionParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(MyError)
        try:
            parser.start_rule()
            self.assertTrue(False)
        except SystemExit:
            self.assertTrue(True)

        file = "InputFiles/MissingSemicolon.c"
        input_stream = FileStream(file)
        lexer = ExpressionLexer(input_stream)
        MyError = CustomError()
        lexer.removeErrorListeners()
        lexer.addErrorListener(MyError)
        stream = CommonTokenStream(lexer)
        parser = ExpressionParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(MyError)
        try:
            parser.start_rule()
            self.assertTrue(False)
        except SystemExit:
            self.assertTrue(True)

        file = "InputFiles/NotAComment.c"
        input_stream = FileStream(file)
        lexer = ExpressionLexer(input_stream)
        MyError = CustomError()
        lexer.removeErrorListeners()
        lexer.addErrorListener(MyError)
        stream = CommonTokenStream(lexer)
        parser = ExpressionParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(MyError)
        try:
            parser.start_rule()
            self.assertTrue(False)
        except SystemExit:
            self.assertTrue(True)

    def test_NotDeclared(self):
        file = "InputFiles/NotDeclared1.c"
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
        printer = CustomListener("DotFiles/NotDeclared")
        walker = ParseTreeWalker()
        with self.assertRaises(Exception) as excep:
            walker.walk(printer, tree)
        self.assertEqual("\n\tError in line 1: x has not been declared yet", str(excep.exception))

        file = "InputFiles/NotDeclared2.c"
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
        printer = CustomListener("DotFiles/NotDeclared")
        walker = ParseTreeWalker()
        with self.assertRaises(Exception) as excep:
            walker.walk(printer, tree)
        self.assertEqual("\n\tError in line 1: z has not been declared yet", str(excep.exception))

        file = "InputFiles/NotDeclared3.c"
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
        printer = CustomListener("DotFiles/NotDeclared")
        walker = ParseTreeWalker()
        with self.assertRaises(Exception) as excep:
            walker.walk(printer, tree)
        self.assertEqual("\n\tError in line 1: z has not been declared yet", str(excep.exception))

    def test_Redefined(self):
        file = "InputFiles/Redefined1.c"
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
        printer = CustomListener("DotFiles/NotDeclared")
        walker = ParseTreeWalker()
        with self.assertRaises(Exception) as excep:
            walker.walk(printer, tree)
        self.assertEqual("\n\tError in line 2: there is a redeclaration of the variable x", str(excep.exception))

        file = "InputFiles/Redefined2.c"
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
        printer = CustomListener("DotFiles/NotDeclared")
        walker = ParseTreeWalker()
        with self.assertRaises(Exception) as excep:
            walker.walk(printer, tree)
        self.assertEqual("\n\tError in line 4: there is a redeclaration of the pointer y", str(excep.exception))

    def test_wrongType(self):
        file = "InputFiles/WrongType1.c"
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
        printer = CustomListener("DotFiles/NotDeclared")
        walker = ParseTreeWalker()
        with self.assertRaises(Exception) as excep:
            walker.walk(printer, tree)
        self.assertEqual("\n\tError in line 1: FLOAT can not be placed in a variable of type INT", str(excep.exception))

        file = "InputFiles/WrongType2.c"
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
        printer = CustomListener("DotFiles/NotDeclared")
        walker = ParseTreeWalker()
        with self.assertRaises(Exception) as excep:
            walker.walk(printer, tree)
        self.assertEqual("\n\tError in line 2: CHAR can not be placed in a variable of type INT", str(excep.exception))

        file = "InputFiles/WrongType3.c"
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
        printer = CustomListener("DotFiles/NotDeclared")
        walker = ParseTreeWalker()
        with self.assertRaises(Exception) as excep:
            walker.walk(printer, tree)
        self.assertEqual("\n\tError in line 2: the pointer has type FLOAT, while the referenced variable y has type INT",
                         str(excep.exception))

        file = "InputFiles/WrongType4.c"
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
        printer = CustomListener("DotFiles/NotDeclared")
        walker = ParseTreeWalker()
        with self.assertRaises(Exception) as excep:
            walker.walk(printer, tree)
        self.assertEqual("\n\tError in line 3: FLOAT can not be placed in a variable of type INT", str(excep.exception))

        file = "InputFiles/WrongType5.c"
        input_stream = FileStream(file)
        lexer = ExpressionLexer(input_stream)
        MyError = CustomError()
        lexer.removeErrorListeners()
        lexer.addErrorListener(MyError)
        stream = CommonTokenStream(lexer)
        parser = ExpressionParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(MyError)
        try:
            parser.start_rule()
            self.assertTrue(False)
        except SystemExit:
            self.assertTrue(True)

        file = "InputFiles/WrongType6.c"
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
        printer = CustomListener("DotFiles/NotDeclared")
        walker = ParseTreeWalker()
        with self.assertRaises(Exception) as excep:
            walker.walk(printer, tree)
        self.assertEqual("\n\tError in line 1: FLOAT can not be placed in a variable of type INT", str(excep.exception))


    def test_Const(self):
        file = "InputFiles/Const1.c"
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
        printer = CustomListener("DotFiles/NotDeclared")
        walker = ParseTreeWalker()
        with self.assertRaises(Exception) as excep:
            walker.walk(printer, tree)
        self.assertEqual("\n\tError in line 2: there is a reassignment of the const variable x", str(excep.exception))

        file = "InputFiles/Const2.c"
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
        printer = CustomListener("DotFiles/NotDeclared")
        walker = ParseTreeWalker()
        with self.assertRaises(Exception) as excep:
            walker.walk(printer, tree)
        self.assertEqual("\n\tError in line 3: there is a reassignment of the const variable x", str(excep.exception))

        file = "InputFiles/Const3.c"
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
        printer = CustomListener("DotFiles/NotDeclared")
        walker = ParseTreeWalker()
        with self.assertRaises(Exception) as excep:
            walker.walk(printer, tree)
        self.assertEqual("\n\tError in line 3: there is a reassignment of the const pointer y", str(excep.exception))

    def test_WrongVariableName(self):
        file = "InputFiles/AssignedRValue1.c"
        input_stream = FileStream(file)
        lexer = ExpressionLexer(input_stream)
        MyError = CustomError()
        lexer.removeErrorListeners()
        lexer.addErrorListener(MyError)
        stream = CommonTokenStream(lexer)
        parser = ExpressionParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(MyError)
        try:
            parser.start_rule()
            self.assertTrue(False)
        except SystemExit:
            self.assertTrue(True)

        file = "InputFiles/AssignedRValue2.c"
        input_stream = FileStream(file)
        lexer = ExpressionLexer(input_stream)
        MyError = CustomError()
        lexer.removeErrorListeners()
        lexer.addErrorListener(MyError)
        stream = CommonTokenStream(lexer)
        parser = ExpressionParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(MyError)
        try:
            parser.start_rule()
            self.assertTrue(False)
        except SystemExit:
            self.assertTrue(True)

        file = "InputFiles/AssignedReservedWord1.c"
        input_stream = FileStream(file)
        lexer = ExpressionLexer(input_stream)
        MyError = CustomError()
        lexer.removeErrorListeners()
        lexer.addErrorListener(MyError)
        stream = CommonTokenStream(lexer)
        parser = ExpressionParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(MyError)
        try:
            parser.start_rule()
            self.assertTrue(False)
        except SystemExit:
            self.assertTrue(True)

        file = "InputFiles/AssignedReservedWord2.c"
        input_stream = FileStream(file)
        lexer = ExpressionLexer(input_stream)
        MyError = CustomError()
        lexer.removeErrorListeners()
        lexer.addErrorListener(MyError)
        stream = CommonTokenStream(lexer)
        parser = ExpressionParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(MyError)
        try:
            parser.start_rule()
            self.assertTrue(False)
        except SystemExit:
            self.assertTrue(True)

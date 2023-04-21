from antlr4.error.ErrorListener import *


class CustomError(ErrorListener):
    INSTANCE = None

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("Line " + str(line) + " has a syntax error. Please check the code.", file=sys.stderr)
        # sys.exit()
        raise SystemExit


CustomError.INSTANCE = CustomError()

from src.ErrorHandeling.GenerateError import NotSupported


class Value:
    pass


class HelperLLVM:
    def __init__(self):
        self.g_assigment = ""
        self.parameters = []


def set_llvm_comparators(left: Value, right: Value, op: str):
    pass


def set_llvm_binary_operators(left: Value, right: Value, op: str, parameters):
    print("binary operator called")
    # get all types
    # move higher type if necessary

    if op == "*":
        pass
    elif op == "/":
        pass
    elif op == "+":
        pass
    elif op == "-":
        pass
    elif op == "%":
        pass
    else:
        raise NotSupported("binary operator", op, left.line)

    return ""

from pandas._libs.lib import Enum

from src.ErrorHandeling.GenerateError import NotSupported
from src.ast.node_types.node_type import LiteralType


class Value:
    pass


class Pointer:
    pass


class HelperLLVM:
    def __init__(self):
        self.g_assigment = ""
        self.parameters = []
        self.load = ""
        self.store = ""


def to_type(ptype):
    pass


def set_llvm_comparators(left: Value, right: Value, op: str):
    pass


def load_type(old, new, ptype_, pointer):
    if pointer:
        return "%{} = load ptr, ptr %{}, align 4\n".format(new, old)
    if ptype_ == LiteralType.INT:
        return "%{} = load i32, ptr %{}, align 4\n".format(new, old)
    if ptype_ == LiteralType.FLOAT:
        return "%{} = load float, ptr %{}, align 4\n".format(new, old)
    if ptype_ == LiteralType.CHAR:
        return "%{} = load i8, ptr %{}, align 4\n".format(new, old)
    if ptype_ == LiteralType.BOOL:
        return "%{} = load i1, ptr %{}, align 4\n".format(new, old)


def load_higher_type_int_to_float(old, new):
    return "%{} = sitofp i32 %{} to float".format(new, old)


def store_mult(left, right, rtype, llvm):
    load = ""
    old_left = llvm.get_variable(left.value)
    if rtype == LiteralType.INT:
        load += "% {} = mult nsw i32 %{}, %{}\n".format(llvm.add_variable(left.value), old_left,
                                                        llvm.get_variable(right.value))
    elif rtype == LiteralType.FLOAT:
        load += " %{} = call float @llvm.fmuladd.f32(float %{}, float %{}, float %{})\n".format(
            llvm.add_variable(left.value), old_left, llvm.get_variable(left.value), llvm.get_variable(right.value))
    return load


def store_div(left, right, rtype, llvm):
    """%2 = load i32, ptr %1, align 4
    % 3 = add nsw i32 %2, %4"""
    load = ""
    old_left = llvm.get_variable(left.value)
    if rtype == LiteralType.INT:
        load += "% {} = sdiv nsw i32 %{}, %{}\n".format(llvm.add_variable(left.value), old_left,
                                                        llvm.get_variable(right.value))
    elif rtype == LiteralType.FLOAT:
        load += "%{} = fdiv float %{}, %{}\n".format(llvm.add_variable(left.value), old_left,
                                                     llvm.get_variable(right.value))
    return load


def store_add(left, right, rtype, llvm):
    load = ""
    old_left = llvm.get_variable(left.value)
    if rtype == LiteralType.INT:
        load += "% {} = add nsw i32 %{}, %{}\n".format(llvm.add_variable(left.value), old_left,
                                                       llvm.get_variable(right.value))
    elif rtype==LiteralType.FLOAT:
        load+="%{} = fadd float %{}, %{}\n".format(llvm.add_variable(left.value), old_left,
                                                       llvm.get_variable(right.value))
    return load


def store_min(left, right, rtype, llvm):
    load = ""
    old_left = llvm.get_variable(left)
    if rtype == LiteralType.INT:
        load += "% {} = sub nsw i32 %{}, %{}\n".format(llvm.add_variable(left), old_left, llvm.get_variable(right))
    elif rtype == LiteralType.FLOAT:
        load += "% {} = fsub float %{}, %{}\n".format(llvm.add_variable(left), old_left, llvm.get_variable(right))
    return load


def store_mod(left, right, rtype, llvm):
    load = ""
    old_left = llvm.get_variable(left)
    if rtype == LiteralType.INT:
        load += "% {} = srem nsw i32 %{}, %{}\n".format(llvm.add_variable(left), old_left, llvm.get_variable(right))
    elif rtype == LiteralType.FLOAT:
        raise NotSupported("%", "float")
    return load


def set_llvm_binary_operators(left: Value, right: Value, op: str, llvm):
    print("binary operator called")
    # get all types
    # move higher type if necessary
    """
    %5 = load i32, ptr %3, align 4
    %6 = load i32, ptr %3, align 4
    %7 = add nsw i32 %5, %6
    store i32 %7, ptr %3, align 4
    %8 = load i32, ptr %3, align 4
    ret i32 %8
    """
    ltype = None
    rype = None
    if left.variable:
        old_var = llvm.get_variable(left.value)
        llvm.add_variable(left.value)
        if llvm.c_function.root.block.getSymbolTable().findSymbol(left.value) is None:
            ltype = llvm.parameters[left.value].getType()
        else:
            ltype = llvm.c_function.root.block.getSymbolTable().findSymbol(right.value)[1]
        llvm.function_load += load_type(old_var, llvm.get_variable(left.value), ltype, isinstance(left, Pointer))
    else:
        ltype = left.getType()

    if right.variable:
        old_var = llvm.get_variable(right.value)
        llvm.add_variable(right.value)
        if llvm.c_function.root.block.getSymbolTable().findSymbol(right.value) is None:
            rtype = llvm.parameters[right.value].getType()
        else:
            rtype = llvm.c_function.root.block.getSymbolTable().findSymbol(right.value)[1]
        llvm.function_load += load_type(old_var, llvm.get_variable(right.value), rtype, isinstance(right, Pointer))
    else:
        rtype = right.getType()
    # fix different types

    if rtype == LiteralType.FLOAT and ltype == LiteralType.INT:
        llvm.function_load += load_higher_type_int_to_float(llvm.get_variable(left.value),
                                                            llvm.add_variable(left.value))
    if rtype == LiteralType.INT and ltype == LiteralType.FLOAT:
        llvm.function_load += load_higher_type_int_to_float(llvm.get_variable(right.value),
                                                            llvm.add_variable(right.value))
        rtype = LiteralType.FLOAT

    if op == "*":
        llvm.function_load += store_mult(left, right, rtype, llvm)
    elif op == "/":
        llvm.function_load += store_div(left, right, rtype, llvm)
    elif op == "+":
        llvm.function_load += store_add(left, right, rtype, llvm)
    elif op == "-":
        llvm.function_load += store_min(left, right, rtype, llvm)
    elif op == "%":
        llvm.function_load += store_mod(left, right, rtype, llvm)
    else:
        raise NotSupported("binary operator", op, left.line)
    return ltype

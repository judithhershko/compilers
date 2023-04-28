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
    return "%{} = sitofp i32 %{} to float\n".format(new, old)


def store_mult(left, right, rtype, llvm, load_left, load_right):
    load = ""
    old_left = llvm.get_variable(left.value)
    if rtype == LiteralType.INT:
        if load_left and load_right:
            load += "% {} = mult nsw i32 %{}, %{}\n".format(llvm.add_variable(left.value), old_left,
                                                            llvm.get_variable(right.value))
        elif load_left:
            load += "% {} = mult nsw i32 %{}, {}\n".format(llvm.add_variable(left.value), old_left,
                                                           llvm.get_variable("$" + str(right.value)))
        elif load_right:
            old_right = llvm.get_variable(right.value)
            load += "% {} = mult nsw i32 {}, %{}\n".format(llvm.add_variable(right.value),
                                                           llvm.get_variable("$" + str(right.value)),
                                                           old_right)
    elif rtype == LiteralType.FLOAT:
        load += " %{} = call float @llvm.fmuladd.f32(float %{}, float %{}, float %{})\n".format(
            llvm.add_variable(left.value), old_left, llvm.get_variable(left.value), llvm.get_variable(right.value))
    return load


def get_operation(op: str, type):
    if op == "-" and type == LiteralType.INT:
        return "sub nsw i32 "
    if op == "-" and type == LiteralType.FLOAT:
        return "fsub float "
    if op == "+" and LiteralType.INT:
        return "add nsw i32 "
    if op == "+" and type == LiteralType.FLOAT:
        return "fadd float "
    if op == "*" and type == LiteralType.INT:
        return "mult nsw i32 "
    if op == "*" and type == LiteralType.FLOAT:
        return "call"
    if op == "/" and type == LiteralType.INT:
        return "sdiv nsw i32 "
    if op == "/" and type == LiteralType.FLOAT:
        return "fdiv float "
    if op == "%" and type == LiteralType.INT:
        return "srem nsw i32 "
    if op == "%" and type == LiteralType.FLOAT:
        raise NotSupported("%", "float")
    if op == ">" and type == LiteralType.INT:
        return "icmp sgt i32 "
    if op == ">" and type == LiteralType.FLOAT:
        return "fcmp ogt float "
    if op == ">=" and type == LiteralType.INT:
        return "icmp sge i32 "
    if op == ">=" and type == LiteralType.FLOAT:
        return "fcmp oge float "
    if op == "<" and type == LiteralType.INT:
        return "icmp slt i32 "
    if op == "<" and type == LiteralType.FLOAT:
        return "fcmp olt float "
    if op == "<=" and type == LiteralType.INT:
        return "icmp sle i32 "
    if op == "<=" and type == LiteralType.FLOAT:
        return "fcmp ole float "
    if op == "==" and type == LiteralType.INT:
        return "icmp eq i32 "
    if op == "==" and type == LiteralType.FLOAT:
        return "fcmp oeq float "


def store_comparator_operation(op, left, right, rtype, llvm, load_left, load_right):
    pass


def stor_binary_operation(op, left, right, rtype, llvm, load_left, load_right):
    load = ""
    op = get_operation(op, rtype)
    old_left = llvm.get_variable(left)
    if op == "call":
        if "fmuladd" not in llvm.g_def:
            llvm.f_count += 1
            llvm.f_declerations += "declare float @llvm.fmuladd.f32(float, float, float) #{}\n".format(llvm.f_count)
            llvm.g_def["fmuladd"] = True

        if load_left and load_right:
            load += " %{} = call float @llvm.fmuladd.f32(float %{}, float %{}, float %{})\n".format(
                llvm.add_variable(left.value), old_left, llvm.get_variable(left.value), llvm.get_variable(right.value))
        elif load_left:
            load += " %{} = call float @llvm.fmuladd.f32(float %{}, float %{}, float {})\n".format(
                llvm.add_variable(left.value), old_left, llvm.get_variable(left.value),
                llvm.get_variable("$" + str(right.value)))
        elif load_right:
            old_right = llvm.get_variable(right)
            load += " %{} = call float @llvm.fmuladd.f32(float {}, float {}, float %{})\n".format(
                llvm.add_variable(right.value), llvm.get_variable("$" + str(left.value)),
                llvm.get_variable(right.value),
                llvm.get_variable(right.value))

    if load_left and load_right:
        load += "%{} = ".format(llvm.add_variable(left))
        load += op
        load += "%{}, %{}\n".format(old_left, llvm.get_variable(right))
    elif load_left:
        load += "%{} = ".format(llvm.add_variable(left))
        load += op
        load += "%{}, {}\n".format(old_left, llvm.get_variable("$" + str(right.value)))
    elif load_right:
        llvm.counter -= 1
        load += "%{} = ".format(llvm.add_variable(right))
        load += op
        old_right = llvm.get_variable(right)
        load += "{}, %{}\n".format(llvm.get_variable("$" + str(right.value)), old_right)
    if not (load_right and load_left):
        pass
    return load


def set_llvm_binary_operators(left: Value, right: Value, op: str, llvm):
    print("binary operator called")
    # get all types
    # move higher type if necessary
    load_left = True
    load_right = True
    if isinstance(right.value, int):
        llvm.var_dic["$" + str(right.value)] = right.value
        load_right = False
    elif isinstance(right.value, float):
        llvm.var_dict["$" + str(right.value)] = llvm.float_to_64bit_hex(right.value)
        load_right = False
    elif isinstance(left.value, int):
        llvm.var_dic["$" + str(left.value)] = left.value
        load_left = False
    elif isinstance(right.value, float):
        llvm.var_dict["$" + str(left.value)] = llvm.float_to_64bit_hex(left.value)
        load_left = False

    if load_left:
        old_var = llvm.get_variable(left.value)
        llvm.add_variable(left.value)
        if llvm.c_function.root.block.getSymbolTable().findSymbol(left.value) is None:
            ltype = llvm.parameters[left.value].getType()
        else:
            ltype = llvm.c_function.root.block.getSymbolTable().findSymbol(left.value)[1]
        llvm.function_load += load_type(old_var, llvm.get_variable(left.value), ltype, isinstance(left, Pointer))
    else:
        ltype = left.getType()

    if load_right:
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

    if op == "*" or op == "/" or op == "+" or op == "-" or op == "%" or op == ">=" or op == "<=" or op == ">" or op == "<" or op == "==":
        llvm.function_load += stor_binary_operation(op, left, right, rtype, llvm, load_left, load_right)
    else:
        raise NotSupported("operator", op, left.line)
    return ltype

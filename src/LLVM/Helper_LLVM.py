from src.ErrorHandeling.GenerateError import NotSupported
from src.ast.node_types.node_type import LiteralType


class Pointer:
    pass


class Value:
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
        old_right = llvm.get_variable(right)
        load += "%{} = ".format(llvm.add_variable(right))
        load += op
        load += "{}, %{}\n".format(llvm.get_variable("$" + str(left.value)), old_right)
    if not (load_right and load_left):
        pass
    return load


def set_llvm_binary_operators(left: Value, right: Value, op: str, llvm):
    if left.name == 'function' or right.name == "function":
        return function_in_operation(left, right, op, llvm)
    if left.name == "array" or right.name == "array":
        return array_in_operation(left, right, op, llvm)
    left_pointer=False
    right_pointer=False
    if left.name == "pointer":
        left_pointer=True
    if right.name == "pointer":
        right_pointer=True
    if left.name == "pointer" or right.name == "pointer":
        return pointer_in_operation(left, right, op, llvm)
    print("binary operator called")
    # get all types
    # move higher type if necessary
    load_left = True
    load_right = True
    if isinstance(right.value, int) or str(right.value).isdigit():
        llvm.var_dic["$" + str(right.value)] = right.value
        load_right = False
    elif isinstance(right.value, float) or isfloat(str(right.value)):
        llvm.var_dict["$" + str(right.value)] = llvm.float_to_64bit_hex(right.value)
        load_right = False
    elif isinstance(left.value, int) or str(left.value).isdigit():
        llvm.var_dic["$" + str(left.value)] = left.value
        load_left = False
    elif isinstance(right.value, float) or isfloat(str(left.value)):
        llvm.var_dict["$" + str(left.value)] = llvm.float_to_64bit_hex(left.value)
        load_left = False

    if load_left:
        old_var = llvm.get_variable(left.value)
        llvm.add_variable(left.value)
        if left.type is LiteralType.VAR:
            if llvm.c_function.root.block.getSymbolTable().findSymbol(left.value) is None:
                ltype = llvm.parameters[left.value].getType()
            else:
                ltype = llvm.c_function.root.block.getSymbolTable().findSymbol(left.value)[1]
        else:
            ltype = left.type
        llvm.function_load += load_type(old_var, llvm.get_variable(left.value), ltype,left_pointer)
    else:
        ltype = left.getType()

    if load_right:
        old_var = llvm.get_variable(right.value)
        llvm.add_variable(right.value)
        if right.type == LiteralType.VAR:
            if llvm.c_function.root.block.getSymbolTable().findSymbol(right.value) is None:
                rtype = llvm.parameters[right.value].getType()
            else:
                rtype = llvm.c_function.root.block.getSymbolTable().findSymbol(right.value)[1]
        else:
            rtype = right.type
        llvm.function_load += load_type(old_var, llvm.get_variable(right.value), rtype, right_pointer)
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
        llvm.function_load += "\n"
    else:
        raise NotSupported("operator", op, left.line)
    return ltype


def function_in_operation(left, right, op: str, llvm):
    """
    f(z)
    %4 = call i32 @function(i32 noundef %3)
    f(0)
    %3 = call i32 @function(i32 noundef 0)

    idee: save function call in register,
    maak nieuwe value node aan voor register met de functie naam
    """
    if llvm.is_function(left):
        left = load_function(left, llvm)
    if llvm.is_function(right):
        right = load_function(right, llvm)
    # if declaration with function x=function() en geen verder operatoes
    if left is None or right is None:
        return
    return set_llvm_binary_operators(left, right, op, llvm)


def load_function(p, llvm):
    inhoud = llvm.program.functions.findFunction(p.f_name, p.line)
    return_ = llvm.program.functions.findFunction(p.f_name, p.line)
    inhoud = p.param
    llvm.add_variable(p.f_name)
    llvm.function_load += "%{} = call {} @{}".format(llvm.get_variable(p.f_name),
                                                     llvm.get_llvm_type(return_["return"]), p.f_name)
    llvm.function_load += "("
    for key in inhoud:
        llvm.function_load += llvm.get_llvm_type(inhoud[key])
        val = key
        is_var = True
        if str(key[0]).isdigit():
            is_var = False
            if inhoud[key] == LiteralType.FLOAT:
                val = llvm.float_to_64bit_hex(key)
        if is_var:
            llvm.function_load += " noundef %{}".format(llvm.get_variable(val))
        else:
            llvm.function_load += "noundef {}".format(val)

    llvm.function_load += ")\n"
    return llvm.make_value(lit=p.f_name, valueType=return_["return"], line=p.line)


def load_array(left, llvm):
    llvm.function_load += "call void @llvm.memcpy.p0.p0.i64(ptr align 4 %{}, ptr align 4 @__const.{}.{}, i64 12, i1 false)\n".format(
        llvm.get_variable(left.getValue()), llvm.c_function.f_name, left.getValue())
    llvm.add_variable(str(left.getPosition) + str(left.getValue()))
    size = llvm.c_function.block.getSymbolTable.findSymbol(left.value)[0]
    llvm.function_load += "%{} = getelementptr inbounds [{} x {}], ptr %6, i64 0, i64 1\n".format(
        llvm.get_variable(str(left.getPosition) + str(left.getValue())), size, llvm.get_llvm_type(left.getType()))
    return llvm.make_value(lit=str(left.getPosition) + str(left.getValue()), valueType=left.getType(), line=left.line)


def array_in_operation(left, right, op, llvm):
    if llvm.is_array(left):
        left = load_array(left, llvm)
    if llvm.is_array(right):
        right = load_array(right, llvm)
    # if declaration with function x=function() en geen verder operatoes
    if left is None or right is None:
        return
    return set_llvm_binary_operators(left, right, op, llvm)

def load_pointer(left, llvm):
    for i in range(1,left.getPointerLevel()):
        old_val=llvm.get_variable(left.getValue())
        new_val=llvm.add_variable(left.getValue())
        llvm.function_load += "%{} = load ptr, ptr %{}, align 8\n".format(new_val,old_val)
    return llvm.make_value(lit=new_val, valueType=left.getType(), line=left.line)


def pointer_in_operation(left, right, op, llvm):
    if llvm.is_pointer(left):
        left = load_pointer(left, llvm)
    if llvm.is_pointer(right):
        right = load_pointer(right, llvm)
    if left is None or right is None:
        return
    return set_llvm_binary_operators(left, right, op, llvm)


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

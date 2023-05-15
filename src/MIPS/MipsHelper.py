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


def load_type(old, new, ptype_, pointer, op=None):
    a = ""
    if pointer:
        a = "%{} = load ptr, ptr %{}, align 4\n".format(new, old)
        return a
    if ptype_ == LiteralType.INT:
        a = "%{} = load i32, ptr %{}, align 4\n".format(new, old)
        return a
    if ptype_ == LiteralType.FLOAT:
        a = "%{} = load float, ptr %{}, align 4\n".format(new, old)
        return a
    if ptype_ == LiteralType.CHAR:
        a = "%{} = load i8, ptr %{}, align 4\n".format(new, old)
        return a
    if ptype_ == LiteralType.BOOL:
        a = "%{} = load i1, ptr %{}, align 4\n".format(new, old)
        return a


def load_higher_type_int_to_float(old, new):
    return "%{} = sitofp i32 %{} to float\n".format(new, old)


def load_higher_type_bool_to_int(old, new):
    return "%{} = zext i1 %{} to i32\n".format(new, old)


def store_mult(left, right, rtype, llvm, load_left, load_right):
    load = ""
    old_left = llvm.get_variable(left.value)
    if rtype == LiteralType.INT:
        if load_left and load_right:
            load += "% {} = mul nsw i32 %{}, %{}\n".format(llvm.add_variable(left.value), old_left,
                                                           llvm.get_variable(right.value))
        elif load_left:
            load += "% {} = mul nsw i32 %{}, {}\n".format(llvm.add_variable(left.value), old_left,
                                                          llvm.get_variable("$" + str(right.value)))
        elif load_right:
            old_right = llvm.get_variable(right.value)
            load += "% {} = mul nsw i32 {}, %{}\n".format(llvm.add_variable(right.value),
                                                          llvm.get_variable("$" + str(right.value)),
                                                          old_right)
    elif rtype == LiteralType.FLOAT:
        load += " %{} = call float @llvm.fmuladd.f32(float %{}, float %{}, float %{})\n".format(
            llvm.add_variable(left.value), old_left, llvm.get_variable(left.value), llvm.get_variable(right.value))
    return load


def get_unary_operation(op: str, type, nr=0):
    if op == "!" and type == LiteralType.INT and nr == 1:
        return "icmp ne i32 "
    if op == "!" and type == LiteralType.FLOAT and nr == 1:
        return " icmp ne float "
    if op == "!" and type == LiteralType.INT and nr == 2:
        return "xor i1 "


def get_operation(op: str, type):
    if op == "-" and type == LiteralType.INT:
        return "subu"
    if op == "-" and type == LiteralType.FLOAT:
        return "sub.s"
    if op == "+" and LiteralType.INT:
        return "addu"
    if op == "+" and type == LiteralType.FLOAT:
        return "add.s"
    if op == "*" and type == LiteralType.INT:
        return "mul"
    if op == "*" and type == LiteralType.FLOAT:
        return "mul.s"
    if op == "/" and type == LiteralType.INT:
        return "div"
    if op == "/" and type == LiteralType.FLOAT:
        return "div.s"
    # TODO fist devide then save modulo
    if op == "%" and type == LiteralType.INT:
        return "mfhi"
    if op == "%" and type == LiteralType.FLOAT:
        raise NotSupported("%", "float")
    if op == ">" and type == LiteralType.INT:
        return "sgt"
    if op == ">" and type == LiteralType.FLOAT:
        return "sgt"
    if op == ">=" and type == LiteralType.INT:
        return "sge"
    if op == ">=" and type == LiteralType.FLOAT:
        return "sge"
    # todo switch volgorde
    if op == "<" and type == LiteralType.INT:
        return "slt"
    if op == "<" and type == LiteralType.FLOAT:
        return "slt"
    if op == "<=" and type == LiteralType.INT:
        return "sle"
    if op == "<=" and type == LiteralType.FLOAT:
        return "slte"
    if op == "==" and type == LiteralType.INT:
        return "seq"
    if op == "==" and type == LiteralType.FLOAT:
        return "seq"
    if op == "&&" and type == LiteralType.INT:
        return "and"
    if op == "&&" and type == LiteralType.FLOAT:
        return "and"
    if op == "||" and type == LiteralType.INT:
        return "or"
    if op == "||" and type == LiteralType.FLOAT:
        return "or"


def store_comparator_operation(op, left, right, rtype, llvm, load_left, load_right):
    pass


def stor_unary_operation(op, right, rtype, llvm, load_right):
    load = ""
    if load_right:
        llvm.counter -= 1
        old_right = llvm.get_variable(right)
        load += "%{} = ".format(llvm.add_variable(right))
        load += get_unary_operation(op, rtype, 1)
        load += "%{}, 0\n".format(llvm.get_variable(old_right))
        load += "%{} = ".format(llvm.add_variable(right))
        load += get_unary_operation(op, rtype, 2)
        load += "%{}, true\n".format(llvm.get_variable(old_right))
        if rtype == LiteralType.INT:
            load_higher_type_bool_to_int(llvm.add_variable(old_right), llvm.get_variable(old_right))
        elif rtype == LiteralType.FLOAT:
            load_higher_type_int_to_float(llvm.add_variable(old_right), llvm.get_variable(old_right))
    if not load_right:
        pass
    return load


def stor_binary_operation(op, left, right, rtype, llvm, load_left, load_right):
    # save olf variable counter
    llvm.save_old_val = left
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
        llvm.counter -= 1
        load += "%{} = ".format(llvm.add_variable(left))
        load += op
        load += "%{}, %{}\n".format(old_left - 2, llvm.get_variable(right) - 1)
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


def set_llvm_unary_operators(right, op: str, llvm):
    if llvm.is_binary(right) and llvm.save_old_val is None:
        right.printTables("random", llvm)
        # return llvm.to_retrans_u(right, op)
    if llvm.is_unary(right) and llvm.save_old_val is None:
        right.printTables("random", llvm)
        # return llvm.to_retrans_u(right, op)
    if llvm.is_logical(right) and llvm.save_old_val is None:
        right.printTables("random", llvm)
        # return llvm.to_retrans_u(right, op)
    if right.name == "function":
        function_in_operation(right, None, op, llvm)
        # return llvm.to_retrans_u(right, op)
    if right.name == "array":
        array_in_operation(right, None, op, llvm)
        # return llvm.to_retrans_u(right, op)
    if llvm.looping:
        if isinstance(right, Value):
            llvm.get_loop_param(right)

    right_pointer = False
    if right.name == "pointer":
        right_pointer = True
    if right.name == "pointer":
        return pointer_in_operation(right, None, op, llvm)

    load_right = True
    if isinstance(right.value, int) or str(right.value).isdigit():
        llvm.var_dic["$" + str(right.value)] = right.value
        load_right = False
    elif isinstance(right.value, float) or isfloat(str(right.value)):
        llvm.var_dict["$" + str(right.value)] = llvm.float_to_64bit_hex(right.value)
        load_right = False
    if load_right:
        old_var = llvm.get_variable(right.value)
        if right.value in llvm.allocated_var:
            old_var = llvm.allocated_var[right.value]
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

    if op == "!" or op == "++" or op == "--":
        llvm.function_load += stor_unary_operation(op, right, rtype, llvm, load_right)
        llvm.function_load += "\n"
    else:
        raise NotSupported("operator", op, right.line)
    return rtype


def set_llvm_binary_operators(left, right, op: str, mips):
    if mips.is_binary(left) and mips.save_old_val is None:
        left.printTables("random", mips)
    if mips.is_binary(right) and mips.save_old_val is None:
        right.printTables("random", mips)
    if mips.is_unary(left) and mips.save_old_val is None:
        left.printTable("random", mips)
    if mips.is_unary(right) and mips.save_old_val is None:
        right.printTables("random", mips)
    if mips.is_logical(left) and mips.save_old_val is None:
        left.printTables("random", mips)
    if mips.is_logical(right) and mips.save_old_val is None:
        right.printTables("random", mips)

    if left is None:
        return
    if right is None:
        return
    if mips.looping:
        if mips.is_value(left):
            mips.get_loop_param(left)
        if mips.is_value(right):
            mips.get_loop_param(right)
    new_case = False
    if mips.enter_fold:
        mips.enter_fold = False
        new_case = True
    if not new_case:
        mips.counter -= 1
    if left.name == "binary" or left.name == "logical" or left.name == "unary":
        left = mips.save_old_val
    if right.name == "binary" or right.name == "logical" or right.name == "unary":
        right = mips.save_old_val
    if left.name == 'function' or right.name == "function":
        return function_in_operation(left, right, op, mips)
    if left.name == "array" or right.name == "array":
        return array_in_operation(left, right, op, mips)
    left_pointer = False
    right_pointer = False
    if left.name == "pointer":
        left_pointer = True
    if right.name == "pointer":
        right_pointer = True
    if left.name == "pointer" or right.name == "pointer":
        return pointer_in_operation(left, right, op, mips)

    # get all types
    # move higher type if necessary
    load_left = True
    load_right = True
    if isinstance(right.value, int) or str(right.value).isdigit() or isinstance(right.value, float) or isfloat(str(right.value)):
        t = mips.get_next_highest_register_type("t", right.value)
        load_right = False
    elif isinstance(left.value, int) or str(left.value).isdigit() or isinstance(right.value, float) or isfloat(str(left.value)):
        t = mips.get_next_highest_register_type("t", left.value)
        load_left = False

    #load left type
    if load_left:
        if left.type is LiteralType.VAR:
            ltype = mips.c_function.root.block.getSymbolTable().findSymbol(left.value)[1]
        else:
            ltype = left.type
        #load_type(old_var, mips.get_variable(right.value), rtype, right_pointer)
    else:
        #save to data+ load from data
        pass

    #load right type
    if load_right:
        if right.type == LiteralType.VAR:
            rtype = mips.c_function.root.block.getSymbolTable().findSymbol(right.value)[1]
        else:
            rtype = right.type
        #mips.function_load += load_type(old_var, mips.get_variable(right.value), rtype, right_pointer)
    else:
        #save to data+ load from data
        pass
    # fix different types

    """if rtype == LiteralType.FLOAT and ltype == LiteralType.INT:
        mips.function_load += load_higher_type_int_to_float(mips.get_variable(left.value),
                                                            mips.add_variable(left.value))
    if rtype == LiteralType.INT and ltype == LiteralType.FLOAT:
        mips.function_load += load_higher_type_int_to_float(mips.get_variable(right.value),
                                                            mips.add_variable(right.value))"""
        # rtype = LiteralType.FLOAT

    if op == "*" or op == "/" or op == "+" or op == "-" or op == "%" or op == ">=" or op == "<=" or op == ">" or op == "<" or op == "==" or op == "&&":
        mips.function_load += stor_binary_operation(op, left, right, rtype, mips, load_left, load_right)
        mips.function_load += "\n"
        if op == ">=" or op == "<=" or op == ">" or op == "<" or op == "==" or op == "&&":

            mips.comparator_found = True
        else:
            mips.comparator_found = False
    else:
        raise NotSupported("operator", op, left.line)
    return ltype


def function_in_operation(left, right, op: str, llvm):
    if llvm.is_function(left):
        left = load_function(left, llvm)
    if llvm.is_function(right):
        right = load_function(right, llvm)
    if right is None:
        return set_llvm_unary_operators(left, op, llvm)
    # if declaration with function x=function() en geen verder operaties
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
    if right is None:
        set_llvm_unary_operators(left, op, llvm)
    # if declaration with function x=function() en geen verder operatoes
    if left is None or right is None:
        return
    return set_llvm_binary_operators(left, right, op, llvm)


def load_pointer(left, llvm):
    for i in range(1, left.getPointerLevel()):
        old_val = llvm.get_variable(left.getValue())
        new_val = llvm.add_variable(left.getValue())
        llvm.function_load += "%{} = load ptr, ptr %{}, align 8\n".format(new_val, old_val)
    return llvm.make_value(lit=new_val, valueType=left.getType(), line=left.line)


def pointer_in_operation(left, right, op, llvm):
    if llvm.is_pointer(left):
        left = load_pointer(left, llvm)
    if llvm.is_pointer(right):
        right = load_pointer(right, llvm)
    if right is None:
        set_llvm_unary_operators(left, op, llvm)
    if left is None or right is None:
        return
    return set_llvm_binary_operators(left, right, op, llvm)


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

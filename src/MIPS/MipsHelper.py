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


def load_type(left, mips):
    a = ""
    # todo fix pointer type
    if mips.is_pointer(left):
        pass
    else:
        s = mips.register[left.value]
        # temporaries dont need to be loaded
        if s[0] == 't' or s[0] == 'f':
            return
        f = mips.frame_register[mips.register[left.value]]
        mips.text += "lw  ${}, {}\n".format(s, f)


def load_higher_type_int_to_float(old, new):
    return "%{} = sitofp i32 %{} to float\n".format(new, old)


def load_higher_type_bool_to_int(old, new):
    return "%{} = zext i1 %{} to i32\n".format(new, old)


def get_unary_operation(op: str, rtype):
    if op == "!":
        return "nor"
    if op == "++" and rtype == LiteralType.INT:
        return "addu"
    if op == "++" and rtype == LiteralType.FLOAT:
        return "add.s"
    if op == "-" and rtype == LiteralType.INT:
        return "subu"
    if op == "-" and rtype == LiteralType.FLOAT:
        return "sub.s"


def get_operation(op: str, type):
    if op == "-" and (type == LiteralType.INT or type == 'INT'):
        return "subu"
    if op == "-" and (type == LiteralType.FLOAT or type == 'FLOAT'):
        return "sub.s"
    if op == "+" and (type == LiteralType.INT or type == 'INT'):
        return "addu"
    if op == "+" and (type == LiteralType.FLOAT or type == 'FLOAT'):
        return "add.s"
    if op == "*" and (type == LiteralType.INT or type == 'INT'):
        return "mul"
    if op == "*" and (type == LiteralType.FLOAT or type == 'FLOAT'):
        return "mul.s"
    if op == "/" and (type == LiteralType.INT or type == 'INT'):
        return "div"
    if op == "/" and (type == LiteralType.FLOAT or type == 'FLOAT'):
        return "div.s"
    # TODO fist devide then save modulo
    if op == "%" and (type == LiteralType.INT or type == 'INT'):
        return "mfhi"
    if op == "%" and (type == LiteralType.FLOAT or type == 'FLOAT'):
        raise NotSupported("%", "float")
    if op == ">" and (type == LiteralType.INT or type == 'INT'):
        return "sgt"
    if op == ">" and (type == LiteralType.FLOAT or type == 'FLOAT'):
        return "sgt"
    if op == ">=" and (type == LiteralType.INT or type == 'INT'):
        return "sge"
    if op == ">=" and (type == LiteralType.FLOAT or type == 'FLOAT'):
        return "sge"
    if op == "<" and (type == LiteralType.INT or type == 'INT'):
        return "slt"
    if op == "<" and (type == LiteralType.FLOAT or type == 'FLOAT'):
        return "slt"
    if op == "<=" and (type == LiteralType.INT or type == 'INT'):
        return "sle"
    if op == "<=" and (type == LiteralType.FLOAT or type == 'FLOAT'):
        return "slte"
    if op == "==" and (type == LiteralType.INT or type == 'INT'):
        return "seq"
    if op == "==" and (type == LiteralType.FLOAT or type == 'FLOAT'):
        return "seq"
    if op == "&&" and (type == LiteralType.INT or type == 'INT'):
        return "and"
    if op == "&&" and (type == LiteralType.FLOAT or type == 'FLOAT'):
        return "and"
    if op == "||" and (type == LiteralType.INT or type == 'INT'):
        return "or"
    if op == "||" and (type == LiteralType.FLOAT or type == 'FLOAT'):
        return "or"


def store_unary_operation(op, right, rtype, mips):
    load = ""
    op = get_unary_operation(op, rtype)
    sr = mips.register[right.value]
    save = mips.register[mips.declaration.value]

    mips.text += "{} ${}, ${} ,${}\n".format(op, save, sr, "zero")
    if mips.register[mips.declaration.value] in mips.frame_register:
        fr = mips.frame_register[mips.register[mips.declaration.value]]
        mips.text += "sw ${}, {}\n".format(save, fr)


def store_binary_operation(op, left, right, rtype, mips):
    # save olf variable counter
    mips.save_old_val = left

    sl = mips.register[left.value]
    sr = mips.register[right.value]
    save = mips.register[mips.declaration.value]

    opi = get_operation(op, rtype)
    mips.text += "{} ${},${}, ${}\n".format(opi, save, sl, sr)
    # store back in frame
    if mips.register[mips.declaration.value] in mips.frame_register:
        fr = mips.frame_register[mips.register[mips.declaration.value]]
        if save[0] == 'f':
            mips.text += "s.s ${}, {}\n".format(save, fr)
        else:
            mips.text += "sw ${}, {}\n".format(save, fr)


def set_llvm_unary_operators(right, op: str, mips):
    load_right = True
    if mips.is_binary(right) and mips.save_old_val is None:
        right.printTables("random", mips)
    if mips.is_unary(right) and mips.save_old_val is None:
        right.printTables("random", mips)
    if mips.is_logical(right) and mips.save_old_val is None:
        right.printTables("random", mips)
    if right.name == "function":
        right = load_function(right, mips)
        # load_right = False
    if right.name == "array":
        array_in_operation(right, None, op, mips)
    right_pointer = False
    if right.name == "pointer":
        right_pointer = True
        right = load_pointer(right, mips)
    if right is None:
        return
    # get all types
    # move higher type if necessary

    if isinstance(right.value, int) or str(right.value).isdigit():
        mips.get_next_highest_register_type("t", right)
        load_right = False
    elif isinstance(right.value, float) or isfloat(str(right.value)):
        mips.get_next_highest_register_type("f", right)
        load_right = False
    rtype = right.type
    # load right type
    if load_right:
        if right.type == LiteralType.VAR:
            rtype = mips.c_function.block.getSymbolTable().findSymbol(right.value)[1]
        else:
            rtype = right.type
        load_type(right, mips)
    else:
        # save to data+ load from data
        save_to_data(right, mips)
        # fix different types

    """if rtype == LiteralType.FLOAT and ltype == LiteralType.INT:
        mips.function_load += load_higher_type_int_to_float(mips.get_variable(left.value),
                                                            mips.add_variable(left.value))
    if rtype == LiteralType.INT and ltype == LiteralType.FLOAT:
        mips.function_load += load_higher_type_int_to_float(mips.get_variable(right.value),
                                                            mips.add_variable(right.value))"""

    if op == "!" or op == "++" or op == "--":
        store_unary_operation(op, right, rtype, mips)
    else:
        raise NotSupported("operator", op, right.line)
    return rtype


def save_to_data(left, mips):
    if str(left.value).isdigit():
        mips.text += "ori ${},$0,{}\n".format(mips.register[left.value], left.value)
    elif isfloat(left.value):
        mips.load_float(left.value)
        s = mips.get_register(left.value, 'f', left.type)
        mips.text += "lwc1 ${}, $${}\n".format(s, mips.data_count)

        """s = mips.get_register(left.value, 'f', left.type)
        mips.text += "l.s ${}, {}\n".format(s, mips.float_to_hex(left.value))"""

    else:
        mips.data_count += 1
        mips.data_dict[left.value] = mips.data_count
        mips.data += "$${}  : .byte {} \"\n".format(mips.data_count, left.value)
        mips.text += "lb ${} , $${}\n".format(mips.register[left.value], mips.data_count)


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
    if left.name == "binary" or left.name == "logical" or left.name == "unary":
        left = mips.save_old_val
    elif right.name == "binary" or right.name == "logical" or right.name == "unary":
        right = mips.save_old_val
    load_left = True
    load_right = True

    if left.name == 'function':
        # load_left = False
        left = load_function(left, mips)
    if right.name == 'function':
        # load_right = False
        right = load_function(right, mips)

    if left.name == "array" or right.name == "array":
        return array_in_operation(left, right, op, mips)
    left_pointer = False
    right_pointer = False
    if left.name == "pointer":
        left_pointer = True
    if right.name == "pointer":
        right_pointer = True
    if left.name == "pointer":
        left = load_pointer(left, mips)
    if right.name == "pointer":
        right = load_pointer(right, mips)
    # get all types
    # move higher type if necessary

    if isinstance(right.value, int) or str(right.value).isdigit():
        load_right = False
        mips.get_next_highest_register_type("t", right)
    elif isinstance(right.value, float) or isfloat(str(right.value)):
        mips.get_next_highest_register_type("f", right)
        load_right = False
    if isinstance(left.value, int) or str(left.value).isdigit():
        load_right = False
        mips.get_next_highest_register_type("t", left)
    elif isinstance(right.value, float) or isfloat(str(left.value)):
        mips.get_next_highest_register_type("f", left)
        load_left = False
    ltype = left.type
    rtype = right.type

    # load left type
    if load_left:
        if left.type is LiteralType.VAR:
            ltype = mips.c_function.block.getSymbolTable().findSymbol(left.value)[1]
        else:
            ltype = left.type
        load_type(left, mips)
    else:
        # save to data+ load from data
        save_to_data(left, mips)

    # load right type
    if load_right:
        if right.type == LiteralType.VAR:
            rtype = mips.c_function.block.getSymbolTable().findSymbol(right.value)[1]
        else:
            rtype = right.type
        load_type(right, mips)
    else:
        # save to data+ load from data
        save_to_data(right, mips)
    # fix different types

    """if rtype == LiteralType.FLOAT and ltype == LiteralType.INT:
        mips.function_load += load_higher_type_int_to_float(mips.get_variable(left.value),
                                                            mips.add_variable(left.value))
    if rtype == LiteralType.INT and ltype == LiteralType.FLOAT:
        mips.function_load += load_higher_type_int_to_float(mips.get_variable(right.value),
                                                            mips.add_variable(right.value))"""
    # rtype = LiteralType.FLOAT
    if op == "*" or op == "/" or op == "+" or op == "-" or op == "%" or op == ">=" or op == "<=" or op == ">" or op == "<" or op == "==" or op == "&&" or op == "||":
        store_binary_operation(op, left, right, rtype, mips)

    else:
        raise NotSupported("operator", op, left.line)
    # return ltype
    mips.remove_temps()
    return


def load_function(p, mips):
    v = mips.make_value(lit='$function', valueType=p.expected["return"], line=p.line)
    mips.to_function_dec(p, v)
    # return l
    return v


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


def load_pointer(p, mips):
    v = mips.make_value(lit='$pointer', valueType=p.type, line=p.line)
    mips.to_pointer_dec(p, v)
    # return l
    return v


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

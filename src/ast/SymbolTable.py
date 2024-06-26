import pandas as pd
from src.ast.node import *
from collections import OrderedDict


class block:
    pass


class FunctionTable:
    def __init__(self):
        self.functions = OrderedDict()
        # self.table = pd.DataFrame({"param": pd.Series(dtype=dict),
        #                            "body": pd.Series(dtype=block)})

    def __eq__(self, other):
        if not isinstance(other, FunctionTable):
            return False
        return self.functions.equals(other.functions)

    def addFunction(self, func: Scope):
        function = OrderedDict()  # TODO: use ordered dict
        for param in func.parameters:
            function[param] = str(func.parameters[param].type)
        if func.f_return is None:
            if func.return_type is None:
                function["return"] = "void"
            elif func.forward_declaration:
                function["return"] = str(func.return_type);
            else:
                raise wrongReturnType(func.f_name, func.line, str(func.return_type), "void")
        elif func.return_type is None:
            raise wrongReturnType(func.f_name, func.line, "void", str(func.f_return.root.getType()))
        elif (func.f_return.root.name == "function" and func.f_return.root.f_name == func.f_name) or func.return_type == func.f_return.root.getType():
            function["return"] = str(func.return_type)
        else:
            raise wrongReturnType(func.f_name, func.line, str(func.return_type), str(func.f_return.root.getType()))
        function["forDecl"] = func.forward_declaration
        if not self.functions:
            self.functions[func.f_name] = function
        elif func.f_name in self.functions:
            if self.functions[func.f_name]["forDecl"]:
                temp = self.functions[func.f_name]
                if len(function) != len(temp):
                    raise forwardWrongSize(func.f_name, func.line)
                for para in function:
                    if para == "forDecl":
                        continue
                    if temp[para] != function[para]:
                        raise forwardWrongType(func.f_name, func.line)
                self.functions[func.f_name]["forDecl"] = False
            else:
                raise RedeclarationF(func.f_name, func.line)
        else:
            self.functions[func.f_name] = function

    def findFunction(self, f_name: str, line: int = 0):
        if f_name in self.functions:
            return self.functions[f_name]
        else:
            raise NotDeclared(f_name, line)

    # TODO: for pointers/references --> give block that calls the function?
    def callFunction(self, f_name: str, block: block, param: list):
        pass


class SymbolTable:
    def __init__(self):
        """
        position meegeven,
        """
        self.table = pd.DataFrame({"Value": pd.Series(dtype=str),
                                   "Type": pd.Series(dtype=str),
                                   "Const": pd.Series(dtype=bool),
                                   "Level": pd.Series(dtype=int),
                                   "Global": pd.Series(dtype=bool),
                                   "Fillable": pd.Series(dtype=bool),
                                   "Array": pd.Series(dtype=bool)})
        self.parent = None

    def __eq__(self, other):
        if not isinstance(other, SymbolTable):
            return False
        return self.table.equals(other.table)

    def setParent(self, parent):
        self.parent = parent

    def addSymbol(self, root: AST_node, isGlobal: bool, fill: bool = True):
        # TODO: check if x is in upper scope, x = 5 replaces upper scope
        if isinstance(root, Array) or isinstance(root.getLeftChild(), Array):
            return self.addArray(root, isGlobal, fill)
        try:
            line = root.getLine()
            if not isinstance(root, Declaration):
                raise NotDeclaration(line)
            else:
                name = root.getLeftChild().getValue()
                if root.getRightChild() is not None:
                    if isinstance(root.getRightChild(), Array):
                        # TODO: cleaning already replaces the value -> if this is the case: just use the value, don't look up
                        value = self.findSymbol(root.getRightChild().getValue(), False,
                                                root.getRightChild().getPosition())
                        if isinstance(value, tuple):
                            value = value[0]
                    else:
                        value = root.getRightChild().getValue()
                else:
                    value = None
                symType = root.getLeftChild().getType()
                const = root.getLeftChild().const
                decl = root.getLeftChild().declaration
                if isinstance(root.rightChild, Array):
                    deref = False
                else:
                    deref = root.getRightChild().deref
                if isinstance(root.getLeftChild(), Value) and root.getLeftChild().isVariable():
                    ref = None
                    level = 0
                elif isinstance(root.getLeftChild(), Pointer):
                    level = root.getLeftChild().getPointerLevel()
                    if root.getRightChild() is not None:
                        ref = root.getRightChild().getValue()
                    else:
                        ref = None
                else:
                    raise LeftSideDeclaration(line)
            if value is None:
                fill = False
            if level == 0 and ref is not None:
                raise WrongPointer(line)
            elif name not in self.table.index:
                if not decl:
                    if self.parent is None:
                        raise NotDeclared(name, line)
                    else:
                        self.parent.addSymbol(root, isGlobal, fill)
                if ref is None:
                    if isinstance(root.getLeftChild(), Pointer):
                        self.table.loc[name] = [str(value), symType, const, level, isGlobal, False, False]
                    else:
                        self.table.loc[name] = [str(value), symType, const, level, isGlobal,
                                                fill, False]  # TODO: use deref to make sure a reference can not be placed in a normal variable once introduced
                    return "placed"
                elif ref not in self.table.index:
                    if root.getRightChild().value == 0: # TODO: added to make int* a; work
                        self.table.loc[name] = ['', symType, const, level, isGlobal, fill, False]
                        return "placed"
                    else:
                        raise ImpossibleRef(ref, line)
                refValue = self.table.loc[ref]
                if deref and level - 1 != refValue["Level"]:
                    raise RefPointerLevel(name, refValue["Level"], level, line)
                elif not deref and level != refValue["Level"]:
                    raise RefPointerLevel(name, refValue["Level"], level, line)
                elif symType != refValue["Type"]:
                    raise PointerType(name, refValue["Type"], symType, line)
                self.table.loc[name] = [str(value), symType, const, level, isGlobal, fill, False]
                return "placed"
            else:
                row = self.table.loc[name]
                if decl:
                    if isinstance(root.getLeftChild(),
                                  Value):  # and isinstance(root.getRightChild(), Value) and not root.getRightChild().deref:
                        raise Redeclaration(name, line)
                    else:
                        raise PointerRedeclaration(name, line)
                elif row["Global"]:
                    raise ResetGlobal(name, line)
                elif row["Const"] and isinstance(root.getLeftChild(),
                                                 Value) and not root.getRightChild().deref:  # TODO: check if deref can be used to let const pointer only not reset value of memorylocation, but reset memorylocation is possible
                    raise ResetConst(name, line)
                elif row["Const"] and isinstance(root.getLeftChild(), Pointer) and not root.getRightChild().deref:
                    raise ResetConstPointer(name, line)
                elif row["Type"] != symType:
                    raise TypeDeclaration(name, row["Type"], symType, line)
                elif row["Level"] != level and not root.getRightChild().deref:
                    raise PointerLevel(name, row["Level"], level+1, line)
                elif row["Level"] != level + 1 and root.getRightChild().deref:
                    raise PointerLevel(name, row["Level"], level, line)
                else:
                    if isinstance(root.getLeftChild(), Value):
                        self.table.loc[name, ["Value"]] = str(value)
                        self.table.loc[name, ["Fillable"]] = fill
                    else:
                        if ref in self.table.index:
                            self.table.loc[name, ["Value"]] = str(value)
                            self.table.loc[name, ["Fillable"]] = fill
                        elif root.getRightChild().getType() != LiteralType.VAR:
                            for i in range(level):
                                temp = self.table.loc[name]
                                name = temp["Value"]
                            temp = self.table.loc[name]
                            if temp["Level"] != 0:
                                raise WrongPointer(line)
                            elif temp["Const"] and not isinstance(root.leftChild, Pointer):
                                raise ResetConst(name, line)
                            self.table.loc[name, ["Value"]] = str(value)
                            self.table.loc[name, ["Fillable"]] = fill
                        else:
                            raise NotReference(line, ref)
                    return "replaced"

        except NotDeclaration:
            raise
        except LeftSideDeclaration:
            raise
        except WrongPointer:
            raise
        except ImpossibleRef:
            raise
        except RefPointerLevel:
            raise
        except PointerType:
            raise
        except Redeclaration:
            raise
        except PointerRedeclaration:
            raise
        except ResetGlobal:
            raise
        except ResetConst:
            raise
        except ResetConstPointer:
            raise
        except TypeDeclaration:
            raise
        except PointerLevel:
            raise
        except NotReference:
            raise

    def addArray(self, root: AST_node, isGlobal: bool, fill: bool):
        try:
            if isinstance(root, Array):
                if not root.declaration:
                    raise NotDeclared(root.value, root.line)
                elif root.value in self.table.index:
                    raise Redeclaration(root.value, root.line)
                elif len(root.arrayContent) != 0 and len(root.arrayContent) != root.pos.value:
                    raise ArraySize(root.value, root.pos.value, root.line)
                elif root.value not in self.table.index:
                    self.table.loc[root.value] = [root.pos.value, root.type, True, 0, isGlobal,
                                                  fill, True]  # TODO: check if arrays are indeed always const
                    for pos in range(root.pos.value):
                        name = str(pos) + root.value
                        if len(root.arrayContent) != 0:
                            arrayValue = root.arrayContent[pos].value
                        else:
                            arrayValue = None
                        self.table.loc[name] = [arrayValue, root.type, False, 0, isGlobal, fill, False]
                    return "placed"
            elif isinstance(root, Declaration):
                position = root.getLeftChild().pos.value
                position = int(position)
                name = str(position) + str(root.getLeftChild().value)
                if root.getLeftChild().declaration:
                    raise Redeclaration(name, root.line)
                elif name not in self.table.index:
                    raise NotDeclared(str(position) + str(root.getLeftChild().value),
                                      root.getLeftChild().line)
                elif position >= self.table.loc[root.getLeftChild().value]["Value"] or position < 0:
                    raise ArrayOutOfBounds(name, root.getLeftChild().line, position)
                elif name in self.table.index:
                    # name = str(position) + root.getLeftChild().name
                    row = self.table.loc[name]
                    if row["Type"] != root.getRightChild().type:
                        raise TypeDeclaration
                    self.table.loc[name, ["Value"]] = str(root.getRightChild().value)
                    self.table.loc[name, ["Fillable"]] = fill
                    return "replaced"

        except NotDeclared:
            raise
        except Redeclaration:
            raise
        except TypeDeclaration:
            raise
        except ArrayOutOfBounds:
            raise
        except ArraySize:
            raise

    def findSymbol(self, name: str, onlyNext: bool = False, pos: int = None,
                   line: int = None):
        if name not in self.table.index:
            if self.parent is not None:  # TODO: check if this gives no problems (changed to find elements in global scope)
                return self.parent.findSymbol(name, onlyNext, pos)
            else:
                return None
        if pos is not None:
            if isinstance(pos, str) and not pos.isnumeric():
                if name not in self.table.index:
                    if self.parent is not None:  # TODO: check if this gives no problems (changed to find elements in global scope)
                        pos = self.parent.findSymbol(name)
                    else:
                        return None
                else:
                    pos = self.table.at[pos, "Value"]
                    if isinstance(pos, str) and pos.isnumeric():
                        pos = int(pos)
            elif isinstance(pos, str) and pos.isnumeric():
                pos = int(pos)
            try:
                if pos < 0 or pos >= self.table.at[name, "Value"]:
                    raise ArrayOutOfBounds(name, line, self.table.at[name, "Value"])
                arrayName = str(pos) + name
                return self.table.at[arrayName, "Value"], self.table.at[arrayName, "Type"], \
                    self.table.at[arrayName, "Level"], self.table.at[arrayName, "Fillable"]
            except ArrayOutOfBounds:
                raise
        if not onlyNext:
            if self.table.at[name, "Array"]:
                raise fullArrayOperation(name, line)
            level = self.table.at[name, "Level"]
            while self.table.at[name, "Level"] > 0:
                old = name
                name = self.table.at[name, "Value"]
                if name == '':
                    raise pointerNotAssigned(old, line)
            return self.table.at[name, "Value"], self.table.at[name, "Type"], level, self.table.at[name, "Fillable"]
        else:
            return self.table.at[name, "Value"], self.table.at[name, "Type"], self.table.at[name, "Level"], \
                self.table.at[name, "Fillable"]

    def makeUnfillable(self):
        self.table = self.table.assign(Fillable=False)

    def setParent(self, parent):
        self.parent = parent

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
        function = dict()  # TODO: use ordered dict
        for param in func.parameters:
            function[param] = func.parameters[param].type
        function["return"] = func.return_type
        if not self.functions:
            self.functions[func.f_name] = function
        elif func.f_name in self.functions:
            raise Redeclaration(func.f_name, func.line)
        else:
            self.functions[func.f_name] = function

    def findFunction(self, f_name: str, line: int):
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
                                   "Fillable": pd.Series(dtype=bool)})
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
                    value = root.getRightChild().getValue()
                else:
                    value = None
                symType = root.getLeftChild().getType()
                const = root.getLeftChild().const
                decl = root.getLeftChild().declaration
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
                    self.table.loc[name] = [value, symType, const, level, isGlobal, fill]
                    return "placed"
                elif ref not in self.table.index:
                    raise ImpossibleRef(ref, line)
                refValue = self.table.loc[ref]
                if not deref and level - 1 != refValue["Level"]:
                    raise RefPointerLevel(name, refValue["Level"], level, line)
                elif deref and level != refValue["Level"]:
                    raise RefPointerLevel(name, refValue["Level"], level, line)
                elif symType != refValue["Type"]:
                    raise PointerType(name, refValue["Type"], symType, line)
                self.table.loc[name] = [value, symType, const, level, isGlobal, fill]
                return "placed"
            else:
                row = self.table.loc[name]
                if decl:
                    if isinstance(root.getLeftChild(), Value):
                        raise Redeclaration(name, line)
                    else:
                        raise PointerRedeclaration(name, line)
                elif row["Global"]:
                    raise ResetGlobal(name, line)
                elif row["Const"] and isinstance(root.getLeftChild(), Value):
                    raise ResetConst(name, line)
                elif row["Const"] and isinstance(root.getLeftChild(), Pointer) and not root.getRightChild().variable:
                    raise ResetConstPointer(name, line)
                elif row["Type"] != symType:
                    raise TypeDeclaration(name, row["Type"], symType, line)
                elif row["Level"] != level:
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
                            elif temp["Const"]:
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
                elif len(root.arrayContent) != 0 and len(root.arrayContent) != root.pos:
                    raise ArraySize(root.value, root.pos, root.line)
                elif root.value not in self.table.index:
                    self.table.loc[root.value] = [root.pos, root.type, True, 0, isGlobal,
                                                 fill]  # TODO: check if arrays are indeed always const
                    for pos in range(root.pos):
                        name = str(pos) + root.value
                        if len(root.arrayContent) != 0:
                            arrayValue = root.arrayContent[pos].value
                        else:
                            arrayValue = None
                        self.table.loc[name] = [arrayValue, root.type, False, 0, isGlobal, fill]
                    return "placed"
            elif isinstance(root, Declaration):
                if root.getLeftChild().declaration:
                    raise Redeclaration(root.name, root.line)
                elif root.getLeftChild().name not in self.table.index:
                    raise NotDeclared(root.getLeftChild().name, root.getLeftChild().line)
                elif root.getLeftChild().pos >= self.table.loc[root.getLeftChild().name]["Value"] or \
                        root.getLeftChild().pos < 0:
                    raise ArrayOutOfBounds(root.getLeftChild().name, root.getLeftChild().line, root.getLeftChild().pos)
                elif root.getLeftChild().name in self.table.index:
                    name = str(root.getLeftChild().pos) + root.getLeftChild().name
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
                   line: int = None):  # TODO: tell adition of pos and line for arrayCall
        if name not in self.table.index:
            return None
        if pos is not None:
            try:
                if pos < 0 or pos >= self.table.at[name, "Value"]:
                    raise ArrayOutOfBounds(name, line, self.table.at[name, "Value"])
                arrayName = str(pos) + name
                return self.table.at[arrayName, "Value"], self.table.at[arrayName, "Type"], \
                       self.table.at[arrayName, "Level"], self.table.at[arrayName, "Fillable"]
            except ArrayOutOfBounds:
                raise
        if not onlyNext:
            level = self.table.at[name, "Level"]
            while self.table.at[name, "Level"] > 0:
                name = self.table.at[name, "Value"]
            return self.table.at[name, "Value"], self.table.at[name, "Type"], level, self.table.at[name, "Fillable"]
        else:
            return self.table.at[name, "Value"], self.table.at[name, "Type"], self.table.at[name, "Level"], \
                   self.table.at[name, "Fillable"]

    def makeUnfillable(self):
        self.table = self.table.assign(Fillable=False)

    def setParent(self, parent):
        self.parent = parent

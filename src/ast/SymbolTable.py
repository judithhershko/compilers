import pandas as pd
from src.ErrorHandeling.GenerateError import *
from src.ast.node import *


class SymbolTable:
    def __init__(self):
        self.table = pd.DataFrame({"Value": pd.Series(dtype=str),
                                   "Type": pd.Series(dtype=str),
                                   "Const": pd.Series(dtype=bool),
                                   # "Ref": pd.Series(dtype="str"),
                                   "Level": pd.Series(dtype=int),
                                   "Global": pd.Series(dtype=bool)})

    def addSymbol(self, root: AST_node, isGlobal: bool):
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
            #if (ref is None and level != 0) or
            if (level == 0 and ref is not None):
                raise WrongPointer(line)
            elif name not in self.table.index:
                if not decl:
                    raise NotDeclared(name, line)
                if ref is None:
                    self.table.loc[name] = [value, symType, const, level, isGlobal]
                    return "placed"
                elif ref not in self.table.index:
                    raise ImpossibleRef(ref, line)
                refValue = self.table.loc[ref]
                if level - 1 != refValue["Level"]:
                    raise RefPointerLevel(name, refValue["Level"], level, line)
                elif symType != refValue["Type"]:
                    raise PointerType(name, refValue["Type"], symType, line)
                self.table.loc[name] = [value, symType, const, level, isGlobal]
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
                # elif row["Level"] > 0:
                #     refRow = self.table.loc[ref]
                #     if refRow["level"] != level - 1:
                #         return "pointerLevel"
                #     self.table.loc[name, ["Value"]] = value
                #     return "replaced"
                else:
                    if isinstance(root.getLeftChild(), Value):
                        self.table.loc[name, ["Value"]] = str(value)
                    else:
                        if ref in self.table.index:
                            self.table.loc[name, ["Value"]] = str(value)
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
                            return "replaced"
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

    def findSymbol(self, name: str, onlyNext:bool = False): #, deref: int = 0):
        if name not in self.table.index:
            return None
        # elif deref == 0:
        #     return self.table.at[name, "Value"], self.table.at[name, "Type"]
        # elif deref > 0 and self.table.at[name, "level"] > 0:
        #     return self.findSymbol(self.table.at[name, "value"], deref=deref - 1)
        # else:
        #     return None
        if not onlyNext:
            level = self.table.at[name, "Level"]
            while self.table.at[name, "Level"] > 0:
                name = self.table.at[name, "Value"]
            return self.table.at[name, "Value"], self.table.at[name, "Type"], level
        else:
            return self.table.at[name, "Value"], self.table.at[name, "Type"], self.table.at[name, "Level"]

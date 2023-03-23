import pandas as pd
from src.ErrorHandeling.GenerateError import *
from src.ast.node import *


class SymbolTable:  # TODO: ask to add memory location?
    def __init__(self):
        self.table = pd.DataFrame({"Value": pd.Series(dtype="str"),
                                   "Type": pd.Series(dtype="str"),
                                   "Const": pd.Series(dtype="bool"),
                                   "Ref": pd.Series(dtype="str"),
                                   "Level": pd.Series(dtype="int")})

    def addSymbol(self, root: AST_node):
        try:
            line = root.getLine()
            if not isinstance(root, Declaration):
                raise NotDeclaration(line)
            else:
                name = root.getLeftChild().getValue()
                value = root.getRightChild().getValue()
                symType = root.getLeftChild().getType()
                const = root.getLeftChild().const
                decl = root.getLeftChild().declaration
                if isinstance(root.getLeftChild(), Value) and root.getLeftChild().isVariable():
                    ref = None
                    level = 0
                elif isinstance(root.getLeftChild(), Pointer):
                    level = root.getLeftChild().level
                    ref = root.getRightChild().getValue()
                else:
                    raise LeftSideDeclaration(line)
            if (ref is None and level != 0) or (level == 0 and ref is not None):
                raise WrongPointer(line)
            elif name not in self.table.index:
                if ref is None:
                    self.table.loc[name] = [value, symType, const, ref, level]
                    return "placed"
                elif ref not in self.table.index:
                    raise ImpossibleRef(ref, line)
                refValue = self.table.loc[ref]
                if level - 1 != refValue["Level"]:
                    raise RefPointerLevel(name, refValue["Level"], level, line)
                elif symType != refValue["Type"]:
                    raise PointerType(name, refValue["Type"], symType, line)
                self.table.loc[name] = [value, symType, const, ref, level]
                return "placed"
            else:
                row = self.table.loc[name]
                if decl:
                    raise Redeclaration(name, line)
                elif row["Const"]:
                    raise ResetConst(name, line)
                elif row["Type"] != symType:
                    raise TypeDeclaration(name, row["type"], symType, line)
                elif row["Level"] != level:
                    raise PointerLevel(name, row["Level"], level, line)
                # elif row["Level"] > 0:
                #     refRow = self.table.loc[ref]
                #     if refRow["level"] != level - 1:
                #         return "pointerLevel"
                #     self.table.loc[name, ["Value"]] = value
                #     return "replaced"
                else:
                    self.table.loc[name, ["Value"]] = value
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
        except ResetConst:
            raise
        except TypeDeclaration:
            raise
        except PointerLevel:
            raise

    def findSymbol(self, name: str, deref: int = 0):
        if name not in self.table.index:
            return None
        elif deref == 0:
            return self.table.at[name, "Value"]
        elif deref > 0 and self.table.at[name, "type"] == "pointer":
            return self.findSymbol(self.table.at[name, "ref"], deref=deref - 1)
        else:
            return None
